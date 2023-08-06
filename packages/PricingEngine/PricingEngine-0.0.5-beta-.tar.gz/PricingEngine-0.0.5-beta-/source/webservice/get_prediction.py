import tornado.web
import tornado.web

from app_runner import MainEntry
from logger.logger_helper import LogHelper
from source.controller.pricing_engine import PricingEngine
from source.model.get_user_data import GetUserData
from utilities.constants import Constants


class GetPrediction(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.write({"error": "Please Use Post method"}, )

    def post(self):
        try:
            result = self.show_output()
            self.write(result)
        except Exception as err:
            if Constants.DATA_ENCODED_FAILED:
                self.write(Constants.ERROR_DATA_NOT_ENOUGH)
                Constants.DATA_ENCODED_FAILED = False
                raise ValueError(Constants.ERROR_DATA_NOT_ENOUGH)

            else:
                self.write({"error": "Wrong data given"}, )
            LogHelper.get_logger().error(err)

    def show_output(self):
        try:
            user_input = ['vin', 'Mileage', 'MMRAvgValue', 'Color', 'AddrZip']
            user_value = {}
            get_user_data = GetUserData()
            for column_name in user_input:
                user_value.update({column_name: self.get_argument(column_name).title()})
            user_data = get_user_data.get_user_data(user_value)
            MainEntry.main_entry_point(user_data)
            pricing_engine = PricingEngine()
            if Constants.DATA_ENCODED_FAILED:
                LogHelper.get_logger().info(Constants.ERROR_DATA_NOT_ENOUGH)
                Constants.DATA_ENCODED_FAILED = False
                return Constants.ERROR_DATA_NOT_ENOUGH
            return {"accuracy_and_prediction": pricing_engine.get_accuracy_and_prediction(),
                    "range": pricing_engine.get_prediction_range()}

        except Exception as err:

            LogHelper.get_logger().error(err)
