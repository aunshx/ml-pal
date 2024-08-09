import json
import uuid
import psycopg2
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain_postgres import PGVector, PostgresChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Define embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Database connection information
conn_info = "dbname=langchain user=langchain password=langchain host=localhost port=6024"

# Establish a synchronous connection to the database

sync_connection = psycopg2.connect(conn_info)

# Create the table schema (only needs to be done once)
table_name = "chat_history"
PostgresChatMessageHistory.create_tables(sync_connection, table_name)

# Generate a session ID for each conversation
session_id = str(uuid.uuid4())

# Initialize chat history with PostgreSQL
chat_history = PostgresChatMessageHistory(
    connection=sync_connection,  # Pass the actual connection object
    table_name=table_name,
    session_id=session_id
)

# Define the function to add initial messages
def initialize_chat():
    # Add initial system message
    chat_history.add_messages([
        SystemMessage(content="Welcome to the chat! Let's get started.")
    ])

# Define the function to determine task type
def determine_task_type(query_text):
    task_prompt = """
    Determine the task type based on the user query. The possible task types are:
    1. Object Detection
    2. Language Task
    3. Multimodal Task
    
    User Query: {query_text}
    
    Provide the task type as one of the following: object_detection, language_task, multimodal_task.
    """
    task_template = PromptTemplate(
        input_variables=["query_text"], template=task_prompt
    )
    task_llm = ChatOpenAI(model='gpt-4o')
    task_chain = RunnableSequence(task_template | task_llm)
    
    task_input_data = {"query_text": query_text}
    task_response = task_chain.invoke(task_input_data)
    task_type = task_response.content.strip().lower()
    
    return task_type

# Define query model function
def query_model(task_type):
    collection_names = {
        "object_detection": "od",
        "language_task": "llm",
        "multimodal_task": "mm"
    }
    collection = collection_names.get(task_type, "od")
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection,
        connection="postgresql+psycopg2://langchain:langchain@localhost:6024/langchain",
        use_jsonb=True,
    )
    results = vector_store.similarity_search("", k=1)
    retrieved_documents = []
    for doc in results:
        retrieved_documents.append({
            "model_name": doc.metadata['type'],
            "description": doc.metadata.get('description', '')
        })
    return retrieved_documents

# Define prompt and LLM chain
template = """
Given the model schema for LLM models, you are an AI agent that should be able to answer all the user questions using the document alone.
Ask the user only the most essential questions needed to find the best match from the document. Limit your questions to a maximum of three.

Make sure that you don't ask questions that might have already been answered in the chat history.
When you suggest a model and the user agrees to go ahead with it, provide more generic information of the model you suggested and stop the thread.
If the user questions or asks why this model was suggested, provide them information related to the use case of the user alone.

User Query and Context: {query_with_context}
AI Response:
"""

prompt = PromptTemplate(
    input_variables=["chat_history", "query_with_context"], template=template
)
llm = ChatOpenAI(model='gpt-4o')

chain = RunnableSequence(prompt | llm)

# Define function to answer query
def answer_query(query, retrieved_documents):
    chat_history_list = chat_history.get_messages()  # Load chat history from PostgreSQL
    documents_json = json.dumps(retrieved_documents, indent=4)
    query_with_context = f"User Query: {query} Retrieved Documents: {documents_json}"
    input_data = {
        "chat_history": chat_history_list,
        "query_with_context": query_with_context
    }
    
    response = chain.invoke(input_data)
    response_content = response.content.strip() if hasattr(response, 'content') else str(response).strip()

    chat_history.add_message(HumanMessage(content=query))  # Save user query
    chat_history.add_message(AIMessage(content=response_content))  # Save AI response
    
    return response_content

# Main function
def main():
    print("You can start asking questions about the models. Type 'exit' to end the conversation.")
    initialize_chat()  # Initialize chat with system message
    retrieved_documents = None
    while True:
        query = input("User: ")
        
        if query.lower() in ["exit", "quit", "stop"]:
            print("AI: Goodbye!")
            break

        if retrieved_documents is None:
            task_type = determine_task_type(query)
            if task_type not in ["object_detection", "language_task", "multimodal_task"]:
                print("AI: Sorry, we don't have a model for your specific needs.")
                continue

            retrieved_documents = query_model(task_type)

        langchain_response = answer_query(query, retrieved_documents)
        print("AI:", langchain_response)

if __name__ == "__main__":
    main()
