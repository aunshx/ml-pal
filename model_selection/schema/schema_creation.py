import json
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
import os

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-proj-NvqIphRNzF9iGBurzBy2T3BlbkFJ1yFpMCXSYc2ubsrt8Xh1'

# Load the original data
with open('model_selection/model_list.json', 'r') as infile:
    original_data = json.load(infile)

# Define the prompt template
template = """
Given the model specifications for LLM models, transform each model into a unified schema and provide the transformed JSON.

Original JSON:
{context}

{{
    "model_name": "<Model Name>",
    "model_architecture": "<Model Architecture>",
    "training_objective": "<Training Objective>",
    "parameters": "<Parameters>",
    "primary_use_case": "<Primary Use Case>",
    "performance_metrics": "<Performance Metrics>",
    "training_data": "<Training Data>",
    "inference_speed": "<Inference Speed>",
    "memory_compute_requirements": "<Memory and Compute Requirements>",
    "fine_tuning_capability": "<Fine-Tuning Capability>",
    "bias_fairness": "<Bias and Fairness>",
    "model_size": "<Model Size>",
    "licensing": "<Licensing>",
    "advantages": "<Advantages>"
}}
"""



prompt = PromptTemplate(template=template, input_variables=['context'])


llm = ChatOpenAI(model='gpt-4o')


chain = LLMChain(llm=llm, prompt=prompt)

transformed_models = {}

for model_name, model_data in original_data.items():
    context = json.dumps({model_name: model_data}, indent=4)
    formatted_prompt = prompt.format(context=context)
    response_content = chain.run(context=context).strip()

    # Find the JSON part in the response content
    start_idx = response_content.find('{')
    end_idx = response_content.rfind('}') + 1

    if start_idx != -1 and end_idx != -1:
        json_str = response_content[start_idx:end_idx]
        try:
            transformed_json = json.loads(json_str)
            transformed_models[model_name] = transformed_json
        except json.JSONDecodeError:
            transformed_models[model_name] = response_content
    else:
        print(f"Could not find JSON structure for model {model_name}:")
       

with open('model_selection/schema/model_list_schema.json', 'w') as outfile:
    json.dump(transformed_models, outfile, indent=4)

print("Combined transformed schema saved to model_list_schema.json")
