
import json

from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
import os

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-proj-NvqIphRNzF9iGBurzBy2T3BlbkFJ1yFpMCXSYc2ubsrt8Xh1'

# Load the original data
with open('LLM_task/LLM_models_schema.json', 'r') as infile:
    original_data = json.load(infile)

# Define the prompt template
template = """
Given the following model specifications in JSON format, transform each model into a unified schema and provide the transformed JSON.

Original JSON:
{context}

{{
    "model_name": "<Model Name>",
    "developed_by": "<Developed By>",
    "model_type": "<Model Type>",
    "licensing": "<Licensing>",
    "installation": {{
        "python_version": "<Python Version>",
        "additional_libraries": "<Additional Libraries>",
        "installation_command": "<Installation Command>"
    }},
    "usage": {{
        "cli_example": "<CLI Example>",
        "python_example": "<Python Example>"
    }},
    "pretrained_models_and_performance_metrics": {{
        "available_models": [
            "<Available Models>"
        ],
        "pretrained_datasets": [
            "<Pretrained Datasets>"
        ],
        "performance_metrics": {{
            "example_metrics_table": [
                {{
                    "model": "<Model>",
                    "size_pixels": "<Size (pixels)>",
                    "map_val50_95": "<mAPval50-95>",
                    "speed_cpu_onnx_ms": "<SpeedCPU ONNX (ms)>",
                    "speed_a100_tensorrt_ms": "<SpeedA100 TensorRT (ms)>",
                    "params_m": "<Params (M)>",
                    "flops_b": "<FLOPs (B)>"
                }}
            ]
        }}
    }},
    "model_details": {{
        "model_description": "<Model Description>",
        "supported_labels": [
            "<Supported Labels>"
        ]
    }},
    "limitations_and_biases": {{
        "limitations": [
            "<Limitations>"
        ],
        "biases": [
            "<Biases>"
        ],
        "risks": [
            "<Risks>"
        ]
    }},
    "recommendations": [
        "<Recommendations>"
    ],
    "compute_infrastructure": {{
        "hardware": "<Hardware>",
        "software": "<Software>"
    }},
    "contact_information": {{
        "model_card_contact": "<Model Card Contact>"
    }},
    "references": {{
        "related_papers_and_resources": [
            "<Related Papers and Resources>"
        ]
    }},
    "example_implementation": {{
        "sample_code": "<Sample Code>"
    }}
}}
"""

prompt = PromptTemplate(template=template, input_variables=['context'])

# Initialize the OpenAI LLM
llm = ChatOpenAI(model='gpt-4')

# Initialize the LLMChain with the LLM and prompt
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
            print(f"Error decoding JSON for model {model_name}:")
            print(response_content)
            transformed_models[model_name] = response_content
    else:
        print(f"Could not find JSON structure for model {model_name}:")
        print(response_content)

with open('LLM_task/LLM_models_schema.json', 'w') as outfile:
    json.dump(transformed_models, outfile, indent=4)

print("Combined transformed schema saved to models_schema.json")
