"""
O3Copilot Module

This module is designed  for the O3Copilot system, an assistant bot developed for Obeikan Group. 
Enabling seamless access to Obeikan Group's real-time data through natural language interactions. It diligently interprets user queries, orchestrates data retrieval from various sources, and constructs informative responses, empowering users with timely insights and actions.

Key Functionalities:
Query Understanding: Analyzes user queries to extract key information, intent, and data requirements.
Data Integration: Effortlessly interacts with multiple databases to retrieve various data types, including productivity values, graphs, and KPIs.
Response Tailoring: Crafts informative responses that effectively address user needs, encompassing text, visualizations, and data tables.
Adaptability: Leverages a combination of custom-built classifiers and generative AI to handle diverse query types, ensuring comprehensive and relevant answers.
Error Resilience: Gracefully manages exceptions to provide informative feedback, ensuring a smooth user experience.

Key Components:
Response Validation
Database Retriever
Classifiers
Payload Builder
Generative AI

Environment:
Securely manages configuration settings using dotenv for enhanced privacy and protection.
"""

import json
from dotenv import load_dotenv

from Utilities.response_validate import ResponseValidator
from Database.data_retriever import DataRetriever

from Utilities.label_search import LabelSearch
from GenerativeAI.openai_text_generator import TextGenerator
from Utilities.payload_builder import O3CopilotPayloadParser
from Classification.classifier import ProdGraphClassifier, ProdValueClassifier, KPIValueClassifier

# Load environment variables from .env file
load_dotenv()

class O3Copilot(ResponseValidator, DataRetriever):
    """
    An assistant bot that provides access to Obeikan Group's real-time data.

    Args:
        query (str): The user's query.
        timeZoneHourDiff (int): The user's timezone hour difference.
    """

    def __init__(self, query, timeZoneHourDiff):
        super().__init__()
        self.query = query
        self.timeZoneHourDiff = timeZoneHourDiff

    def classification_results(self, query, classifier):
        """
        Classifies the user's query using the specified classifier.

        Args:
            query (str): The user's query.
            classifier (Classifier): The classifier to use.

        Returns:
            dict: A dictionary containing the classification results.
        """
        try:
            classifier_classes = classifier.ClassifyInput(query)
            return classifier_classes
        except Exception as e:
            return {
                        'agent_response':self.SPECIFIC_MESSAGE,
                        'Type':"Textual-Answer"
                    }

    def prepare_payload(self, response_data):
        """Prepare payload from the response data."""
        json_input = json.loads(response_data['agent_response'])
        json_input = {key.lower(): value for key, value in json_input.items()}
        parser = O3CopilotPayloadParser(json_input, self.timeZoneHourDiff)
        return parser.process_query()
    
    def call_database_module(self, classifier_name, payload_type=None, payload_module=None):
        """Call the specified database module based on the classifier and payload details."""

        classifier_classes = self.classification_results(self.query, classifier_name)
        if 'agent_response' in classifier_classes and classifier_classes['agent_response'] == self.SPECIFIC_MESSAGE:
            return classifier_classes
        payload = self.prepare_payload(classifier_classes)
        if payload_type == 'text':
            payload['type'] = 'text'
        elif payload_module == 'productivity':
            payload['module'] = 'productivityy'
        return self.retrieve_data_from_database(classifier_classes, payload)

    def call_prod_values_api(self):
        """Call the productivity values API/Module."""
        return self.call_database_module(ProdValueClassifier, payload_type='text')

    def call_prod_graph_api(self):
        """Call the productivity graph API/Module."""
        return self.call_database_module(ProdGraphClassifier, payload_module='productivity')

    def call_kpi_values_api(self):
        """Call the KPI API/Module."""
        return self.call_database_module(KPIValueClassifier)

    def query_interpreter(self):
        common_label = ['kpi','plant', 'line', 'unit','machine','availability', 'olp', 'opf', 'opi', 'otf', 'orp', 'ocp', 'ots', 'ogc', 'off', 'assembly', 'assembly-osc-osd', 'binding', 'caps', 'cbob-caps', 'coating', 'cutting', 'design', 'diemaking', 'eai', 'electrical', 'flexo', 'hdpe', 'inspection', 'krones', 'lamination', 'mechanical', 'moulding', 'ome', 'operational', 'packaging-osc-osd', 'planning', 'preforms', 'prepress', 'printing', 'quality', 'quality-checklist', 'roto', 'safety', 'sales', 'sheeter', 'shipping', 'slitting', 'sorting', 'stripping', 'tubeline', 'utilities', 'utilitiesfilm', 'utilitiesflex', 'utility', 'warehouse', 'warping', 'wearhouse', 'weaving', 'workshop', 'availability', 'availability-checklist', 'waste', 'waste-checklist', 'ahu01', 'ahu02', 'ahu03', 'ahu04', 'ahu05', 'ahu06', 'ahu-1', 'ahu-10', 'ahu-11', 'ahu-2', 'ahu-3', 'ahu-4', 'ahu-5', 'ahu-6', 'ahu-7', 'ahu-8', 'ahu-9', 'alkaline', 'ashe', 'asitrade', 'assembly-01', 'assembly-02', 'bag', 'bhs', 'breyer', 'cbob-osc', 'cbob-osd', 'cdi', 'cfm-2', 'cfm-3', 'chm', 'chrome', 'comexi', 'copper-4', 'copper-5', 'core', 'corrugated', 'creasing', 'ctp', 'cylinder', 'daiten', 'dcm', 'dechrome', 'degreasing-2', 'degreasing-3', 'design', 'diemaking', 'eai', 'engraving-1', 'engraving-2', 'engraving-3', 'erector', 'er-we-pa', 'exposure-1', 'exposure-2', 'forklift', 'glue', 'gma-2', 'gma-3', 'gma-4', 'gma-5', 'heidelberg', 'hocker', 'hpx', 'hugobeck-1', 'hugobeck-2', 'husky-1', 'husky-2', 'im_03', 'im_04', 'im_05', 'im_07', 'im_08', 'im_09', 'im_10', 'im_11', 'im_12', 'im_13', 'jkampf', 'kba-105', 'kba-a', 'kba-b', 'kba-c', 'kba-x', 'krones1', 'krones2', 'krones3', 'krones4', 'krones5', 'krones6', 'label', 'lining', 'lithoman-1', 'lithoman-2', 'long-ming', 'mbo-2', 'mbo-3', 'mechanical', 'menzel', 'misomex', 'nexus', 'ome', 'pallets', 'pasaban', 'pet001', 'pet002', 'pet003', 'pet004', 'plates', 'plc', 'pma', 'polar', 'proofing-1', 'proofing-2', 'proslit', 'quality-documents', 'renze', 'resin', 'rewinder-1', 'rewinder-2', 'robank', 'rotomec', 'sales', 'shipping', 'sleeve', 'sorting', 'spanex', 'spiral', 'stahl', 'stretch', 'tcx', 'techne-05', 'techne-06', 'techne-07', 'techne-08', 'techne-09', 'techne-11', 'techne-13', 'techne-15', 'techne-16', 'texa', 'tray', 'tubeline', 'txr', 'uniloy-01', 'uniloy-02', 'uniloy-03', 'uniloy-04', 'uteco', 'warehouse', 'washrooms', 'wearhouse', 'wireing', 'wohlenberg-1', 'wohlenberg-2', 'workshop', 'availability-documents', 'waste-documents','actual value', 'target value', 'gap analysis','raci matrix','raci','responsible','accountable','consulted','informed','closed action plan','closed action plan','open action plan', 'complete action plan', 'reopened action plan', 'delay action plan', 'delayed action plan', 'in progress action plan','closed','open','complete','reopened','delay','delayed','in progress','action plan']
        graph_labels = ['table','list', 'display', 'graph', 'plot', 'chart', 'trend', 'pie', 'histogram', 'line graph', 'bar chart', 'pie chart', 'scatter plot', 'area chart', 'heatmap', 'visualize', 'visualization','analysis','comparison']
        prod_labels = ['capacity utilization', 'quality', 'overall equipment effectiveness', 'oee','machine', 'performance', 'waste','availability']
        kpi_labels = ['actual', 'target','kpi','actual value', 'target value', 'gap analysis','raci matrix','raci','responsible','accountable','consulted','informed','closed action plan','closed action plan','open action plan', 'complete action plan', 'reopened action plan', 'delay action plan', 'delayed action plan', 'in progress action plan','closed','open','complete','reopened','delay','delayed','in progress','action plan','kpi']
        
        common_label_search = LabelSearch(common_label)
        common_matching_words = common_label_search.search(self.query)
        if common_matching_words:
            # logging.info('Common Label')
            graph_label = LabelSearch(graph_labels)
            graph_matching_words = graph_label.search(self.query)

            if graph_matching_words:
                # logging.info('is graph')
                prod_graph_label = LabelSearch(prod_labels)
                prod_matching_words = prod_graph_label.search(self.query)

                if prod_matching_words:
                    # logging.info('prod_graph')
                    GetPlantProductivityGraph = self.call_prod_graph_api()
                    return GetPlantProductivityGraph
                else:
                    kpi_graph_label = LabelSearch(kpi_labels)
                    kpi_matching_words = kpi_graph_label.search(self.query)
                    if kpi_matching_words:
                        # logging.info('kpi graph')
                        GetPlantKPI = self.call_kpi_values_api()
                        return GetPlantKPI
            else:  
                # logging.info('not graph')
                prod_value_label = LabelSearch(prod_labels)
                value_matching_words = prod_value_label.search(self.query)
                if value_matching_words:
                    # logging.info('prod_value')
                    GetPlantProductivity = self.call_prod_values_api()
                    return GetPlantProductivity
                else:
                    kpi_value_label = LabelSearch(kpi_labels)
                    kpi_matching_words = kpi_value_label.search(self.query)
                    if kpi_matching_words:
                        # logging.info('kpi Value')
                        GetPlantKPI = self.call_kpi_values_api()
                        return GetPlantKPI
                    else:
                        # logging.info('call general api')
                        classifier_classes = {}
                        classifier_classes['Type'] = 'Textual-Answer'

                        Text_Generator = TextGenerator(self.query, self.BOT_NAME, self.SPECIFIC_MESSAGE)
                        answer = Text_Generator.generate_unseen_answer()

                        classifier_classes['agent_response'] = answer['agent_response']
                        if 'agent_response' in answer:
                            answer.pop('agent_response')

                        classifier_classes['Repharasing_Cost'] = answer
                        return classifier_classes
        else:
            classifier_classes = {}
            classifier_classes['Type'] = 'Textual-Answer'
            Text_Generator = TextGenerator(self.query, self.BOT_NAME, self.SPECIFIC_MESSAGE)
            answer = Text_Generator.generate_unseen_answer()
            classifier_classes['agent_response'] = answer['agent_response']
            if 'agent_response' in answer:
                answer.pop('agent_response')

            classifier_classes['Repharasing_Cost'] = answer
            return classifier_classes
    