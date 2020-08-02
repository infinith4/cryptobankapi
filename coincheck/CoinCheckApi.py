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

    def make_header(self, url,
                access_key=None,
                secret_key=None):
        ''' create request header function
        :param url: URL for the new :class:`Request` object.
        '''
        nonce = self.get_nonce()
        url    = url
        message = nonce + url
        signature = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        headers = {
        'ACCESS-KEY'      : access_key,
        'ACCESS-NONCE'    : nonce,
        'ACCESS-SIGNATURE': signature
        }
        return headers

    def exchange_orders_transactions(self):
        method = "/exchange/orders/transactions"
        req = {
            # "params": {
            #     "aaa": ""
            # }
        }

        nonce = self.get_nonce()
        url = f"{self.base_url}{method}"
        sig = self.make_signature(nonce, url, req)
        headers = {
            "ACCESS-KEY": self.API_KEY,
            "ACCESS-NONCE": str(nonce),
            "ACCESS-SIGNATURE": sig
        }
        pprint(url)
        pprint(nonce)
        pprint(headers)
        response = requests.get(url, headers=headers)

        pprint(response)
        pprint(response.content)
        pprint(json.loads(response.text))
        return json.loads(response.text)