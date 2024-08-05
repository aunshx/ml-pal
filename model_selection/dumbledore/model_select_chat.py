import json
import os
from langchain_community.embeddings.openai import OpenAIEmbeddings
import chromadb
from chromadb.config import Settings
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains.llm import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from save_memory_chat import MemoryDataSerializer

os.environ['OPENAI_API_KEY'] = 'sk-proj-NvqIphRNzF9iGBurzBy2T3BlbkFJ1yFpMCXSYc2ubsrt8Xh1'

embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")
client = chromadb.Client(Settings(persist_directory="./chroma"))
collection = client.create_collection("model_index")

with open('dd_11/model_list_schema.json', 'r') as f:
    json_data = json.load(f)

model_info_map = {}

for model_type, model_info in json_data.items():
    if isinstance(model_info, dict):
        model_name = model_info.get("model_name", model_type)
        developed_by = model_info.get("developed_by", "")
        model_type_info = model_info.get("model_type", "")
        #licensing = model_info.get("licensing", "")
        #installation = model_info.get("installation", {})
        #python_version = installation.get("python_version", "")
        #additional_libraries = installation.get("additional_libraries", "")
        #installation_command = installation.get("installation_command", "")```
        usage = model_info.get("usage", {})
        #cli_example = usage.get("cli_example", "")
        python_example = usage.get("python_example", "")
        pretrained_models = model_info.get("pretrained_models_and_performance_metrics", {})
        available_models = pretrained_models.get("available_models", "")
        pretrained_datasets = pretrained_models.get("pretrained_datasets", "")
        performance_metrics = pretrained_models.get("performance_metrics", {})
        model_architecture = model_info.get("model_details", {}).get("model_description", "")
        supported_labels = model_info.get("model_details", {}).get("supported_labels", "")
        limitations = model_info.get("limitations_and_biases", {}).get("limitations", "")
        #biases = model_info.get("limitations_and_biases", {}).get("biases", "")
        #risks = model_info.get("limitations_and_biases", {}).get("risks", "")
        recommendations = model_info.get("recommendations", "")
        hardware = model_info.get("compute_infrastructure", {}).get("hardware", "")
        software = model_info.get("compute_infrastructure", {}).get("software", "")
        #model_card_contact = model_info.get("contact_information", {}).get("model_card_contact", "")
        #related_papers_and_resources = model_info.get("references", {}).get("related_papers_and_resources", "")
        sample_code = model_info.get("example_implementation", {}).get("sample_code", "")
        
        text = (f"{model_name} - Developed by: {developed_by} " 
                f"- Python Example: {python_example} - Available Models: {available_models} "
                f"- Pretrained Datasets: {pretrained_datasets} - Performance Metrics: {performance_metrics} "
                f"- Model Architecture: {model_architecture} - Supported Labels: {supported_labels} "
                f"- Limitations: {limitations} "
                f"- Recommendations: {recommendations} - Hardware: {hardware} - Software: {software} "
                f"- Sample Code: {sample_code}")
        
        embedding = embeddings_model.embed_query(text)
       
        collection.add(
            embeddings=[embedding],
            metadatas=[{"description": model_architecture, "type": model_type}],
            ids=[model_name]
        )  
        model_info_map[model_name] = model_info

def query_model(query_text):
    query_embedding = embeddings_model.embed_query(query_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=1)  
    
    if results and results['metadatas']:
        retrieved_documents = []
        for metadata, model_id in zip(results['metadatas'][0], results['ids'][0]):
            model_info = model_info_map.get(model_id, {})
            retrieved_documents.append({
                "model_name": model_id
            })
        return retrieved_documents
    else:
        return []

template = """
Given the model schema for LLM models, you are an AI agent that should be able to answer all the user questions using the document alone.
Keep asking the user questions until you find the perfect match from the document. Suggest the model only in the end until then ask the user questions that you can use to find the best match.

User Query and Context: {query_with_context}
AI Response:
"""


prompt = PromptTemplate(template=template, input_variables=['query_with_context'])

llm = ChatOpenAI(model='gpt-4o')

memory = ConversationBufferMemory()

chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

def answer_query(query, retrieved_documents):
    documents_json = json.dumps(retrieved_documents, indent=4)
    query_with_context = f"User Query: {query} Retrieved Documents: {documents_json}"
    response_content = chain.run({"query_with_context": query_with_context}).strip()
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