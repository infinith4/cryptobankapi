import python_bitbankcc
import json
from utils.Config import Config

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

    def __init__(self):
        configFile = "../app_config.yml"
        config = Config(configFile).content
        API_KEY = config['BANKINFO']['BITBANK']['API_KEY']
        API_SECRET = config['BANKINFO']['BITBANK']['SECRET_KEY']
        self.prv = python_bitbankcc.private(API_KEY, API_SECRET)

    def get_asset(self):
        try:
            value = self.prv.get_asset()
            return value
        except Exception as e:
            print(e)
            return None

def main():
    pub_set = BitBankPubAPI()
    prv_set = BitBankPrvAPI()

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
        if asset.get('asset') != 'jpy' and asset.get('asset') != 'ltc' and asset.get('asset') != 'eth' :
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

if __name__ == '__main__':
    main()