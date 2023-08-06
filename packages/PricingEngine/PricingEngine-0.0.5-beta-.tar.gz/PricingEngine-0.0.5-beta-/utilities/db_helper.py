from logger.logger_helper import LogHelper
from sqlalchemy import create_engine, MetaData
from configuration.config import Config


class DBHelper:

    @staticmethod
    def connection():
        config = Config()
        config_object = config.get_db_credentials()

        url = 'mysql+mysqlconnector://' + config_object.dbuser_ + ':' + config_object.dbpwd_ + '@' + config_object.dbhost_ + '/' + config_object.dbname_
        meta = MetaData()
        meta.bind = url
        try:
            engine = create_engine(url)
            return engine.connect()
        # except
        except Exception as err:
            LogHelper.get_logger().error(err)
