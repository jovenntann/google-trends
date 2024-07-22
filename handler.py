import os
import json
import logging
from datetime import datetime, timedelta
import math
import yfinance as yf

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f"Event received: {event}")
    logger.info(f"Context received: {context}")

    if event['httpMethod'] == 'GET' and event['path'] == '/status':
        logger.info("Received GET request for /status")
        content = {
            "application": "Generate Report from yFinance Service",
            "status": "OK",
            "environment": os.environ.get('ENV_NAME', 'Unknown')
        }
        logger.info(f"Response content: {content}")
        return {
            'statusCode': 200,
            'body': json.dumps(content)
        }

    elif event['httpMethod'] == 'POST' and event['path'] == '/yfinance':
        body = json.loads(event['body'])
        isins = body['isins']
        tickers = {}

        for isin in isins:
            data = yf.Ticker(isin)
            try:
                tickers[isin] = data.info['symbol']
            except:
                tickers[isin] = 'NONE'

        date = body['date']
        start_date = datetime.strptime(date, '%Y-%m-%d')
        end_date = start_date + timedelta(days=1)
        response = {}

        for ticker in tickers:
            try:
                data = yf.download(tickers[ticker], start=str(start_date.date()), end=str(end_date.date()))
                json_data = json.loads(json.dumps(list(data.T.to_dict().values())))
                json_data = json_data[0]

                if math.isnan(float(json_data['Open'])) or \
                        math.isnan(float(json_data['High'])) or \
                        math.isnan(float(json_data['Low'])) or \
                        math.isnan(float(json_data['Close'])) or \
                        math.isnan(float(json_data['Adj Close'])) or \
                        math.isnan(float(json_data['Volume'])):

                    formatted_data = {}

                else:
                    formatted_data = {
                        'open': json_data['Open'],
                        'high': json_data['High'],
                        'low': json_data['Low'],
                        'close': json_data['Close'],
                        'adj_close': json_data['Adj Close'],
                        'volume': json_data['Volume']
                    }

            except:
                formatted_data = {}

            response[ticker] = formatted_data

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    elif event['httpMethod'] == 'POST' and event['path'] == '/yfinance/filter':
        body = json.loads(event['body'])
        tickers = body['tickers']
        date = body['date']
        start_date = datetime.strptime(date, '%Y-%m-%d')
        end_date = start_date + timedelta(days=1)
        response = {}

        for ticker in tickers:
            try:
                data = yf.download(ticker, start=str(start_date.date()), end=str(end_date.date()))
                json_data = json.loads(json.dumps(list(data.T.to_dict().values())))
                json_data = json_data[0]

                if math.isnan(float(json_data['Open'])) or \
                        math.isnan(float(json_data['High'])) or \
                        math.isnan(float(json_data['Low'])) or \
                        math.isnan(float(json_data['Close'])) or \
                        math.isnan(float(json_data['Adj Close'])) or \
                        math.isnan(float(json_data['Volume'])):

                    formatted_data = {}

                else:
                    formatted_data = {
                        'open': json_data['Open'],
                        'high': json_data['High'],
                        'low': json_data['Low'],
                        'close': json_data['Close'],
                        'adj_close': json_data['Adj Close'],
                        'volume': json_data['Volume']
                    }
            except Exception as e:
                logger.error(e)
                formatted_data = {}

            response[ticker] = formatted_data

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Not Found'})
        }