import requests
from bs4 import BeautifulSoup
import json

data = {}

urls = [
    'https://huggingface.co/openai-community/gpt2',
    'https://huggingface.co/openai-community/openai-gpt',
    'https://huggingface.co/meta-llama/Meta-Llama-3-8B',
    'https://huggingface.co/meta-llama/Llama-2-7b',
    'https://huggingface.co/meta-llama/CodeLlama-70b-Instruct-hf',
    'https://huggingface.co/google-bert/bert-base-uncased',
    'https://huggingface.co/FacebookAI/roberta-base',
    'https://huggingface.co/google-t5/t5-base',
    'https://huggingface.co/bigscience/bloom',
    'https://huggingface.co/xlnet/xlnet-base-cased',
    'https://huggingface.co/mistralai/Mixtral-8x7B-v0.1',
    'https://huggingface.co/distilbert/distilbert-base-uncased',
    'https://huggingface.co/google/gemma-2-9b',
    'https://huggingface.co/google/gemma-2-27b-it',
    'https://huggingface.co/Salesforce/codegen-350M-multi'
    ]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for link in urls:
    try:
        response = requests.get(link, headers=headers)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        model_name = link.split('/')[-1]
        data[model_name] = {}

        model_overview = soup.find('div', class_='model-card-content')
        data[model_name]["Model Overview"] = model_overview.get_text(strip=True) if model_overview else 'N/A'

        sections = soup.find_all('section', class_='section')

        for section in sections:
            title = section.find('h2').get_text(strip=True) if section.find('h2') else 'Unknown Section'
            content = section.get_text(strip=True)
            data[model_name][title] = content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {link}: {e}")
        data[model_name] = {"Model Overview": 'Error fetching data'}

with open('LLM_task/LLM_models_overview.json', 'w') as file:
    json.dump(data, file, indent=4)
