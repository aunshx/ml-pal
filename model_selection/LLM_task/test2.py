import json
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-proj-NvqIphRNzF9iGBurzBy2T3BlbkFJ1yFpMCXSYc2ubsrt8Xh1'

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the ChromaDB client
client = chromadb.Client(Settings(persist_directory="./chroma"))

# Create a collection for the model index
collection = client.create_collection("model_index")

# Load the JSON data
with open('LLM_task/LLM_models_schema.json', 'r') as f:
    json_data = json.load(f)

model_info_map = {}

# Process the JSON data
for model_type, model_info in json_data.items():
    model_name = model_type  # Assume model_type is the model name
    model_overview = model_info.get("Model Overview", "")
    model_details = model_info.get("model_details", {}).get("model_description", "")
    example_implementation = model_info.get("example_implementation", {})
    model_installation = example_implementation.get("sample_code", "") if example_implementation else ""

    # Concatenate the text information for encoding
    text = f"{model_name} - {model_overview} - {model_details} - {model_installation}"
    embedding = model.encode(text).tolist()

    # Add the model information to the ChromaDB collection
    collection.add(
        embeddings=[embedding],
        metadatas=[{"description": model_overview, "type": model_type}],
        ids=[model_name]
    )

    model_info_map[model_name] = model_info

# Function to query the vector database and generate a descriptive answer
def query_model(query_text):
    query_embedding = model.encode(query_text).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=1)
    
    if results and results['metadatas']:
        top_result = results['metadatas'][0][0]
        model_name = results['ids'][0][0]
        model_description = top_result["description"]
        model_type = top_result["type"]
        model_installation = model_info_map[model_name].get("example_implementation", {}).get("sample_code", "")
        response = f"The best model for the query is {model_name} from the category {model_type}. It is described as: {model_description}. To use this model, you can follow the instructions: {model_installation}."
        return response
    else:
        return "No relevant model found for the query."

# Load the original data for LangChain LLM
with open('LLM_task/LLM_models_schema_new.json', 'r') as infile:
    original_data = json.load(infile)

# Define the prompt template
template = """
Given the model schema for LLM models, you are an AI agent that should be able to answer all the user questions using the document.

Original JSON:
{context}

User Query: {query}
AI Response:
"""

prompt = PromptTemplate(template=template, input_variables=['context', 'query'])

# Initialize the OpenAI LLM
llm = ChatOpenAI(model='gpt-4')

# Initialize the LLMChain with the LLM and prompt
chain = LLMChain(llm=llm, prompt=prompt)

def answer_query(query, context):
    formatted_prompt = prompt.format(context=context, query=query)
    response_content = chain.run({"context": context, "query": query}).strip()
    return response_content

# Example usage
context = json.dumps(original_data, indent=4)
query = "WHich model is the best for code generation task? and what is the model size?"

# First, use the ChromaDB-based model query
model_query_response = query_model(query)
print('ChromaDB Response:', model_query_response)

# Then, use the LangChain LLM for additional context-based response
langchain_response = answer_query(query, context)
print("LangChain AI Response:", langchain_response)

