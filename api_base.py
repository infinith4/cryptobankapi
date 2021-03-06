from coinall.CoinallAPI import CoinallAPI
from bitbank.BitBankAPI import BitBankPrvAPI
from bitflyer.BitflyerAPI import BitflyerAPI
from cryptocom.CryptoComApi import CryptoComApi
from coincheck.CoinCheckApi import CoinCheckApi
from coinmarketcap.CoinMarketCapApi import CoinMarketCapApi
from utils.Config import Config

import datetime


JPY_USDT = 107
configFile = "app_config.yml"
config = Config(configFile).content

COINALL_API_KEY = config['BANKINFO']['COINALL']['API_KEY']
COINALL_API_SECRET = config['BANKINFO']['COINALL']['SECRET_KEY']
COINALL_PASS_PHRASE = config['BANKINFO']['COINALL']['PASS_PHRASE']

CRYPTOCOM_API_KEY = config['BANKINFO']['CRYPTOCOM']['API_KEY']
CRYPTOCOM_API_SECRET = config['BANKINFO']['CRYPTOCOM']['SECRET_KEY']

COINCHECK_API_KEY = config['BANKINFO']['COINCHECK']['API_KEY']
COINCHECK_SECRET_KEY = config['BANKINFO']['COINCHECK']['SECRET_KEY']

COINMARKETCAP_API_KEY = config['BANKINFO']['COINMARKETCAP']['API_KEY']
#COINMARKETCAP_SECRET_KEY = config['BANKINFO']['COINMARKETCAP']['SECRET_KEY']

########### CoinMarketCap ###########################

# coinMarketApi = CoinMarketCapApi(COINMARKETCAP_API_KEY)
# coinMarketApi.get_listing()

########### Coincheck ###########################

# coinCheckApi = CoinCheckApi(COINCHECK_API_KEY, COINCHECK_SECRET_KEY)
# coinCheckApi.exchange_orders_transactions_pagination()
# coinCheckApi.get_deposit_money()
# coinCheckApi.get_withdraws()
# coinCheckApi.get_trades("btc_jpy")
#coinCheckApi.accounts_balance()
#coinCheckApi.get_send_money()

#coinCheckApi.exchange_orders_transactions()

###########Crypto.com###########################


cryptoComApi = CryptoComApi(CRYPTOCOM_API_KEY, CRYPTOCOM_API_SECRET)

cryptoComApi.public_get_instruments()



# startDateTime = datetime.datetime(2020, 5, 12, 0, 0, 0)
# endDateTime = datetime.datetime(2020, 5, 13, 0, 0, 0)
# startTimeStamp = int(startDateTime.timestamp()* 1000)
# endTimeStamp = int(endDateTime.timestamp()* 1000)
# print(startTimeStamp)
# print(endTimeStamp)

# cryptoComApi.private_get_order_history(startTimeStamp, endTimeStamp, "CRO_USDT")

startDateTime = datetime.datetime(2020, 5, 4, 0, 0, 0)
endDateTime = datetime.datetime(2020, 5, 15, 0, 0, 0)

cryptoComApi.get_order_histories(startDateTime, endDateTime, "CRO_USDT")
#cryptoComApi.public_get_instruments()

# ######################################

# coinall_asset_usdt = 0
# coinalapi = CoinallAPI(COINALL_API_KEY, COINALL_API_SECRET, COINALL_PASS_PHRASE)
# balance_bsv = coinalapi.get_balance(COINALL_API_KEY, COINALL_API_SECRET, COINALL_PASS_PHRASE, "BSV")
# bsv_price = coinalapi.get_marketdata_bsv()
# coinall_asset_usdt += balance_bsv * bsv_price
# balance_okb = coinalapi.get_balance(COINALL_API_KEY, COINALL_API_SECRET, COINALL_PASS_PHRASE, "OKB")
# okb_price = coinalapi.get_marketdata_okb()
# coinall_asset_usdt += balance_okb * okb_price
# print(coinall_asset_usdt)
# print("coinall_asset_usdt * JPY_USDT")
# print(coinall_asset_usdt * JPY_USDT)

# ######################################

# BITBANK_API_KEY = config['BANKINFO']['BITBANK']['API_KEY']
# BITBANK_API_SECRET = config['BANKINFO']['BITBANK']['SECRET_KEY']


# bitbankapi = BitBankPrvAPI(BITBANK_API_KEY, BITBANK_API_SECRET)

# bitbank_asset_jpy = bitbankapi.get_asset_jpy()

# print("all asset: ")
# print((coinall_asset_usdt*JPY_USDT) + bitbank_asset_jpy)

# print("==================bitbank==================")
# print("btc_jpy==================")
# bitbankapi.get_trade("btc_jpy")
# print("mona_jpy==================")
# bitbankapi.get_trade("mona_jpy")
# print("xrp_jpy==================")
# bitbankapi.get_trade("xrp_jpy")
# print("bcc_jpy==================")
# bitbankapi.get_trade("bcc_jpy")

# print("get_withdraw btc==================")
# bitbankapi.get_withdraw("btc")
# ######################################

# # API_KEY = config['BANKINFO']['BITFLYER']['API_KEY']
# # API_SECRET = config['BANKINFO']['BITFLYER']['SECRET_KEY']

# # bitflyerapi = BitflyerAPI(API_KEY, API_SECRET)

