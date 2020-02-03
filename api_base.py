from coinall.CoinallAPI import CoinallAPI
from utils.Config import Config



configFile = "app_config.yml"
config = Config(configFile).content
API_KEY = config['BANKINFO']['COINALL']['API_KEY']
API_SECRET = config['BANKINFO']['COINALL']['SECRET_KEY']
PASS_PHRASE = config['BANKINFO']['COINALL']['PASS_PHRASE']
print(PASS_PHRASE)

coinalapi = CoinallAPI(API_KEY, API_SECRET, PASS_PHRASE)
balance_bsv = coinalapi.get_balance(API_KEY, API_SECRET, PASS_PHRASE)
bsv_price = coinalapi.get_marketdata_bsv()
print(balance_bsv * bsv_price)