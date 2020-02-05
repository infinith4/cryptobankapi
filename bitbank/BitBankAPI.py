#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import python_bitbankcc
import json

class BitBankPubAPI:

    def __init__(self):
        self.pub = python_bitbankcc.public()

    def get_ticker(self, pair):
        try:
            value = self.pub.get_ticker(pair)
            return value
        except Exception as e:
            print(e)
            return None

class BitBankPrvAPI:

    def __init__(self, api_key, api_secret):
        self.prv = python_bitbankcc.private(api_key, api_secret)

    def get_asset(self):
        try:
            value = self.prv.get_asset()
            return value
        except Exception as e:
            print(e)
            return None

    def get_asset_jpy(self):
        pub_set = BitBankPubAPI()
        prv_set = self.prv

        ticker = pub_set.get_ticker('btc_jpy')
        print(ticker['last'])

        asset_dict = prv_set.get_asset()
        #print(asset_dict['assets'])
        print(json.dumps(asset_dict['assets'], indent=2))

        asset_jpy = 0
        asset_btc = 0
        #btctojpy = ticker['last'] * asset_dict['assets']
        for asset in asset_dict['assets']:
            print("asset: " + asset.get('asset'))
            print("onhand_amount: " + asset.get('onhand_amount'))
            if asset.get('asset') == 'jpy':
                asset_jpy += float(asset.get('onhand_amount'))
            elif asset.get('asset') != 'ltc' and asset.get('asset') != 'eth' :
                ticker = pub_set.get_ticker(asset.get('asset') + '_jpy')
                print(ticker['last'])
                asset_jpy += float(asset.get('onhand_amount')) * float(ticker['last'])
            else:
                if asset.get('asset') == 'ltc' or asset.get('asset') == 'eth' :
                    ticker = pub_set.get_ticker(asset.get('asset') + '_btc')
                    asset_btc += float(asset.get('onhand_amount')) * float(ticker['last'])

        ticker_btc = pub_set.get_ticker('btc_jpy')
        asset_jpy += float(asset_btc) * float(ticker_btc['last'])

        print(asset_jpy)
        return float(asset_jpy)

    def get_trade(self, pair):
        pub_set = BitBankPubAPI()
        prv_set = self.prv
        trade_btc_jpy = prv_set.get_trade_history(pair, 500)
        print(json.dumps(trade_btc_jpy, indent=2))
        return 0

