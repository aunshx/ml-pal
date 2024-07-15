import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.Client(Settings(persist_directory="./chroma"))

collection = client.create_collection("model_index")

with open('gemini_schema/unified_schema_models.json', 'r') as f:
    json_data = json.load(f)

model_info_map = {}
for model_type, model_list in json_data.items():
    for model_info in model_list:
        model_name = model_info["model_name"]
        model_description = model_info["model_details"]["model_description"]
        model_installation = model_info["example_implementation"]
        text = f"{model_name} - {model_description} - {model_installation}"
        embedding = model.encode(text).tolist()
        collection.add(
            embeddings=[embedding],
            metadatas=[{"description": model_description, "type": model_type}],
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
        response = f"The best model for the query for this task is {model_name} from the category {model_type}. It is described as: {model_description}. To use this model you can look at the followining instructions {model_installation}."
        return response
    else:
        return "No relevant model found for the query."

# Example query
query_text = "best ML model to segment thermal images"
result = query_model(query_text)
print(result)
