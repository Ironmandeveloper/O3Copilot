"""
The Config class is designed to manage configuration settings for a chatbot application.

Key Features:
- Initializes common HTTP headers for API requests.
- Provides a specific message template for budget-related responses.
- Loads important configuration details like bot name and API endpoints from a JSON file.

Author: [Muhammad Sahil]
Date: [29 Dec 2024]
"""

import json
class Config:
    def __init__(self, config_file='config.json') -> None:
        self.HEADERS = {'Content-Type': 'application/json'}
        self.SPECIFIC_MESSAGE = "I think you are out of budget. I kindly request you to check your credit. Your cooperation is greatly appreciated."
        with open(config_file, 'r') as file:
            config_data = json.load(file)
            self.BOT_NAME = config_data.get('BOT_NAME')
            self.GET_CHAT_HISTORY_URL = config_data.get('GET_CHAT_HISTORY_URL')
            self.RETRIEVE_DATA_URL = config_data.get('RETRIEVE_DATA_URL')
            self.SAVE_CHAT_HISTORY_URL = config_data.get('SAVE_CHAT_HISTORY_URL')
