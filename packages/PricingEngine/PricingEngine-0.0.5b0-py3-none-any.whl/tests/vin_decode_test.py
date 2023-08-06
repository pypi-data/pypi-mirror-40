import unittest
from source.model.vin_decode import VINDecoder
from utilities.constants import Constants


class VINDecodeTest(unittest.TestCase):

    def test_vin_decode(self):
        self.assertTrue(VINDecoder.vin_decode(Constants.VIN_NO))
