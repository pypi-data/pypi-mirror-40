import unittest

from app_runner import MainEntry
from source.controller.pricing_engine import PricingEngine
from source.model.get_user_data import GetUserData
from utilities.constants import Constants


class PredictionTest(unittest.TestCase):

    def test_prediction_range(self):
        MainEntry.main_entry_point(self.user_data())
        self.entry()
    def test_prediction_range_from_csv(self):
        MainEntry.main_entry_point(MainEntry.read_user_data_from_csv())
        self.entry()
    @staticmethod
    def user_data():
        user_input = ['vin', 'Mileage', 'MMRAvgValue', 'AddrZip']
        user_value = [Constants.VIN_NO, Constants.MILEAGE, Constants.MMR, Constants.ADDRESS_ZIP]
        data = {}
        for i in range(len(user_input)):
            data.update({user_input[i]: user_value[i]})
        return GetUserData.get_user_data(data)

    def entry(self):
        self.assertTrue(PricingEngine.get_prediction_range()['ACV Range']['begin'])