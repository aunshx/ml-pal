import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load the original JSON file
with open('models.json', 'r') as infile:
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

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key='AIzaSyCPTjKCLXLnW3ssrCDXTeLgWeFhhUSnJtM')
transformed_models = {}

# Process each model in the original JSON
for model_name, model_data in original_data.items():

    context = json.dumps({model_name: model_data}, indent=4)
    formatted_prompt = prompt.format(context=context)
    response = llm.invoke(formatted_prompt)
 
    print(f"Response Content for model {model_name}:")
    print(response.content)
    
   
    if model_name not in transformed_models:
        transformed_models[model_name] = []
    transformed_models[model_name].append(response.content)

with open('unified_schema_models.json', 'w') as outfile:
    json.dump(transformed_models, outfile, indent=4)
print("Combined transformed schema saved to unified_schema_models.json")
