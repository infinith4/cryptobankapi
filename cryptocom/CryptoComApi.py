#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hmac
import hashlib
import json
import requests
import time
import datetime
from py_linq import Enumerable

from pprint import pprint
from cryptocom.models.order_history_model import OrderHistoryModel
from cryptocom.models.order_totally_history_model import OrderTotallyHistoryModel

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
                paramString += item[0]
                paramString += str(item[1])
        sigPayload = f"{method}{id}{self.API_KEY}{paramString}{nonce}"
        # print("sigPayload")
        # print(sigPayload)
        sig = hmac.new(self.SECRET_KEY.encode('utf-8'), sigPayload.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()

        return sig

    ## TODO: private/get-order-history
    #def private_get_order_history():
    
    ## TODO: private/get-trades https://exchange-docs.crypto.com/?java#private-get-trades
    #def private_get_trades():

    def private_get_order_detail(self, order_id: str):
        method = "private/get-order-detail"
        req = {
        "id": 11,
        "method": method,
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

        url = f"{self.base_url}/{method}"
        sigPayload = req['method'] + str(req['id']) + req['api_key'] + paramString + str(req['nonce'])
        # print("sigPayload")
        # print(sigPayload)
        sig = hmac.new(bytes(str(self.SECRET_KEY), 'utf-8'), msg=bytes(sigPayload, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

        # print("sig")
        # print(sig)
        response = requests.post(url, json=req)
        print(response)
        return json.loads(response.text)

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
            "page_size": 2,  ##TODO: mod
            "page": 0  ##TODO: mod
        },
        "sig": "",
        "nonce": self.get_nonce()
        }

        url = f"{self.base_url}/{method}"  ##NOTE: no need query params.
        #url = f"{self.base_url}/{method}?instrument_name=BTC_USDT"
        #url = f"{self.base_url}/{method}?instrument_name={instrument_name}&start_ts={start_ts}&end_ts={end_ts}"
        id = str(req["id"])
        sig = self.make_signature(method = method, id = id, nonce = req["nonce"], req=req)

        #print("sig")
        #print(sig)
        req["sig"] = sig
        #print(req)
        headers = {
            "Content-Type" : "application/json"
        }
        response = requests.post(url, json=req, headers=headers)
        return json.loads(response.text)

    def get_order_histories(self, startDateTime: datetime, endDateTime: datetime, instrument_name:str = "CRO_USDT"):
        subDateTime = endDateTime - startDateTime
        orderHistroyList = []
        for day in range(subDateTime.days):
            epochStartDateTime = startDateTime + datetime.timedelta(days=day)
            epochEndDateTime = startDateTime + datetime.timedelta(days=day + 1)
            pprint(f"from {epochStartDateTime} to {epochEndDateTime}")
            startTimeStamp = int(epochStartDateTime.timestamp()* 1000)
            endTimeStamp = int(epochEndDateTime.timestamp()* 1000)
            time.sleep(2)
            resJson = self.private_get_order_history(startTimeStamp, endTimeStamp, instrument_name)
            if resJson["code"] != 0:
                continue

            if len(resJson["result"]["order_list"]) == 0:
                continue
            else:
                pprint(resJson["result"]["order_list"])
            
            for order in resJson["result"]["order_list"]:
                if order['status'] == 'FILLED':
                    orderHistroyList.append(OrderHistoryModel(order["order_id"], order["side"], order["price"], order["quantity"]))

        #orderHistroyList = list(map(OrderHistoryModel, orderHistroyList)) #does not work
        unit = self.get_pair_to_unit_for_profit(instrument_name)
        self.get_totally_history_data(orderHistroyList, unit)
    
    def get_totally_history_data(self, orderHistroyList: list, unit: str):
        ##https://viralogic.github.io/py-enumerable/
        sellPriceAmount = 0
        sellAmount = 0
        sellPriceTotal = 0
        enumorderHistroyList = Enumerable(orderHistroyList)
        sellOrders = enumorderHistroyList.where(lambda x: x.side == "SELL")
        cnt = 0
        for orderHistory in sellOrders:
            #orderHistory = map(OrderHistoryModel, item) #does not work
            pprint(f"{orderHistory.price};{orderHistory.quantity}")
            sellPriceTotal += orderHistory.price
            sellAmount += orderHistory.quantity
            sellPriceAmount += orderHistory.quantity * orderHistory.price
            cnt += 1

        sellOrderTotallyHistory = OrderTotallyHistoryModel(sellAmount, sellPriceTotal/cnt)  ## WARNING: 計算が間違っている
        pprint(sellOrderTotallyHistory)
        buyAmount = 0
        buyPriceTotal = 0
        buyPriceAmount = 0
        enumorderHistroyList = Enumerable(orderHistroyList)
        buyOrders = enumorderHistroyList.where(lambda x: x.side == "BUY")
        cnt = 0
        for orderHistory in buyOrders:
            #orderHistory = map(OrderHistoryModel, item) #does not work
            pprint(f"{orderHistory.price};{orderHistory.quantity}")
            buyPriceTotal += orderHistory.price
            buyAmount += orderHistory.quantity
            buyPriceAmount += orderHistory.quantity * orderHistory.price
            cnt += 1

        buyOrderTotallyHistory = OrderTotallyHistoryModel(buyAmount, buyPriceTotal/cnt)  ## WARNING: 計算が間違っている
        totalQuantity = buyOrderTotallyHistory.totalQuantity if sellOrderTotallyHistory.totalQuantity > buyOrderTotallyHistory.totalQuantity else sellOrderTotallyHistory.totalQuantity
        profit = sellPriceAmount - buyPriceAmount #(sellOrderTotallyHistory.averagePrice - buyOrderTotallyHistory.averagePrice) * totalQuantity
        formatted_profit = "{:>10.4f}".format(profit)
        pprint(f"{formatted_profit} {unit}")

        # 0.0634 * 5348.087 = 339.0687158
        # 0.0657 * 2.0 = 0.1314
        # 0.0635 * 5000.0 = 317.5
        # (0.0634 - 0.0635) * 5000 = -0.5


    def get_pair_to_unit_for_profit(self, instrument_name: str):
        return instrument_name.split("_")[1]

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

        # pprint(response)
        # pprint(json.loads(response.text))

        return json.loads(response.text)
