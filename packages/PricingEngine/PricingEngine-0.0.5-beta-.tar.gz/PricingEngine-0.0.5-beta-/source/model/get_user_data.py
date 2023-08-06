from logger.logger_helper import LogHelper
from source.controller.pricing_engine import PricingEngine
from source.model.car import Car
from utilities.constants import Constants
from utilities.app_history import AppHistory


class GetUserData:
    @staticmethod
    def create_vehicle_data(car, vin):
        vehicle_data = {}
        arr_user_input = Constants.USER_INPUT
        for count in range(len(arr_user_input)):
            result = [getattr(car.get_car_data_by_vin(vin), arr_user_input[count])]
            vehicle_data.update({arr_user_input[count]: result})
            AppHistory.app_data.update(
                {arr_user_input[count]: result[0]})
        return vehicle_data

    @staticmethod
    def get_user_data(user_data):
        try:
            vin = user_data.get('vin')
            car = Car()
            PricingEngine.get_vehicle_info(vin)
            for column in user_data:
                setattr(car.get_car_data_by_vin(vin), column, user_data.get(column))
            vehicle_data = GetUserData.create_vehicle_data(car, vin)
            return vehicle_data

        except Exception as err:
            LogHelper.get_logger().error(err)
