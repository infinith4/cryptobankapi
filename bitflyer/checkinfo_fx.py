import pybitflyer
import json
import yaml

with open('apikey.yaml', 'rt') as fin:
  apikey_text = fin.read()

apidata = yaml.load(apikey_text)
api = pybitflyer.API(api_key=apidata['api_key'], api_secret=apidata['api_secret'])

productCode = "FX_BTC_JPY"  #FX

board = api.board(product_code=productCode) #FX_BTC_JPY

#print(board)
print("buy price :min,max")
print(board)
print(min([p["price"] for p in board["asks"]]))  #買値の最小価格, いつからいつまでの期間？
print(max([p["price"] for p in board["asks"]]))  #買値の最大価格

ticker = api.ticker(product_code=productCode)
print("ticker")
print(ticker)

collateral = api.getcollateral()
print("collateral")
print(collateral)
#jsonString = collateral
#data = json.loads(jsonString)
#jsondata = json.dump(data, indent=4, separators=(',', ': '))
#print(jsondata)
print("open_position_pnl 建玉の評価損益（円）")
print(collateral["open_position_pnl"])

positions = api.getpositions(product_code=productCode)
print(positions)
print("length:", len(positions))

execetions = api.getexecutions(product_code=productCode)
print("execetions")
print(execetions)

minKeepRate = 0.80
print('証拠金維持率が{0}%になったら全キャンセル'.format(minKeepRate*100))
if collateral["keep_rate"] == minKeepRate :
  #ALL Order Cancel
  print("ALL Order Cancel")
  #cancelallchildorders = api.cancelallchildorders(product_code="FX_BTC_JPY")
  #print(cancelallchildorders)
  #現在の注文状況をチェックする
  print("現在の建玉状況")
  positions = api.getpositions(product_code=productCode)
  print(positions)
  print("length:", len(positions))

  #現在注文中のBTCを売買する(買い注文なら売る。売り注文なら買う)
  ordered_side = ""
  if len(positions) > 0:
    for elem in positions:
      if elem["product_code"] == productCode:
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
#child_order_state:
# 次のいずれかを指定します。
# ACTIVE: オープンな注文の一覧を取得します。
# COMPLETED: 全額が取引完了した注文の一覧を取得します。
# CANCELED: お客様がキャンセルした注文です。
# EXPIRED: 有効期限に到達したため取り消された注文の一覧を取得します。
# REJECTED: 失敗した注文です。

print("現在のACTIVEな注文（建玉でない）")
childorders = api.getchildorders(product_code=productCode,child_order_state="ACTIVE")
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
