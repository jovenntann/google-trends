import os
import json
import requests
import logging
from urllib.parse import quote

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    logger.info('Received event: %s', event)

    serp_url = 'https://serpapi.com/search'
    query_parameters = event.get('queryStringParameters', {})
    query = query_parameters.get('q', '')
    date = query_parameters.get('date', 'today+5-y').replace(' ', '+')
    timezone = query_parameters.get('tz', '-540')
    data_type = query_parameters.get('data_type', 'TIMESERIES')
    geo = query_parameters.get('geo', 'US')
    api_key = os.environ.get('SERP_API_KEY')

    logger.info(date)
    
    url = f"{serp_url}?engine=google_trends&q={quote(query)}&data_type={data_type}&date={date}&tz={timezone}&geo={geo}&api_key={api_key}"
    logger.info('Constructed URL: %s', url)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        logger.info('Request successful. Response data: %s', response_data)
        return {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }
    else:
        logger.error('Request failed with status code: %s. Response text: %s', response.status_code, response.text)
        return {
            'statusCode': response.status_code,
            'body': json.dumps(response.text)
        }