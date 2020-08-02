#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hmac
import hashlib
import json
import requests
import time

class CryptoComApi:

    def __init__(self, apiKey, secretKey):
        self.base_url = "https://api.crypto.com/v2"

        self.API_KEY = apiKey
        self.SECRET_KEY = secretKey

    ## TODO: private/get-order-history
    #def private_get_order_history():
    
    ## TODO: private/get-trades https://exchange-docs.crypto.com/?java#private-get-trades
    #def private_get_trades():

    def private_get_order_detail(self, order_id: str):

        req = {
        "id": 11,
        "method": "private/get-order-detail",
        "api_key": self.API_KEY,
        "params": {
            "order_id": order_id,
        },
        "nonce": int(time.time() * 1000)
        }

        # First ensure the params are alphabetically sorted by key
        paramString = ""

        if "params" in req:
            for key in req['params']:
                paramString += key
                paramString += str(req['params'][key])

        sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])
        print("sigPayload")
        print(sigPayload)
        sig = hmac.new(bytes(str(self.SECRET_KEY), 'utf-8'), msg=bytes(sigPayload, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

        print("sig")
        print(sig)
        response = requests.post(self.base_url + "/private/get-order-detail", json=req)
        print(response)
        return sig

    def private_get_order_history(self):

        req = {
        "id": 12,
        "method": "private/get-order-history",
        "api_key": self.API_KEY,
        "params": {
            "instrument_name": "BTC_USDT",
        },
        "sig": "",
        "nonce": int(time.time() * 1000)
        }
        # First ensure the params are alphabetically sorted by key
        paramString = ""

        if "params" in req:
            for key in req['params']:
                paramString += key
                paramString += str(req['params'][key])

        sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])
        print("sigPayload")
        print(sigPayload)
        sig = hmac.new(bytes(str(self.SECRET_KEY), 'utf-8'), msg=bytes(sigPayload, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

        print("sig")
        print(sig)
        req["sig"] = sig
        print(req)
        response = requests.post(self.base_url + "/private/get-order-history", req)
        print(response.content)
        return sig