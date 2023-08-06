import unittest

from source.model.data_writer import DataWriter
from utilities.query_sql import QuerySql, Constants


class DataWriterTest(unittest.TestCase):
    def test_app_data_read(self):
        data_write = DataWriter()
        data_write.data_writer(QuerySql.sql_query.get(Constants.APP_SUMMARY_QUERY), ('test', 'test', 'test', 'test', 'test'))
        a = data_write.data_writer('select * from app_summary where Algorithms=%s', 'test')
        for row in a:
            self.assertTrue(row['Algorithms'] == 'test')
        data_write.data_writer('delete from app_summary where Algorithms=%s', 'test')
