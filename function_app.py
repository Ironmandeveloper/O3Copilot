"""
Azure Functions Module for O3 Copilot Chatbot

This module implements an Azure Functions app to provide endpoints for the O3 Copilot chatbot. 
It includes functionalities for handling HTTP requests, processing chatbot queries, and managing 
responses. The app supports both production and testing environments with respective endpoints.

Main components:
- `app`: An Azure Function App with anonymous authentication, serving as the entry point for HTTP requests.
- `ENDPOINTS`: A dictionary defining the available endpoints for production and testing purposes.
- `get_response`: A utility function to generate standardized HTTP responses with JSON content.
- `handle_post_request`: A function to process POST requests, validate input, and invoke the O3 Copilot class for query interpretation.
- `o3copilot_production`: The endpoint function for O3 Copilot in production, handling GET and POST requests.

Author: Sahil
Date: 19 Nov 2023
"""



import json
import azure.functions as func
from o3_copilot import O3Copilot

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)




ENDPOINTS = {
    "production": "/api/o3chatbot",
}

def get_response(message, status_code=200):
    """
    Generates an HTTP response with the provided message and status code.

    Args:
        message (str): Response message.
        status_code (int): HTTP status code.

    Returns:
        func.HttpResponse: HTTP response object.
    """
    response_data = {
        "message": message,
        "version": "1.0",
        "endpoints": ENDPOINTS
    }
    return func.HttpResponse(
        body=json.dumps(response_data),
        mimetype="application/json",
        status_code=status_code
    )


def handle_post_request(req, db_tool_class):
    """
    Handles the POST request by extracting JSON payload, validating parameters,
    and invoking the database tool for query interpretation.

    Args:
        req (func.HttpRequest): HTTP request object.
        db_tool_class (class): Database tool class for query interpretation.
 
    Returns:
        func.HttpResponse: HTTP response object.
    """
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON payload", status_code=400)

    query = req_body.get('query')
    timeZoneHourDiff = req_body.get('timeZoneHourDiff')

    if not query or timeZoneHourDiff is None:
        return func.HttpResponse("Missing required parameters", status_code=400)

    return db_tool_class(query, timeZoneHourDiff).query_interpreter()

@app.route(route="o3chatbot")
def o3copilot_production(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function endpoint for O3 Copilot Production.

    Args:
        req (func.HttpRequest): HTTP request object.

    Returns:
        func.HttpResponse: HTTP response object.
    """
    if req.method == 'GET':
        return get_response("Welcome to O3 Copilot Production Endpoint")

    if req.method == 'POST':
        result = handle_post_request(req, O3Copilot)
        return func.HttpResponse(
            body=json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
    else:
        return get_response("Only Post Method Allowed!", status_code=406)

