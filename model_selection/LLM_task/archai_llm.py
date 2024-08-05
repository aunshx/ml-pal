import json
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-proj-NvqIphRNzF9iGBurzBy2T3BlbkFJ1yFpMCXSYc2ubsrt8Xh1'

# Load the original data
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
query = "We need to analyze customer reviews for sentiment. Which model demonstrates the highest precision and recall for sentiment analysis?"

response = answer_query(query, context)
print("AI Response:", response)
