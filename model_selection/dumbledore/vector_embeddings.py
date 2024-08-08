import json
import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
import getpass

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


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

    text = f"{model_name} - {model_overview} - {model_details} - {model_architecture}"
    embedding = embeddings.embed_query(text)
       
    vector_store.add_documents([
        Document(
            page_content=text,
            metadata={"description": model_installation, "type": model_type},
        )
    ])
    model_info_map[model_name] = model_info