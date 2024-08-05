import json
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import sys
print(sys.path)

print('JNEFNEJFNF')

with open('models_schema.json', 'r') as f:
    json_data = json.load(f)

print('HELLPO')

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the ChromaDB client
client = chromadb.Client(Settings(persist_directory="./chroma"))

# Create a collection for the model index
collection = client.create_collection("model_index")

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

# Example query
query_text = "Which would be the best model to help detecting skirts and blouses?"
result = query_model(query_text)
print('Question :', query_text)
print('Response :', result)
