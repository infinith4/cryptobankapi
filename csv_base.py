import sys
import os
from utils.Config import Config
import datetime
from pymongo import MongoClient
import logging
from pprint import pprint
from cryptocom.utils.csv_reader import CsvReader
from cryptocom.models.csv_model import CsvModel
#import dnspython
class CsvBase:

    def __init__(self, config_file:str= "app_config.yml"):
        self.config = Config(configFile).content
        mongo_username = config["MONGODB"]["USER_NAME"]
        mongo_password = config["MONGODB"]["PASSWORD"]
        connectionstr = 'mongodb+srv://%s:%s@cluster0-xhjo9.mongodb.net/test?retryWrites=true&w=majority' % (mongo_username, mongo_password)
        self.mongo = MongoClient(connectionstr)
    
    def get_total_earn_amount_in_usd(self):
            pipeline = [
            {
                "$match" : {
                    "transaction_kind" : "crypto_earn_interest_paid"
                }
            },
            {
                "$group": {
                    "_id": "$transaction_kind",
                    "total_amount": { "$sum": "$native_amount_in_usd" }
                }
            },
            {
                "$sort": {
                    "time_stamp": 1 
                }
            }
        ]
        results = mongo.test.cryptocom_transactions.aggregate(pipeline)
        total_amount = 0
        for item in results:
            total_amount = item["total_amount"]

        return total_amount

if __name__ == '__main__':
    csvBase = CsvBase()
    total_earn_amount = csvBase.get_total_earn_amount()



    cryptocom_csv_file_path = "csv_files/cryptocom/crypto_transactions_record_20200801_101854.csv"  ##TODO: search directory
    csvReader = CsvReader(cryptocom_csv_file_path)
    csv_list = csvReader.get_csv_list()
    csv_header = csvReader.get_csv_header()

    for csv_item in csv_list:
        data = {
                "time_stamp": csv_item.time_stamp , "transaction_description": csv_item.transaction_description, "currency": csv_item.currency,
                "amount": csv_item.amount, "to_currency": csv_item.to_currency, "to_amount": csv_item.to_amount, 
                "native_currency": csv_item.native_currency, "native_amount": csv_item.native_amount, "native_amount_in_usd": csv_item.native_amount_in_usd,
                "transaction_kind": csv_item.transaction_kind
            }
        record = mongo.test.cryptocom_transactions.find_one(data)
        #pprint(record)
        if record == None:
            mongo.test.cryptocom_transactions.insert(data)
            print("inserted")


        