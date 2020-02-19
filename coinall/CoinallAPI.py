#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import hmac
import base64
import requests
import json

CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'

class CoinallAPI:

    def __init__(self, api_key, secret_key, pass_phrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.pass_phrase = pass_phrase
        self.base_url = 'https://www.CoinAll.com'
        self.request_path_currencies = '/api/account/v3/currencies'
        self.request_path_timestamp = "/api/general/v3/time"
        self.request_path_wallet = "/api/account/v3/wallet"
        self.request_path_spot = "/api/spot/v3/accounts"
        self.request_path_instruments_bsv_usdt = "/api/spot/v3/instruments/BSV-USDT/candles"
        self.request_path_instruments_okb_usdt = "/api/spot/v3/instruments/OKB-USDT/candles"

    # signature
    def signature(self, timestamp, method, request_path, body, secret_key):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = str(timestamp) + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)


    # set request header
    def get_header(self, api_key, sign, timestamp, passphrase):
        header = dict()
        header[CONTENT_TYPE] = APPLICATION_JSON
        header[OK_ACCESS_KEY] = api_key
        header[OK_ACCESS_SIGN] = sign
        header[OK_ACCESS_TIMESTAMP] = str(timestamp)
        header[OK_ACCESS_PASSPHRASE] = passphrase
        return header


    def parse_params_to_str(self, params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'

        return url[0:-1]

    def get_balance(self, api_key, secret_key, pass_phrase, cryptocurrency_name):
        # set request header
        response_timestamp = requests.get(self.base_url + self.request_path_timestamp)
        timestamp = response_timestamp.json()["iso"]
        sign = self.signature(timestamp, 'GET', self.request_path_currencies, "None", secret_key)
        header = self.get_header(api_key, sign , timestamp, pass_phrase)
        # do request
        response = requests.get(self.base_url + self.request_path_currencies, headers=header)
        # json
        #print(response.json())
        #print(json.dumps(response.json(), indent=2))

        ## funding account wallet
        header = self.get_header(api_key, self.signature(timestamp, 'GET', self.request_path_wallet, "None", secret_key), timestamp, self.pass_phrase)
        response_wallet = requests.get(self.base_url + self.request_path_wallet, headers=header)
        # json
        #print(response_wallet.json())
        print(json.dumps(response_wallet.json(), indent=2))

        balance = 0
        for asset in response_wallet.json():
            if asset["currency"] == cryptocurrency_name:
                balance += float(asset["balance"])

        ## trading account wallet
        header = self.get_header(api_key, self.signature(timestamp, 'GET', self.request_path_spot, "None", secret_key), timestamp, self.pass_phrase)
        request_path_spot = requests.get(self.base_url + self.request_path_spot, headers=header)
        # json
        #print(response_spot.json())
        print(json.dumps(request_path_spot.json(), indent=2))

        for asset in request_path_spot.json():
            if asset["currency"] == cryptocurrency_name:
                balance += float(asset["balance"])

        #print(balance_BSV)
        return balance

    def get_marketdata_bsv(self):
        response_timestamp = requests.get(self.base_url + self.request_path_timestamp)
        timestamp = response_timestamp.json()["iso"]
        
        ## Get Market Data
        header = self.get_header(self.api_key, self.signature(timestamp, 'GET', self.request_path_instruments_bsv_usdt, "None", self.secret_key), timestamp, self.pass_phrase)
        response_instruments = requests.get(self.base_url + self.request_path_instruments_bsv_usdt + "?granularity=60", headers=header)
        # json
        print("-----------")
        print(json.dumps(response_instruments.json()[0], indent=2))
        return float(response_instruments.json()[0][1])

    def get_marketdata_okb(self):
        response_timestamp = requests.get(self.base_url + self.request_path_timestamp)
        timestamp = response_timestamp.json()["iso"]
        
        ## Get Market Data
        header = self.get_header(self.api_key, self.signature(timestamp, 'GET', self.request_path_instruments_okb_usdt, "None", self.secret_key), timestamp, self.pass_phrase)
        response_instruments = requests.get(self.base_url + self.request_path_instruments_okb_usdt + "?granularity=60", headers=header)
        # json
        print("-----------")
        print(json.dumps(response_instruments.json()[0], indent=2))
        return float(response_instruments.json()[0][1])

# Response
# Parameter	Type	Description
# time	String	Start time
# open	String	Open price
# high	String	Highest price
# low	String	Lowest price
# close	String	Close price
# volume	String	Trading volume

# [{
#     "id": "BTC",
#     "name": “Bitcoin”，
#      "deposit": "1",
#      "withdraw": “1”,
#       “withdraw_min”:”0.000001btc”
# }, {
#     "id": "ETH",
#     "name": “Ethereum”,
#     "deposit": "1",
#      "withdraw": “1”，
#      “withdraw_min”:”0.0001eth”
#     }
#  …
# ]


# ########################################################
# # take order
# base_url = 'https://www.CoinAll.com'
# request_path = '/api/spot/v3/orders'

# # request params
# params = {'type': 'market', 'side': 'buy', 'instrument_id': 'usdt_okb', 'size': '10', 'client_oid': '',
#                   'price': '10', 'funds': ''}

# # request path
# request_path = request_path + parse_params_to_str(params)
# url = base_url + request_path

# # request header and body
# header = get_header('your_api_key', signature('timestamp', 'POST', request_path, 'your_secret_key'), 'timestamp', 'your_passphrase')
# body = json.dumps(params)

# # do request
# response = requests.post(url, data=body, headers=header)

# #########################################################
# # get order info
# base_url = 'https://www.CoinAll.com'
# request_path = '/api/spot/v3/orders'

# params = {'status':'all', 'instrument_id': 'okb_usdt'}

# # request path
# request_path = request_path + parse_params_to_str(params)
# url = base_url + request_path

# # request header and body
# header = get_header('your_api_key', signature('timestamp', 'GET', request_path, 'your_secret_key'), 'timestamp', 'your_passphrase')

# # do request
# response = requests.get(url, headers=header)
