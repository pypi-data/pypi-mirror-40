import unittest

from source.model.pricing_data_reader import PricingDataReader
from utilities.constants import Constants
from utilities.query_sql import QuerySql


class PricingDataReaderTest(unittest.TestCase):

    def test_data_reader(self):
        result = PricingDataReader.read_raw_data(QuerySql.sql_query.get(Constants.SQL_APP_QUERY))
        self.assertTrue(len(result)>0)


