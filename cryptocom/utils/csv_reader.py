import csv
from datetime import datetime

from cryptocom.models.csv_model import CsvModel

class CsvReader:
    def __init__(self, filePath: str):
        self.csv_list = []
        with open(filePath) as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter=',')
            self.header = next(reader)
            for row in reader:
                record = CsvModel(
                    time_stamp=datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'),
                    transaction_description=row[1],
                    currency=row[2],
                    amount=float(row[3]),
                    to_currency=row[4],
                    to_amount=float(row[5]) if row[5] != "" else 0,
                    native_currency=row[6],
                    native_amount=float(row[7]),
                    native_amount_in_usd=float(row[8]),
                    transaction_kind=row[9])
                self.csv_list.append(record)

    def get_csv_list(self):
        return self.csv_list

    def get_csv_header(self):
        return self.header

    # def get_csv_header_key(self):
    #     return ["time_stamp, 