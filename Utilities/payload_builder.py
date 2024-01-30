"""
This module provides utility functions for processing JSON input and generating a final payload for O3 Copilot service.
It includes functions for parsing date strings, checking date formats, and processing queries based on the input.

Module Structure:
- parse_date: Parses the given date string into a datetime object or returns None if parsing fails.
- date_format: Checks if the given date string matches the expected format.
- process_query: Processes JSON input and generates a final payload for O3 Copilot service.

Functions:
1. parse_date(date_str): Parses date string into a datetime object.

2. date_format(date): Checks if the date string matches the expected format.

3. process_query(json_input, timeZoneHourDiff): Processes JSON input and generates a final payload.
   - Parameters:
      - json_input (dict): JSON input data.
      - time_zone_hour_diff (int): Time zone hour difference.
   - Returns:
      - dict: Final payload data.

Example Usage:
- Use the process_query function to convert JSON input into a formatted payload for further processing.

Author: Sahil
Date: 24 Nov 2023
"""



from datetime import datetime
import re
class O3CopilotPayloadParser:
    def __init__(self, json_data,time_ZoneHour_Diff):
        self.data = json_data 
        self.timeZoneHourDiff = time_ZoneHour_Diff

    def parse_date(self,date_str):
        
        """
        Parses the given date string into a datetime object.

        Args:
            date_str (str): Date string in the format '%Y-%m-%d %H:%M:%S'.

        Returns:
            datetime or None: Parsed datetime object or None if parsing fails.
        """

        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    def date_format(self,date):
        """
        Checks if the given date string matches the expected format.

        Args:
            date (str): Date string.

        Returns:
            bool: True if the date string matches the format, False otherwise.
        """

        date_format_regex = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
        return re.match(date_format_regex, date) is not None
    # @classmethod
    def process_query(self):
        """
        Processes the JSON input and generates a final payload.

        Args:
            json_input (dict): JSON input data.
            time_zone_hour_diff (int): Time zone hour difference.

        Returns:
            dict: Final payload data.
        """

        json_Input = self.data
        current_datetime = datetime.now()
        data = {
            "intent": None,
            "entity": None,
            "entityName": None,
            "fromdate": None,
            "todate": None,
            "timezonehourdiff": self.timeZoneHourDiff,
            "module": None,
            "type": None,
            "count": None,
            "frequency": None,
            "ischart": None,
            "bestorworst": None,
            "name": None
        }

        if all(json_Input[key].lower() == 'unknown' for key in ['entity', 'entityname', 'intent']):
            data['fromdate'] = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
            data['todate'] = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999).strftime('%Y-%m-%d %H:%M:%S')
            data['entity'] = json_Input['entity']
            data['entityname'] = json_Input['entityname']
            data['intent'] = json_Input['intent']
            return data

        data['entity'] = json_Input['entity']
        data['entityName'] = json_Input['entityname']
        data['intent'] = json_Input['intent']

        if 'chart_type' in json_Input and json_Input['chart_type'] is not None:
            data['ischart'] = json_Input['chart_type']
        if 'type' in json_Input and json_Input['type'] is not None:
            data['type'] = json_Input['type']
            # Check if type is 'list'
            if json_Input['type'] == 'list':
                data['ischart'] = json_Input['type']
        if 'module' in json_Input and json_Input['module'] is not None:
            data['module'] = json_Input['module']
        if 'list' in json_Input and json_Input['list'] is not None:
            data['count'] = json_Input['list']
        if 'frequency' in json_Input and json_Input['frequency'] is not None:
            data['frequency'] = json_Input['frequency']
        if 'kpiname' in json_Input and json_Input['kpiname'] is not None:
            data['name'] = json_Input['kpiname']

        if 'best/' in json_Input['intent'].lower():
            data['bestorworst'] = 'best'
            intent_parts = json_Input['intent'].split('/')
            data['intent'] = "/".join(intent_parts[1:])
        elif 'worst/' in json_Input['intent'].lower():
            data['bestorworst'] = 'worst'
            intent_parts = json_Input['intent'].split('/')
            data['intent'] = "/".join(intent_parts[1:])

        if 'todate' in json_Input and json_Input['todate'] and self.date_format(json_Input['todate']):
            data['todate'] = self.parse_date(json_Input['todate']).strftime('%Y-%m-%d %H:%M:%S')

        if 'fromdate' in json_Input and json_Input['fromdate'] and self.date_format(json_Input['fromdate']):
            data['fromdate'] = self.parse_date(json_Input['fromdate']).strftime('%Y-%m-%d %H:%M:%S')
            if not data['todate']:
                # If 'todate' is not provided, set it to the end of the same day as 'fromdate'
                from_date = datetime.strptime(data['fromdate'], '%Y-%m-%d %H:%M:%S')
                data['todate'] = (from_date.replace(hour=23, minute=59, second=59, microsecond=999999)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            if data['todate']:
                # If only 'todate' is given, set 'fromdate' to the start of the same day
                to_date = datetime.strptime(data['todate'], '%Y-%m-%d %H:%M:%S')
                data['fromdate'] = to_date.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
            else:
                # If neither 'fromdate' nor 'todate' is given, set both to the current day
                data['fromdate'] = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')
                data['todate'] = current_datetime.replace(hour=23, minute=59, second=59, microsecond=999999).strftime('%Y-%m-%d %H:%M:%S')

        return data