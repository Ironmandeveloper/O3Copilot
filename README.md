Azure Functions Module for O3 Copilot Chatbot
This project contains an Azure Functions module designed to serve as a backend for the O3 Copilot chatbot. It provides essential functionalities for handling HTTP requests, processing queries, and managing responses. The module supports different environments, including production and testing, with dedicated endpoints for each.

Key Components:
    main.py
    o3_copilot.py

    Classification
        classifier.py  
        prompts.yaml
    BotConfiguration
        config.json  
        config.py
    Database
        data_retriever.py

    GenerativeAI
        KPI_Reasoning_Script.txt
        openai_text_generator.py
    Utilities
        label_search.py
        payload_builder.py
        prompts.py
        response_validate.py



Clone the Repository:
Clone this repository to your local machine or development environment.

Install Dependencies:
Ensure you have Azure Functions Core Tools and Python installed. Install required Python packages using:

Copy code
pip install -r requirements.txt
Configure Azure Functions:
Set up an Azure Functions environment. You can use Azure Portal or Azure CLI for deployment.

Debugging:
Press F5 after installing azure function extentions in VS Code for debugging.

Deploy the Function App:
Deploy the function app to your Azure account. Configure the function app settings according to your requirements.

Usage
Production Endpoint:
Send a GET request to /api/o3chatbot to receive a welcome message.
Send a POST request with a JSON payload containing query and timeZoneHourDiff to receive a response from the O3 Copilot chatbot.



Author
Sahil
Date: 19 Nov 2023

Note: Ensure that you have the necessary permissions and configurations set up in Azure to deploy and run this module. Also, the O3Copilot class and other dependencies should be properly defined and imported in your project for this module to function correctly.