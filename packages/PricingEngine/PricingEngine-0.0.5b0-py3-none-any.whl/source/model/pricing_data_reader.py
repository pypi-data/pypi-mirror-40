import pandas as pd

from logger.logger_helper import LogHelper
from utilities.db_helper import DBHelper


class PricingDataReader:

    @staticmethod
    def read_raw_data(sql_query):
        # Open database connection
        con = DBHelper.connection()
        try:
            # replace sql query with pandas
            return pd.read_sql_query(sql_query, con)
            # Execute the SQL command
        except IOError as errorNo:
            LogHelper.get_logger().error(errorNo)
        # disconnect from server
        con.close()
