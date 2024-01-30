"""
This module contains classifiers for processing and classifying queries related to productivity values,
productivity graphs and lists, and KPI values. It leverages the LangChain framework with the GPT-4 model
from OpenAI to generate responses based on provided query prompts.

Key Components:
- Load environment variables and prompt templates.
- Initialize LangChain with the GPT-4 model.
- Define classifiers for different types of productivity and KPI queries.

Classes:
- ProdValueClassifier: Classifies input queries for productivity values.
- ProdGraphClassifier: Classifies input queries for productivity graphs and lists.
- KPIValueClassifier: Classifies input queries for KPI values.

This module also initializes the LangChain framework, loads necessary prompt engineering templates from files,
and configures the GPT-4 model for use in the classifiers.

Note: Ensure that environment variables, especially OPENAI_API_KEY, are properly set before using this module.

Author: Sahil
Date: 19 Nov 2023
"""


import os
import yaml
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

# Load environment variables from .env file
load_dotenv()

# Open the YAML file and read its content
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prompts.yaml')
with open(path, 'r') as file:
    data = yaml.safe_load(file)

prod_values_prompt_template = data["Prod_Values_Prompt_Engg_Template"]
prod_graph_prompt_template = data["Prod_Graph_Prompt_Engg_Template"]
kpi_graph_prompt_template = data["KPI_Combine_prompt"]


# LLM declaration
llm = ChatOpenAI(
    openai_api_key=os.environ['OPENAI_API_KEY'],  # platform.openai.com
    temperature=0,
    # verbose=True,
    model_name="gpt-4"
)

# Productivity Textual Answer Classifier
class ProdValueClassifier:
    @staticmethod
    def ClassifyInput(query=""):
        """
        Classifies the input query for productivity values.

        Args:
            query (str): Input query.

        Returns:
            dict: Classification result with agent response and cost details.
        """
        template = prod_values_prompt_template
        prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )

        prompt.format(query=query)
        with get_openai_callback() as cb:
            o3hub_chain = LLMChain(llm=llm, prompt=prompt)
            o3hub_response = o3hub_chain.run(query)
            total_tokens = cb.total_tokens  
            prompt_tokens = cb.prompt_tokens 
            completion_tokens = cb.completion_tokens  
            total_cost = cb.total_cost

        return {
            "agent_response": o3hub_response,
            "Classification_Cost":{
                                    "total_tokens": total_tokens,
                                    "prompt_tokens": prompt_tokens,
                                    "completion_tokens": completion_tokens,
                                    "total_cost_usd": total_cost
                                }
        }


# Productivity Graph and List Classifier
class ProdGraphClassifier:
    @staticmethod
    def ClassifyInput(query=""):
        """
        Classifies the input query for productivity graph and lists.

        Args:
            query (str): Input query.

        Returns:
            dict: Classification result with agent response and cost details.
        """
        template = prod_graph_prompt_template
        prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )

        prompt.format(query=query)
        with get_openai_callback() as cb:
            o3hub_chain = LLMChain(llm=llm, prompt=prompt)
            o3hub_response = o3hub_chain.run(query)
            total_tokens = cb.total_tokens  
            prompt_tokens = cb.prompt_tokens  
            completion_tokens = cb.completion_tokens  
            total_cost = cb.total_cost

        
        classification_cost = {
            "total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_cost_usd": total_cost
        }
        # return o3hub_response
        return {
            "agent_response": o3hub_response,
            "Classification_Cost":classification_cost
        }

# KPI Textual Answer Classifier
class KPIValueClassifier:
    @staticmethod
    def ClassifyInput(query=""):
        """
        Classifies the input query for KPI values.

        Args:
            query (str): Input query.

        Returns:
            dict: Classification result with agent response and cost details.
        """
        template = kpi_graph_prompt_template
        prompt = PromptTemplate(
            input_variables=["query"],
            template=template
        )

        prompt.format(query=query)
        with get_openai_callback() as cb:
            o3hub_chain = LLMChain(llm=llm, prompt=prompt)
            o3hub_response = o3hub_chain.run(query)
            total_tokens = cb.total_tokens  
            prompt_tokens = cb.prompt_tokens  
            completion_tokens = cb.completion_tokens  
            total_cost = cb.total_cost

        
        classification_cost = {
            "total_tokens": total_tokens,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_cost_usd": total_cost
        }
        # return o3hun_response
        return {
            "agent_response": o3hub_response,
            "Classification_Cost":classification_cost
        }