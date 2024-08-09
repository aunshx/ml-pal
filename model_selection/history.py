import json
import psycopg2
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain.memory import ConversationBufferMemory
from langchain_postgres import PGVector
import uuid
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
collection_names = {
    "object_detection": "od",
    "language_task": "llm",
    "multimodal_task": "mm"
}

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="od",  
    connection=connection,
    use_jsonb=True,
)

# Connect to PostgreSQL
db_conn = psycopg2.connect(
    dbname='langchain',
    user='langchain',
    password='langchain',
    host='localhost',
    port='6024'
)
db_cursor = db_conn.cursor()

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

def query_model(task_type):

    collection = collection_names.get(task_type, "od")  
    vector_store.collection_name = collection  

    results = vector_store.similarity_search("", k=1) 
    retrieved_documents = []
    for doc in results:
        retrieved_documents.append({
            "model_name": doc.metadata['type'],
            "description": doc.metadata.get('description', '')
        })
    return retrieved_documents

# If the model does not exist in the given document just say sorry we don't have a model for your specific needs.
template = """
Given the model schema for LLM models, you are an AI agent that should be able to answer all the user questions using the document alone.
Ask the user only the most essential questions needed to find the best match from the document. Limit your questions to a maximum of three.

Make sure that you don't ask questions that might have already been answered in the {chat_history}.
When you suggest a model and the user agrees to go ahead with it, provide more generic information of the model you suggested and stop the thread.
If the user questions or asks why this model was suggested, provide them information related to the use case of the user alone.

User Query and Context: {query_with_context}
AI Response:
"""

prompt = PromptTemplate(
    input_variables=["chat_history", "query_with_context"], template=template
)
llm = ChatOpenAI(model='gpt-4o')

memory = ConversationBufferMemory(memory_key="chat_history", input_key="user_input", output_key="response")

chain = RunnableSequence(prompt | llm)


def answer_query(query, retrieved_documents):
    chat_history = memory.load_memory_variables({})['chat_history']
    documents_json = json.dumps(retrieved_documents, indent=4)
    query_with_context = f"User Query: {query} Retrieved Documents: {documents_json}"
    input_data = {
        "chat_history": chat_history,
        "query_with_context": query_with_context
    }
    
    response = chain.invoke(input_data)
    response_content = response.content.strip() if hasattr(response, 'content') else str(response).strip()

    memory.save_context({"user_input": query}, {"response": response_content})
    
    return response_content

def save_memory_to_db(memory_data):
    # Extract chat history as a single string
    chat_history = memory_data.get('chat_history', '')

    # Generate a unique session ID
    session_id = str(uuid.uuid4())

    # Insert the entire conversation into the database
    if chat_history:
        print(f"Inserting session: session_id={session_id}, conversation={chat_history}")

        db_cursor.execute(
            "INSERT INTO conversation_history (id, conversation) VALUES (%s, %s)",
            (session_id, chat_history)
        )
    else:
        print("No conversation data to insert")

    db_conn.commit()

def main():
    print("You can start asking questions about the models. Type 'exit' to end the conversation.")
    retrieved_documents = None
    while True:
        query = input("User: ")

        if query.lower() in ["exit", "quit", "stop"]:
            print("AI: Goodbye!")
            break

        if retrieved_documents is None:
            task_type = determine_task_type(query)
            if task_type not in collection_names:
                print("Du: Sorry, we don't have a model for your specific needs.")
                continue

            retrieved_documents = query_model(task_type)

        langchain_response = answer_query(query, retrieved_documents)
        print("Dumbledore:", langchain_response)

    memory_data = memory.load_memory_variables({})
    save_memory_to_db(memory_data)

if __name__ == "__main__":
    main()
