"""
Module: DataRetriever for O3Copilot

Key Features:
- Data Retrieval: Communicates with API endpoints to fetch necessary data based on given queries.
- Data Processing: Includes methods to process and format data, such as removing null keys from dictionaries.
- Chat History Management: Capable of saving chat history to maintain a record of interactions.
- Error Handling: Provides mechanisms to handle and respond to failed API requests.
- Text Generation: Utilizes a text generator for creating contextually relevant and meaningful responses.

Classes:
- DataRetriever: A class that encapsulates all functionalities related to data retrieval, processing, and management.

Dependencies:
- json: For handling JSON data.
- requests: For making HTTP requests to external APIs.
- GenerativeAI.openai_text_generator: A module providing text generation capabilities, used for crafting responses.
"""

import json
import requests
from GenerativeAI.openai_text_generator import TextGenerator

class DataRetriever():

    def __init__(self):
        super().__init__() 

    def check_existing_queries(self, data):
        """
        Check existing queries by sending a POST request to the specified API endpoint.

        Args:
            data (dict): JSON data to be sent in the request payload.

        Returns:
            dict or str: Response from the API if successful, otherwise an error message.
        """
        response = requests.post(self.GET_CHAT_HISTORY_URL, headers=self.HEADERS,json=data, verify=False)

        if response.status_code // 100 == 2:
            response = json.loads(response.text)
            result = response        
            if result.get('Result') is not None:  # Check if 'Result' is not null
                agent_response = result
                return agent_response
            else:
                return "Data not found"
        else:
            return "Error while hitting API"
    def remove_null_keys(self, d):
        return {k: v for k, v in d.items() if v is not None}
    

    def save_chat_history(self, payload, classifier_classes):
        """
        Save chat history by making a POST request to the specified endpoint.

        Args:
            payload (dict): The payload to send.
            classifier_classes (dict): The classifier classes to serialize and send.

        Returns:
            dict: The classifier classes.
        """

        serialized_json = json.dumps(classifier_classes, indent=4)
        payload['JsonData'] = serialized_json
        response = requests.post(self.SAVE_CHAT_HISTORY_URL, headers=self.HEADERS, json=payload, verify=False)
        return classifier_classes
    
    def handle_failed_response(self, status_code):
        """
        Handle failed API responses.

        Args:
            status_code (int): The status code of the failed response.

        Returns:
            dict: A response indicating failure.
        """

        return {
            'agent_response': "I regret any inconvenience caused. "
                              "I encountered an error while processing new data. "
                              "Please get in touch with the Database Team for assistance. "
                              "Your cooperation is highly valued. Thank you.",
            'Type': "Textual-Answer",
            'status_code':status_code
        }
    
    def generate_kpi_reasoning_answer(self, result, classifier_classes, payload):
        """
        Process text results from the KPI Reasoning Module.

        Args:
            result (dict): The result data to process.
            classifier_classes (dict): The classifier classes.
            payload (dict): The payload data.

        Returns:
            dict: Updated classifier classes.
        """

        if result['Text']:
            filtered_data = [self.remove_null_keys(item) for item in result['Text']]
            text_generate = TextGenerator(self.query, self.BOT_NAME, self.SPECIFIC_MESSAGE)
            answer = text_generate.generate_kpi_reasoning_answer(filtered_data)
            classifier_classes['agent_response'] = answer['agent_response']
            self.save_chat_history(payload, classifier_classes)
        else:
            Text_Generator = TextGenerator(self.query, self.BOT_NAME, self.SPECIFIC_MESSAGE)
            answer = Text_Generator.repharse_answer('No Data in the database', self.no_data_in_db_prompt)
            classifier_classes['agent_response'] = answer['agent_response']
            if 'agent_response' in answer:
                answer.pop('agent_response')
            classifier_classes['Repharasing_Cost'] = answer
        return classifier_classes

    def retrieve_data_from_database(self, classifier_classes, payload):
        """
        Retrieve data from the database.

        Args:
            classifier_classes (dict): The classifier classes.
            payload (dict): The payload data.

        Returns:
            dict: The response data.
        """
        
        try:
            existing_classes = self.check_existing_queries(payload)
            if 'Result' in existing_classes and 'Response' in existing_classes['Result']:
                response = json.loads(existing_classes["Result"]["Response"])
                return response

            payload['Question'] = self.query
            response = requests.post(self.RETRIEVE_DATA_URL, headers=self.HEADERS, json=payload, verify=False)

            if response.status_code // 100 == 2:
                result = response.json()
                if payload['module'] == 'diagnostic':
                    classifier_classes['Type'] = 'Textual-Answer'
                    classifier_classes = self.generate_kpi_reasoning_answer(result, classifier_classes, payload)
                    return classifier_classes
                else:
                    return self.call_values_response_validate(result, classifier_classes, payload)

            else:
                return self.handle_failed_response(response.status_code)

        except Exception as e:
            self.handle_failed_response(response.status_code)
        
