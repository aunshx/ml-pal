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
with open('tranformed_schema.json', 'r') as f:
    json_data = json.load(f)

model_info_map = {}


for model_type, model_info in json_data.items():
    if isinstance(model_info, dict):
        model_name = model_info.get("model_name", model_type)
        developed_by = model_info.get("developed_by", "")
        model_type_info = model_info.get("model_type", "")
        licensing = model_info.get("licensing", "")
        installation = model_info.get("installation", {})
        python_version = installation.get("python_version", "")
        additional_libraries = installation.get("additional_libraries", "")
        installation_command = installation.get("installation_command", "")
        usage = model_info.get("usage", {})
        cli_example = usage.get("cli_example", "")
        python_example = usage.get("python_example", "")
        pretrained_models = model_info.get("pretrained_models_and_performance_metrics", {})
        available_models = pretrained_models.get("available_models", "")
        pretrained_datasets = pretrained_models.get("pretrained_datasets", "")
        performance_metrics = pretrained_models.get("performance_metrics", {})
        model_architecture = model_info.get("model_details", {}).get("model_description", "")
        supported_labels = model_info.get("model_details", {}).get("supported_labels", "")
        limitations = model_info.get("limitations_and_biases", {}).get("limitations", "")
        biases = model_info.get("limitations_and_biases", {}).get("biases", "")
        risks = model_info.get("limitations_and_biases", {}).get("risks", "")
        recommendations = model_info.get("recommendations", "")
        hardware = model_info.get("compute_infrastructure", {}).get("hardware", "")
        software = model_info.get("compute_infrastructure", {}).get("software", "")
        model_card_contact = model_info.get("contact_information", {}).get("model_card_contact", "")
        related_papers_and_resources = model_info.get("references", {}).get("related_papers_and_resources", "")
        sample_code = model_info.get("example_implementation", {}).get("sample_code", "")
        
        text = (f"{model_name} - Developed by: {developed_by} - Model Type: {model_type_info} - Licensing: {licensing} "
                f"- Python Version: {python_version} - Additional Libraries: {additional_libraries} "
                f"- Installation Command: {installation_command} - CLI Example: {cli_example} "
                f"- Python Example: {python_example} - Available Models: {available_models} "
                f"- Pretrained Datasets: {pretrained_datasets} - Performance Metrics: {performance_metrics} "
                f"- Model Architecture: {model_architecture} - Supported Labels: {supported_labels} "
                f"- Limitations: {limitations} - Biases: {biases} - Risks: {risks} "
                f"- Recommendations: {recommendations} - Hardware: {hardware} - Software: {software} "
                f"- Model Card Contact: {model_card_contact} - Related Papers and Resources: {related_papers_and_resources} "
                f"- Sample Code: {sample_code}")
        
        embedding = model.encode(text).tolist()
        collection.add(
            embeddings=[embedding],
            metadatas=[{"description": model_architecture, "type": model_type}],
            ids=[model_name]
        ) ## Takes in json file data emdeddings
        model_info_map[model_name] = model_info

def query_model(query_text):
    query_embedding = model.encode(query_text).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=5) #Takes in query embeddings
    
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

chain = LLMChain(llm=llm, prompt=prompt)

def answer_query(query, retrieved_documents):
    documents_json = json.dumps(retrieved_documents, indent=4)
    formatted_prompt = prompt.format(query=query, documents=documents_json)
    response_content = chain.run({"query": query, "documents": documents_json}).strip()
    return response_content

query = "I want a model that can handle multilingual stuff, which one is the best in that case?"

retrieved_documents = query_model(query)

langchain_response = answer_query(query, retrieved_documents)
print("LangChain AI Response:", langchain_response)
