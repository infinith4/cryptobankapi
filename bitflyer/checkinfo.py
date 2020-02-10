import pybitflyer
import json
import yaml

with open('apikey.yaml', 'rt') as fin:
  apikey_text = fin.read()
 
apidata = yaml.load(apikey_text)
api = pybitflyer.API(api_key=apidata['api_key'], api_secret=apidata['api_secret'])

board = api.board(product_code="BTC_JPY")

print(board)
print(min([p["price"] for p in board["asks"]]))
print(max([p["price"] for p in board["asks"]]))
ticker = api.ticker(product_code="BTC_JPY")
#print(ticker)

collateral = api.getcollateral()
print("collateral")
print(collateral)
#jsonString = collateral
#data = json.loads(jsonString)
#jsondata = json.dump(data, indent=4, separators=(',', ': '))
#print(jsondata)
print("open_position_pnl")
print(collateral["open_position_pnl"])

if collateral["keep_rate"] == 0.85 :
  #ALL Order Cancel
  print("ALL Order Cancel")
  #cancelallchildorders = api.cancelallchildorders(product_code="FX_BTC_JPY")
  #print(cancelallchildorders)
  #現在の注文状況をチェックする
  #現在注文中のBTCを売買する(買い注文なら売る。売り注文なら買う)
  positions = api.getpositions(product_code="FX_BTC_JPY")
  print(positions)
  print("length:", len(positions))

  ordered_side = ""
  if len(positions) > 0:
    for elem in positions:
      if elem["product_code"] == "FX_BTC_JPY":
        print(elem["side"])
        ordered_side = elem["side"]
    if ordered_side == "BUY":
      #Order Sell
      print("ORDER SELL")
      #sell_fx_btc = api.sendchildorder(product_code="FX_BTC_JPY",
      #                               child_order_type="MARKET",
      #                               side="SELL",
      #                               size=0.5,
      #                               minute_to_expire=10000,
      #                               time_in_force="GTC"
      #)
      #print(buy_fx_btc)
    elif ordered_side == "SELL":
      #Order BUY
      print("ORDER BUY")
      # buy_fx_btc = api.sendchildorder(product_code="FX_BTC_JPY",
      #                              child_order_type="MARKET",
      #                              side="BUY",
      #                              size=0.5,
      #                              minute_to_expire=10000,
      #                              time_in_force="GTC"
      # )

      # print(buy_fx_btc)




#coinins = api.getcoinins()
#print("coinins")
#print(coinins)
#print(type(coinins))
#jsonString = coinins
#data = json.loads(jsonString)
#jsondata = json.dump(data, indent=4, separators=(',', ': '))
#print(jsondata)

#print(data["open_position_pnl"])

childorders = api.getchildorders()

print(childorders)

# buy_fx_btc = api.sendchildorder(product_code="FX_BTC_JPY",
#                              child_order_type="MARKET",
#                              side="BUY",
#                              size=0.001,
#                              minute_to_expire=10000,
#                              time_in_force="GTC"
# )

# print(buy_fx_btc)

#証拠金維持率が0.8未満にならないようにいくら売買すれば0.8以上になるか計算する(課題)
#とりあえず今は固定で売買する
#buy_fx_btc = api.sendchildorder(product_code="FX_BTC_JPY",
#                                child_order_type="MARKET",
#                                side="BUY",
#                                size=0.001,
#                                minute_to_expire=10000,
#                                time_in_force="GTC"
#)

#print(buy_fx_btc)



# {'collateral': 65124.0, 'open_position_pnl': -1393.969, 'require_collateral': 47620.8248, 'keep_rate': 1.3382807052934538}


# buy_fx_btc = api.sendchildorder(product_code="FX_BTC_JPY",
#                              child_order_type="MARKET",
#                              side="BUY",
#                              size=0.001,
#                              minute_to_expire=10000,
#                              time_in_force="GTC"
# )

# print(buy_fx_btc)

# child_order_typeは注文のタイプで、指値注文なら"LIMIT"、成行注文なら"MARKET"を指定します。
# sideには売り買いを"SELL"か"BUY"で、sizeに取引額を指定します。
# なお、minute_to_expireやtime_in_forceは必須ではありません。


