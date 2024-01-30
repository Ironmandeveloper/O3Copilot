import json
import requests
from Utilities.prompts import Prompts
from GenerativeAI.openai_text_generator import TextGenerator

class ResponseValidator(Prompts):
    def __init__(self):
        super().__init__() 

    def update_type(self, data):
            for item in data:
                if 'Type' in item:
                    if item['Type'] == 'Actual':
                        item['Type'] = 'Actual Value'
                    elif item['Type'] == 'Glidepath':
                        item['Type'] = 'Target Value'

            return data

    def process_text_response(self, result, classifier_classes, new_payload):
        self.update_type(result['Text'])
        classifier_classes['Type'] = 'Textual-Answer'
        text_generator = TextGenerator(self.query, self.BOT_NAME, self.SPECIFIC_MESSAGE)
        answer = text_generator.repharse_answer(result['Text'], self.PROMPTS['data_access_prompt'])
        classifier_classes['agent_response'] = answer['agent_response']
        if 'agent_response' in answer:
            answer.pop('agent_response')
        classifier_classes['Repharasing_Cost'] = answer
        if all(new_payload[key].lower() == 'unknown' for key in ['entity', 'entityname', 'intent']):
            return classifier_classes
        if 'token_error' in answer and answer['token_error']:
            return classifier_classes
        else:
            serialized_json = json.dumps(classifier_classes, indent=4)
            new_payload['JsonData'] = serialized_json
            response = requests.post(self.SAVE_CHAT_HISTORY_URL, headers=self.HEADERS, json=new_payload, verify=False)
            return classifier_classes
        
    def process_chart_list_response(self, result, classifier_classes, new_payload):
        self.update_type(result['Chart'])
        classifier_classes['Type'] = 'chart/list'
        classifier_classes['chart_type'] = new_payload['ischart']
        classifier_classes['module'] = result['Module']
        classifier_classes['agent_response'] = result['Chart']
        serialized_json = json.dumps(classifier_classes, indent=4)
        new_payload['JsonData'] = serialized_json
        response = requests.post(self.SAVE_CHAT_HISTORY_URL, headers=self.HEADERS, json=new_payload, verify=False)
        return classifier_classes

    def process_chart_response(self, result, classifier_classes, new_payload):
        self.update_type(result['Chart'])
        if new_payload['ischart']:
            classifier_classes['Type'] = 'chart'
            classifier_classes['chart_type'] = new_payload['ischart']
        else:
            classifier_classes['Type'] = 'chart'
            classifier_classes['chart_type'] = new_payload['type']
        classifier_classes['module'] = result['Module']
        classifier_classes['agent_response'] = result['Chart']
        serialized_json = json.dumps(classifier_classes, indent=4)
        new_payload['JsonData'] = serialized_json
        response = requests.post(self.SAVE_CHAT_HISTORY_URL, headers=self.HEADERS, json=new_payload, verify=False)
        return classifier_classes

    def process_list_response(self, result, classifier_classes, new_payload):
        self.update_type(result['List'])
        if new_payload['ischart']:
            classifier_classes['Type'] = 'list'
            classifier_classes['chart_type'] = new_payload['ischart']
        else:
            classifier_classes['Type'] = 'list'
            classifier_classes['chart_type'] = new_payload['type']
        classifier_classes['module'] = result['Module']
        classifier_classes['agent_response'] = result['List']
        serialized_json = json.dumps(classifier_classes, indent=4)
        new_payload['JsonData'] = serialized_json
        response = requests.post(self.SAVE_CHAT_HISTORY_URL, headers=self.HEADERS, json=new_payload, verify=False)
        return classifier_classes

    def process_no_data_response(self, message, classifier_classes, prompt):
        classifier_classes['Type'] = 'Textual-Answer'
        text_generator = TextGenerator(self.query, self.bot_name, self.specific_message)
        answer = text_generator.repharse_answer(message, prompt)
        classifier_classes['agent_response'] = answer['agent_response']
        if 'agent_response' in answer:
            answer.pop('agent_response')
        classifier_classes['Repharasing_Cost'] = answer
        return classifier_classes
    
    def call_values_response_validate(self, result, classifier_classes, new_payload):
        if result['Text'] is not None:
            return self.process_text_response(result, classifier_classes, new_payload)
        
        elif result['Chart'] is not None and result['List'] is not None:
            return self.process_chart_list_response(result, classifier_classes, new_payload)
        
        elif result['Chart'] is not None:
            return self.process_chart_response(result, classifier_classes, new_payload)
        
        elif result['List'] is not None:
            return self.process_list_response(result, classifier_classes, new_payload)
        
        elif not any([result['Text'], result['Chart'], result['List'], result['IsError']]):
            return self.process_no_data_response(
                'There is no Record against these entities in the Database.',
                classifier_classes,
                self.data_access_prompt
            )
        
        elif all([result[key] is None for key in ['Text', 'Chart', 'List']]):
            return self.response_validator.process_no_data_response(
                'Your Query is incomplete!',
                classifier_classes,
                self.query_incomplete_prompt
            )


