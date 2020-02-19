from coinall.CoinallAPI import CoinallAPI
from bitbank.BitBankAPI import BitBankPrvAPI
from bitflyer.BitflyerAPI import BitflyerAPI

from utils.Config import Config


JPY_USDT = 110
configFile = "app_config.yml"
config = Config(configFile).content
API_KEY = config['BANKINFO']['COINALL']['API_KEY']
API_SECRET = config['BANKINFO']['COINALL']['SECRET_KEY']
PASS_PHRASE = config['BANKINFO']['COINALL']['PASS_PHRASE']
print(PASS_PHRASE)

coinall_asset_usdt = 0
coinalapi = CoinallAPI(API_KEY, API_SECRET, PASS_PHRASE)
balance_bsv = coinalapi.get_balance(API_KEY, API_SECRET, PASS_PHRASE, "BSV")
bsv_price = coinalapi.get_marketdata_bsv()
coinall_asset_usdt += balance_bsv * bsv_price
balance_okb = coinalapi.get_balance(API_KEY, API_SECRET, PASS_PHRASE, "OKB")
okb_price = coinalapi.get_marketdata_okb()
coinall_asset_usdt += balance_okb * okb_price
print(coinall_asset_usdt)
print(coinall_asset_usdt * JPY_USDT)

API_KEY = config['BANKINFO']['BITBANK']['API_KEY']
API_SECRET = config['BANKINFO']['BITBANK']['SECRET_KEY']


bitbankapi = BitBankPrvAPI(API_KEY, API_SECRET)

bitbank_asset_jpy = bitbankapi.get_asset_jpy()

print((coinall_asset_usdt*JPY_USDT) + bitbank_asset_jpy)

bitbankapi.get_trade("btc_jpy")
bitbankapi.get_trade("mona_jpy")
bitbankapi.get_trade("xrp_jpy")
bitbankapi.get_trade("bcc_jpy")

bitbankapi.get_withdraw("btc")

API_KEY = config['BANKINFO']['BITFLYER']['API_KEY']
API_SECRET = config['BANKINFO']['BITFLYER']['SECRET_KEY']

bitflyerapi = BitflyerAPI(API_KEY, API_SECRET)

