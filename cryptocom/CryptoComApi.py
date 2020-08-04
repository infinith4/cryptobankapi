#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hmac
import hashlib
import json
import requests
import time
import datetime

from pprint import pprint

##https://crypto.com/exchange-doc
## https://crypto.com/exchange-docs-v1

class CryptoComApi:

    def __init__(self, apiKey, secretKey):
        self.base_url = "https://api.crypto.com/v2"

        self.API_KEY = apiKey
        self.SECRET_KEY = secretKey

    def get_nonce(self):
        #return str(int(time.time() * 1000))
        return str(int(time.time() * 1000))

    def make_signature(self, method: str, id: str, nonce: str, req: dict):
        # NOTE: First ensure the params are alphabetically sorted by key
        paramString = ""
        
        if "params" in req:
            items = req['params'].items()
            sorted_params = sorted(items)
            for item in sorted_params:
                print(item)
                paramString += item[0]
                paramString += str(item[1])
        sigPayload = f"{method}{id}{self.API_KEY}{paramString}{nonce}"
        print("sigPayload")
        print(sigPayload)
        sig = hmac.new(self.SECRET_KEY.encode('utf-8'), sigPayload.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        return sig

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

    # private/get-order-history
    def private_get_order_history(self,start_ts:int, end_ts:int, instrument_name:str = "BTC_USDT"):

        method = "private/get-order-history"
        req = {
        "id": 12,
        "method": method,
        "api_key": self.API_KEY,
        "params": {
            "instrument_name": instrument_name,
            ##TODO: datetime to timestamp
            #NOTE: default is 24 hours ago.
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page_size": 2,
            "page": 0
        },
        "sig": "",
        "nonce": self.get_nonce()
        }

        url = f"{self.base_url}/{method}"  ##it's ok
        #url = f"{self.base_url}/{method}?instrument_name=BTC_USDT"
        #url = f"{self.base_url}/{method}?instrument_name={instrument_name}&start_ts={start_ts}&end_ts={end_ts}"
        id = str(req["id"])
        sig = self.make_signature(method = method, id = id, nonce = req["nonce"], req=req)

        print("sig")
        print(sig)
        req["sig"] = sig
        print(req)
        headers = {
            "Content-Type" : "application/json"
        }
        response = requests.post(url, json=req, headers=headers)
        print(response.content)
        return sig

    def get_order_histories(self, startDateTime: datetime, endDateTime: datetime, instrument_name:str = "CRO_USDT"):
        subDateTime = endDateTime - startDateTime
        for day in range(subDateTime.days):
            epochStartDateTime = startDateTime + datetime.timedelta(days=day)
            epochEndDateTime = startDateTime + datetime.timedelta(days=day + 1)
            pprint(f"from {epochStartDateTime} to {epochEndDateTime}")
            startTimeStamp = int(epochStartDateTime.timestamp()* 1000)
            endTimeStamp = int(epochEndDateTime.timestamp()* 1000)
            time.sleep(2)
            self.private_get_order_history(startTimeStamp, endTimeStamp, instrument_name)


    ## GET public/get-instruments
    def public_get_instruments(self):
        method = "public/get-instruments"
        req = {
            "id":11,
            "method": method,
            "nonce": self.get_nonce()
        }
        url = f"{self.base_url}/{method}"
        response = requests.get(url, json=req)

        pprint(response)
        pprint(json.loads(response.text))

        return json.loads(response.text)
