import sys
sys.path[0:0] = [""]  ## NOTE: よくわからないけど、これがないと上位層のcsv_base がimport できない

import unittest
from csv_base import CsvBase ##TODO: it's failed

class TestCsvBase(unittest.TestCase):
    def test_get_total_earn_amount_in_usd(self):
        csv_base = CsvBase()
        #tests
        pipeline = [
            {
                "$match" : {
                    "transaction_kind" : "crypto_earn_interest_paid"
                }
            }
        ]
        test_total_amount = 0
        test_results = csv_base.mongo.test.cryptocom_transactions.aggregate(pipeline)
        for item in test_results:
            test_total_amount += item["native_amount_in_usd"]
        self.assertEqual(test_total_amount, total_amount, 'total_amount is not matched.')


if __name__ == "__main__":
    unittest.main()