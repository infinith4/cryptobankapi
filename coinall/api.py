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


# signature
def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)
    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


# set request header
def get_header(api_key, sign, timestamp, passphrase):
    header = dict()
    header[CONTENT_TYPE] = APPLICATION_JSON
    header[OK_ACCESS_KEY] = api_key
    header[OK_ACCESS_SIGN] = sign
    header[OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[OK_ACCESS_PASSPHRASE] = passphrase
    return header


def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        url = url + str(key) + '=' + str(value) + '&'

    return url[0:-1]


# request example
# set the request url
base_url = 'https://www.CoinAll.com'
request_path_currencies = '/api/account/v3/currencies'
request_path_timestamp = "/api/general/v3/time"
request_path_wallet = "/api/account/v3/wallet"
request_path_spot = "/api/spot/v3/accounts"
request_path_instruments = "/api/spot/v3/instruments/BSV-USDT/candles"

# set request header
api_key = ""
secret_key = ""
pass_phrase = ""

response_timestamp = requests.get(base_url + request_path_timestamp)
timestamp = response_timestamp.json()["iso"]
print(timestamp)
header = get_header(api_key, signature(timestamp, 'GET', request_path_currencies, "None", secret_key), timestamp, pass_phrase)
# do request
response = requests.get(base_url + request_path_currencies, headers=header)
# json
#print(response.json())
#print(json.dumps(response.json(), indent=2))

## funding account wallet
header = get_header(api_key, signature(timestamp, 'GET', request_path_wallet, "None", secret_key), timestamp, pass_phrase)
response_wallet = requests.get(base_url + request_path_wallet, headers=header)
# json
#print(response_wallet.json())
print(json.dumps(response_wallet.json(), indent=2))

balance_BSV = 0
for asset in response_wallet.json():
    print("asset: " + asset.get('balance'))
    if asset.get('currency') == "BSV":
        balance_BSV += float(asset.get('balance'))
        

## trading account wallet
header = get_header(api_key, signature(timestamp, 'GET', request_path_spot, "None", secret_key), timestamp, pass_phrase)
response_spot = requests.get(base_url + request_path_spot, headers=header)
# json
#print(response_spot.json())
print(json.dumps(response_spot.json(), indent=2))

for asset in response_spot.json():
    print("asset: " + asset.get('balance'))
    if asset.get('currency') == "BSV":
        balance_BSV += float(asset.get('balance'))
    

## Get Market Data
header = get_header(api_key, signature(timestamp, 'GET', request_path_instruments, "None", secret_key), timestamp, pass_phrase)
response_instruments = requests.get(base_url + request_path_instruments + "?granularity=60", headers=header)
# json
#print(response_spot.json())
print(json.dumps(response_instruments.json()[0], indent=2))
print(float(response_instruments.json()[0][1]) * balance_BSV)



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
