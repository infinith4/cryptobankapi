#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pybitflyer
import json

class BitflyerAPI:

    def __init__(self, api_key, api_secret):
        self.api = pybitflyer.API(api_key=api_key, api_secret=api_secret)
        board = self.api.board(product_code="BTC_JPY")
        print(board)
        print(min([p["price"] for p in board["asks"]]))
        print(max([p["price"] for p in board["asks"]]))
        ticker = self.api.ticker(product_code="BTC_JPY")