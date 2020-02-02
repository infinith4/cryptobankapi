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

    def __init__(self):
        API_KEY = ''
        API_SECRET = ''
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
    #btctojpy = ticker['last'] * asset_dict['assets']
    for asset in asset_dict['assets']:
        print("asset: " + asset.get('asset'))
        print("onhand_amount: " + asset.get('onhand_amount'))
        if asset.get('asset') != 'jpy' and asset.get('asset') != 'ltc' and asset.get('asset') != 'eth' :
            ticker = pub_set.get_ticker(asset.get('asset') + '_jpy')
            print(ticker['last'])
            asset_jpy += float(asset.get('onhand_amount')) * float(ticker['last'])
    print(asset_jpy)

if __name__ == '__main__':
    main()