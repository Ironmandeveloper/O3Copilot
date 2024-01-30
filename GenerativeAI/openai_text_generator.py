"""
Module: Text Generation for O3Copilot System

Key Features:
- General Query Response Generation: Generates responses for general manufacturing-related queries.
- KPI Reasoning: Provides detailed explanations and insights into specific KPI data.
- Rephrasing Capabilities: Offers the ability to rephrase or clarify previous responses for better understanding.
- Cost Calculation: Calculates the cost of each API request based on token usage.
- Error Handling: Handles scenarios where token limits are exceeded and prompts for query refinement.

Classes:
- TextGenerator: A core class that integrates many text generation functionalities. It includes methods for 
  generating standard responses, KPI reasoning answers, rephrasing answers, and handling token limit errors.

Usage:
- The class is initialized with a query, bot name, and a specific message for error scenarios.
- Methods within the class call the OpenAI API with customized prompts, tailored for the manufacturing domain.

Dependencies:
- os: For path operations related to reading external prompt files.
- openai: To interact with OpenAI's GPT-3.5-turbo model for text generation.
"""

import os
import openai

# Load prompt engineering template for KPI Values
KPI_Reasoning_Script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'KPI_Reasoning_Script.txt')
with open(KPI_Reasoning_Script_path, "r") as file:
    KPI_Reasoning_Script = file.read()
kpi_prompt = KPI_Reasoning_Script


class TextGenerator:
    def __init__(self, query, bot_name, specific_mesg):
        self.query = query
        self.specific_mesg = specific_mesg
        self.bot_name = bot_name

    def generate_unseen_answer(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a helpful assistant named as {self.bot_name} developed by Obeikan investment group. 
    You are developed by AI Engineers Team at Obeikan Investment Group.
    Your purpose is to give answer related to manufacturing industry quires like plants, lines units/machines and general questions as well.
    I can answer your about particular plant productivity like oee, availability, performance, quality, capacity utilization, waste.
    Also can tell your about particular KPI, like it's target value actual value and RACI matrix as well.
    I also can generate chart and table as well."""
                    },
                    {
                        "role": "user",
                        "content": f"Query: {self.query}"
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response['choices'][0]['message']['content']
            repharse_cost = (response['usage']['prompt_tokens'] / 1000) * 0.0015 + (response['usage']['completion_tokens'] / 1000) * 0.002
            total_token = response['usage']['total_tokens']
            return {
                'agent_response': answer,
                'total_cost_usd': repharse_cost,
                'total_token': total_token,
                'prompt_token': response['usage']['prompt_tokens'],
                'output_token': response['usage']['completion_tokens']
            }
        except:
            return {
                'agent_response':self.specific_mesg,
                'Type':"Textual-Answer"
            }
        

    def generate_kpi_reasoning_answer(self,get_answer):
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"{kpi_prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"{self.query}\ndata:{get_answer}"
                    }
                ],
                temperature=1,
                max_tokens=500,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
                
            answer = response['choices'][0]['message']['content']
            repharse_cost = (response['usage']['prompt_tokens'] / 1000) * 0.0015 + (response['usage']['completion_tokens'] / 1000) * 0.002
            total_token = response['usage']['total_tokens']
            return {
                'agent_response': answer,
                'total_cost_usd': repharse_cost,
                'total_token': total_token,
                'prompt_token': response['usage']['prompt_tokens'],
                'output_token': response['usage']['completion_tokens']
            }
        

        except:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": f"you are a helpful assistant named as {self.bot_name} developed by Obeikan investment group.\nYour encountered error of token limit exceeds. now generate response that limit your query so that i can generate text. my limit is 4000 token\n                        "
                    },
                    {
                    "role": "assistant",
                    "content": "Please limit your query so that i can generate text answer within limit of 4000 token"
                    }
                ],
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response['choices'][0]['message']['content']
            repharse_cost = (response['usage']['prompt_tokens'] / 1000) * 0.0015 + (response['usage']['completion_tokens'] / 1000) * 0.002
            total_token = response['usage']['total_tokens']
            return {
                'agent_response': answer,
                'total_cost_usd': repharse_cost,
                'total_token': total_token,
                'prompt_token': response['usage']['prompt_tokens'],
                'output_token': response['usage']['completion_tokens'],
                'token_error':True
            }
        

    def repharse_answer(self, get_answer, prompt):
        try:
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"{prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"Query: {self.query}\nAnswer:{get_answer}"
                    }
                ],
                temperature=0,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
             
            answer = response['choices'][0]['message']['content']
            repharse_cost = (response['usage']['prompt_tokens'] / 1000) * 0.0015 + (response['usage']['completion_tokens'] / 1000) * 0.002
            total_token = response['usage']['total_tokens']
            return {
                'agent_response': answer,
                'total_cost_usd': repharse_cost,
                'total_token': total_token,
                'prompt_token': response['usage']['prompt_tokens'],
                'output_token': response['usage']['completion_tokens']
            }
        

        except:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                    "role": "system",
                    "content": f"you are a helpful assistant named as {self.bot_name} developed by Obeikan investment group.\nYour encountered error of token limit exceeds. now generate response that limit your query so that i can generate text. my limit is 4000 token\n                        "
                    },
                    {
                    "role": "assistant",
                    "content": "Please limit your query so that i can generate text answer within limit of 4000 token"
                    }
                ],
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response['choices'][0]['message']['content']
            repharse_cost = (response['usage']['prompt_tokens'] / 1000) * 0.0015 + (response['usage']['completion_tokens'] / 1000) * 0.002
            total_token = response['usage']['total_tokens']
            return {
                'agent_response': answer,
                'total_cost_usd': repharse_cost,
                'total_token': total_token,
                'prompt_token': response['usage']['prompt_tokens'],
                'output_token': response['usage']['completion_tokens'],
                'token_error':True
            }

