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

        #print(asset_jpy)
        return float(asset_jpy)

    def get_trade(self, pair):
        pub_set = BitBankPubAPI()
        prv_set = self.prv
        trade_btc_jpy = prv_set.get_trade_history(pair, 500)
        # get side: buy
        # get side: sell
        amount_buy = 0
        price_buy = 0
        count_buy = 0
        amount_sell = 0
        price_sell = 0
        count_sell = 0
        amount_price_sell = 0

        for item in trade_btc_jpy['trades']:
            if item['side'] == 'buy':
                amount_buy += float(item['amount'])
                price_buy += float(item['price'])
                count_buy += 1
                print('buy amount' + item['amount'])
                print('buy price' + item['price'])
            elif item['side'] == 'sell':
                amount_sell += float(item['amount'])
                price_sell += float(item['price'])
                count_sell += 1
                print('sell amount' + item['amount'])
                print('sell price' + item['price'])
        print(amount_buy)
        print(amount_sell)
        average_price_buy = price_buy/count_buy
        average_price_sell = price_sell/count_sell
        print('average_price_buy\t' + str(average_price_buy))
        print('average_price_sell\t' + str(average_price_sell))
        average_amount_buy = average_price_buy * amount_buy
        average_amount_sell = average_price_sell * amount_sell
        print(average_amount_buy)
        print(average_amount_sell)
        print(average_amount_sell - average_amount_buy)
        return 0

    def get_withdraw(self, asset):
        pub_set = BitBankPubAPI()
        prv_set = self.prv
        # asset enum: btc, xrp, ltc, eth, mona, bcc
        withdraw_account = prv_set.get_withdraw_account(asset)
        print(json.dumps(withdraw_account, indent=2))
        return 0

