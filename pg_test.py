import json
import os
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from langchain.memory import ConversationBufferMemory
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
import getpass

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

#os.environ['OPENAI_API_KEY'] = 'sk-proj-NvqIphRNzF9iGBurzBy2T3BlbkFJ1yFpMCXSYc2ubsrt8Xh1'
# Uses psycopg3!
connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"
collection_name = "all_models"
# 06c9e80d-fe54-461a-8e35-d244b0a0c19f
vector_store = PGVector(
    embeddings= embeddings,
    collection_name=collection_name,
    connection=connection,
    use_jsonb=True,
)

with open('model_selection/schema/model_list_schema.json', 'r') as f:
    json_data = json.load(f)

model_info_map = {}

for model_type, model_info in json_data.items():
    model_name = model_type  # Assume model_type is the model name
    model_overview = model_info.get("Model Overview", "")
    model_details = model_info.get("model_details", {}).get("model_description", "")
    example_implementation = model_info.get("example_implementation", {})
    model_architecture = model_info.get("model_details", {}).get("model_description", "")
    model_installation = example_implementation.get("sample_code", "") if example_implementation else ""

    text = f"{model_name} - {model_overview} - {model_details} - {model_installation}"
    embedding = embeddings.embed_query(text)
       
    vector_store.add_documents([
        Document(
            page_content=text,
            metadata={"description": model_architecture, "type": model_type},
        )
    ])
    model_info_map[model_name] = model_info

def query_model(query_text):
    #query_embedding = embeddings.embed_query(query_text)
    results = vector_store.similarity_search(query_text, k=1)
    
    retrieved_documents = []
    for doc in results:
        model_info = model_info_map.get(doc.metadata['type'], {})
        retrieved_documents.append({
            "model_name": doc.metadata['type']
        })
    return retrieved_documents

template = """
Given the model schema for LLM models, you are an AI agent that should be able to answer all the user questions using the document alone.
Keep asking the user questions until you find the perfect match from the document. Suggest the model only in the end until then ask the user questions that you can use to find the best match. Ask concise questions.
If the model does not exist in the given document just say sorry we dont not have a model for youir specific needs.

Make sure that you dont ask questions that might have already been answered in the {chat_history}.
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


