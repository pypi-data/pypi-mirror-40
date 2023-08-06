import unittest

from source.model.algorithms import Algorithms
from tests.prediction_test import PredictionTest


class AlgorithmTest(unittest.TestCase):
    algo = Algorithms(PredictionTest.user_data())
    user_data = PredictionTest.user_data()
    def test_read_and_raw_data_label_encoding(self):
        data = self.algo.read()
        self.assert_check(data)

    def test_user_data_label_encode(self):
        user_data = self.algo.user_data_label_encoding(self.user_data)
        self.assert_check(user_data)

    def assert_check(self, user_data):
        d = list(user_data['ModelName'])[0]
        self.assertTrue(type(d) == float)