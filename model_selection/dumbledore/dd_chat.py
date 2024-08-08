import json
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain.memory import ConversationBufferMemory
from langchain_postgres import PGVector
from model_selection.dumbledore.save_mem import MemoryDataSerializer
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
collection_name = "all_models"

vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

def query_model(query_text):

    results = vector_store.similarity_search(query_text, k=1)
    retrieved_documents = []
    for doc in results:
        retrieved_documents.append({
            "model_name": doc.metadata['type'],
            "description": doc.metadata.get('description', '')
        })
    return retrieved_documents

#If the model does not exist in the given document just say sorry we dont not have a model for your specific needs.
template = """
Given the model schema for LLM models, you are an AI agent that should be able to answer all the user questions using the document alone.
Ask the user only the most essential questions needed to find the best match from the document. Limit your questions to a maximum of three.

Make sure that you don't ask questions that might have already been answered in the {chat_history}.
When you suggest a model and the user agrees to go ahead with it, provide complete information of the model and stop the thread.

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

print("You can start asking questions about the models. Type 'exit' to end the conversation.")
while True:
    query = input("User: ")
    
    if query.lower() in ["exit", "quit", "stop"]:
        print("AI: Goodbye!")
        break

    retrieved_documents = query_model(query)
    langchain_response = answer_query(query, retrieved_documents)
    print("AI:", langchain_response)

memory_data = memory.load_memory_variables({})
serializer = MemoryDataSerializer()
serializer.save_memory_data_to_json(memory_data)