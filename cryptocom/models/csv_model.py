from datetime import datetime

class CsvModel:
    def __init__(self, time_stamp: datetime, transaction_description: str,
     currency: str, amount: float, to_currency: str, to_amount: float, native_currency: str,
     native_amount: float, native_amount_in_usd: float, transaction_kind: str):
        self.time_stamp = time_stamp
        self.transaction_description = transaction_description
        self.currency = currency
        self.amount = amount
        self.to_currency = to_currency
        self.to_amount = to_amount
        self.native_currency = native_currency
        self.native_amount = native_amount
        self.native_amount_in_usd = native_amount_in_usd
        self.transaction_kind = transaction_kind