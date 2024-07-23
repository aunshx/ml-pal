import json
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-proj-NvqIphRNzF9iGBurzBy2T3BlbkFJ1yFpMCXSYc2ubsrt8Xh1'

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client and collection
client = chromadb.Client(Settings(persist_directory="./chroma"))
collection = client.create_collection("model_index")

# Load JSON data
with open('LLM_task/tranformed_schema(test3).json', 'r') as f:
    json_data = json.load(f)

model_info_map = {}

def flatten_dict(d, parent_key='', sep=' - '):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Process each entry in the JSON data
for model_type, model_info in json_data.items():
    if isinstance(model_info, dict):
        flat_info = flatten_dict(model_info)
        text = ' - '.join(f"{key}: {value}" for key, value in flat_info.items() if value)
        
        embedding = model.encode(text).tolist()
        collection.add(
            embeddings=[embedding],
            metadatas=[{"description": flat_info.get('model_details - model_description', ''), "type": model_type}],
            ids=[flat_info.get('model_name', model_type)]
        )
        model_info_map[flat_info.get('model_name', model_type)] = model_info

def query_model(query_text):
    query_embedding = model.encode(query_text).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=2)
    
    if results and results['metadatas']:
        retrieved_documents = []
        for metadata, model_id in zip(results['metadatas'][0], results['ids'][0]):
            model_info = model_info_map.get(model_id, {})
            retrieved_documents.append({
                "model_name": model_id,
                "description": metadata["description"],
                "type": metadata["type"],
                "installation": model_info.get("example_implementation", {}).get("sample_code", ""),
                "full_info": model_info
            })
        return retrieved_documents
    else:
        return []

# Define the prompt template
template = """
Given the model schema for LLM models, you are an AI agent that should be able to answer all the user questions using the document alone.

User Query: {query}
Retrieved Documents: {documents}
AI Response:
"""

prompt = PromptTemplate(template=template, input_variables=['query', 'documents'])

# Initialize the OpenAI LLM
llm = ChatOpenAI(model='gpt-4o')

# Initialize the LLMChain with the LLM and prompt
chain = LLMChain(llm=llm, prompt=prompt)

def answer_query(query, retrieved_documents):
    documents_json = json.dumps(retrieved_documents, indent=4)
    formatted_prompt = prompt.format(query=query, documents=documents_json)
    response_content = chain.run({"query": query, "documents": documents_json}).strip()
    return response_content

# Example usage
query = "I want a model that is not transformed based. Is there any such model?"

# First, use the ChromaDB-based model query
retrieved_documents = query_model(query)

# Use the retrieved documents from ChromaDB for the LangChain LLM
langchain_response = answer_query(query, retrieved_documents)
print("LangChain AI Response:", langchain_response)
