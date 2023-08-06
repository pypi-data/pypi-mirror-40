from logger.logger_helper import LogHelper
from utilities.db_helper import DBHelper


class DataWriter:

    def data_writer(self, sql_query, values):
        # Open database connection
        con = DBHelper.connection()
        try:
            return con.execute(sql_query, values)
            # con.commit()
        # Execute the SQL command
        except IOError as errorNo:
            LogHelper.get_logger().debug(errorNo)
        except Exception as err:
            LogHelper.get_logger().debug(err)
        finally:
            con.close()
        # disconnect from server
