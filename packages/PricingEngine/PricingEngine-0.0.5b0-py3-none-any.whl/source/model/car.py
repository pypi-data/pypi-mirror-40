from logger.logger_helper import LogHelper
# This is the object of the Car it contains all the required fields.


class Car:
    car_data = {}

    def __init__(self):
        self.VIN = ""
        self.Year = 0
        self.MakeName = ""
        self.ModelName = ""
        self.StyleName = ""
        self.Color = ""
        self.Mileage = 0
        self.AddrZip = 0
        self.MMRAvgValue = 0

    def add_car(self, vin, car):
        try:
            self.car_data.update({vin: car})
        except Exception as err:
            LogHelper.get_logger().error(err)

    def get_car_data_by_vin(self, vin):
        try:
            return self.car_data[vin]
        except ValueError as err:
            LogHelper.get_logger().error(err)
        except Exception as err:
            LogHelper.get_logger().error(err)
    # Example how to get values using Car class object car.getCarByVIN('VIN').'parameter'
