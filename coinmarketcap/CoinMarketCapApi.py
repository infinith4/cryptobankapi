#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

class CoinMarketCapApi:

    def __init__(self, apiKey: str):
        self.base_url = "https://sandbox-api.coinmarketcap.com" #"https://pro-api.coinmarketcap.com"
        self.apiKey = apiKey
        #self.secretKey = secretKey
    
    def get_listing(self):
        url = f'{self.base_url}/v1/cryptocurrency/listings/latest'
        parameters = {
        'start':'1',
        'limit':'5000',
        'convert':'USD'
        }
        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': self.apiKey,
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(data)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)