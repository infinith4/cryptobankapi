#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hmac
import hashlib
import json
import requests
import time

from pprint import pprint

#https://github.com/kmn/coincheck/blob/master/coincheck/order.py

class CoinCheckApi:
    def __init__(self, apiKey:str, secretKey:str):
        self.base_url = "https://coincheck.com/api"
        self.API_KEY = apiKey
        self.SECRET_KEY = secretKey

    def get_nonce(self):
        return str(int(time.time() * 1000000000))

    def make_signature(self, nonce: str, url: str, req: dict):
        # First ensure the params are alphabetically sorted by key
        paramString = ""

        if "params" in req:
            for key in req['params']:
                paramString += key
                paramString += "=" + str(req['params'][key])
        sigPayload = f"{nonce}{url}{paramString}"
        print("sigPayload")
        print(sigPayload)
        sig = hmac.new(self.SECRET_KEY.encode('utf-8'), sigPayload.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        return sig

    def make_header(self, url, access_key:str, req: object = None):
        ''' create request header function
        :param url: URL for the new :class:`Request` object.
        '''
        nonce = self.get_nonce()
        url    = url
        sig = self.make_signature(nonce, url, req)
        headers = {
        'ACCESS-KEY'      : access_key,
        'ACCESS-NONCE'    : nonce,
        'ACCESS-SIGNATURE': sig
        }
        return headers

    def exchange_orders_transactions(self):
        method = "/exchange/orders/transactions"
        req = {
            # "params": {
            #     "aaa": ""
            # }
        }

        url = f"{self.base_url}{method}"
        headers = self.make_header(url, self.API_KEY, req)
        pprint(url)
        pprint(headers)
        response = requests.get(url, headers=headers)

        pprint(response)
        pprint(response.content)
        pprint(json.loads(response.text))
        return json.loads(response.text)

    ## GET /api/exchange/orders/transactions_pagination
    def exchange_orders_transactions_pagination(self):
        method = "/exchange/orders/transactions_pagination"
        req = {
            # "params": {
            #     "aaa": ""
            # }
        }

        url = f"{self.base_url}{method}"
        headers = self.make_header(url, self.API_KEY, req)
        pprint(url)
        pprint(headers)
        response = requests.get(url, headers=headers)

        pprint(response)
        pprint(response.content)
        pprint(json.loads(response.text))
        return json.loads(response.text)
    
    ## GET /api/accounts/balance
    def accounts_balance(self):
        method = "/accounts/balance"
        req = {
        }

        url = f"{self.base_url}{method}"
        headers = self.make_header(url, self.API_KEY, req)
        pprint(url)
        pprint(headers)
        response = requests.get(url, headers=headers)

        pprint(response)
        pprint(response.content)
        pprint(json.loads(response.text))
        return json.loads(response.text)

    ## GET /api/send_money
    def get_send_money(self, currency: str="BTC"):
        method = "/send_money"
        req = {
            "params":{
                "currency" : currency
            }
        }

        url = f"{self.base_url}{method}?currency={currency}"
        #url = f"{self.base_url}{method}"
        headers = self.make_header(url, self.API_KEY, req)
        pprint(url)
        pprint(headers)
        response = requests.get(url, headers=headers)

        pprint(response)
        pprint(response.content)
        pprint(json.loads(response.text))
        return json.loads(response.text)

    ## GET /api/deposit_money
    def get_deposit_money(self, currency: str="BTC"):
        method = "/deposit_money"
        req = {
            "params":{
                "currency" : currency
            }
        }

        url = f"{self.base_url}{method}?currency={currency}"
        #url = f"{self.base_url}{method}"
        headers = self.make_header(url, self.API_KEY, req)
        pprint(url)
        pprint(headers)
        response = requests.get(url, headers=headers)

        pprint(response)
        pprint(response.content)
        pprint(json.loads(response.text))
        return json.loads(response.text)

    ## GET /api/withdraws
    def get_withdraws(self):
        method = "/withdraws"
        req = {
            "params":{
            }
        }

        url = f"{self.base_url}{method}"
        headers = self.make_header(url, self.API_KEY, req)
        pprint(url)
        pprint(headers)
        response = requests.get(url, headers=headers)

        pprint(response)
        pprint(response.content)
        pprint(json.loads(response.text))
        return json.loads(response.text)


    # HTTP REQUEST
    # GET /api/trades

    # PARAMETERS
    # *pair Specify a currency pair to trade. "btc_jpy" and "fct_jpy" are now available.
    def get_trades(self, pair:str = "btc_jpy"):
        method = "/trades"
        req = {
            "params":{
                "pair": pair
            }
        }

        url = f"{self.base_url}{method}?pair={pair}"
        headers = self.make_header(url, self.API_KEY, req)
        pprint(url)
        pprint(headers)
        response = requests.get(url)

        pprint(response)
        pprint(json.loads(response.text))
        return json.loads(response.text)