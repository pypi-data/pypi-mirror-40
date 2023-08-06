import requests
from logger.logger_helper import LogHelper
from source.model.car import Car
from utilities.constants import Constants
import json
from utilities.app_history import AppHistory


class VINDecoder:
    @staticmethod
    def vin_decode(vin):
        try:
            url = Constants.VIN_DECODE_URL
            post_vars1 = Constants.POST_VARIABLE_ONE
            post_vars2 = {
                "decoder_settings":
                    {
                        "display": "full",
                        "version": "7.0.1",
                        "styles": "on",
                        "style_data_packs": {

                            "basic_data": "on",
                            "pricing": "on",
                            "engines": "on",
                            "transmissions": "on",
                            "specifications": "on",
                            "installed_equipment": "on",
                            "optional_equipment": "off",
                            "colors": "on",
                            "safety_equipment": "on",
                            "warranties": "on",
                            "fuel_efficiency": "on",
                            "green_scores": "on",
                            "crash_test": "on",
                            "awards": "off"
                        },
                        "common_data": "on",
                        "common_data_packs": {
                            "basic_data": "on",
                            "pricing": "on",
                            "engines": "on",
                            "transmissions": "on",
                            "specifications": "on",
                            "installed_equipment": "on",
                            "optional_equipment": "on",
                            "colors": "on",
                            "safety_equipment": "on",
                            "warranties": "on",
                            "fuel_efficiency": "on",
                            "green_scores": "on",
                            "crash_test": "on",
                            "awards": "off"
                        }
                    },
                "query_requests": {
                    "Request-Sample": {
                        "vin": vin,
                        "year": "",
                        "make": "",
                        "model": "",
                        "trim": "",
                        "model_number": "",
                        "package_code": "",
                        "drive_type": "",
                        "vehicle_type": "",
                        "body_type": "",
                        "body_subtype": "",
                        "doors": "",
                        "bedlength": "",
                        "wheelbase": "",
                        "msrp": "",
                        "invoice_price": "",
                        "engine": {
                            "description": "",
                            "block_type": "",
                            "cylinders": "",
                            "displacement": "",
                            "fuel_type": ""
                        },
                        "transmission": {
                            "description": "",
                            "trans_type": "",
                            "trans_speeds": ""
                        },
                        "optional_equipment_codes": "",
                        "installed_equipment_descriptions": "",
                        "interior_color": {
                            "description": "",
                            "color_code": ""
                        },
                        "exterior_color": {
                            "description": "",
                            "color_code": ""
                        }
                    }
                }
            }
            post_vars = post_vars1 + json.dumps(post_vars2)
            # print(post_vars)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = requests.post(url, data=post_vars, headers=headers)
            result = result.json()
            # result got from DataOne API in json format
            year = result['query_responses']['Request-Sample']['us_market_data']['common_us_data']['basic_data']['year']
            make = result['query_responses']['Request-Sample']['us_market_data']['common_us_data']['basic_data']['make']
            model = result['query_responses']['Request-Sample']['us_market_data']['common_us_data']['basic_data'][
                'model']
            style = result['query_responses']['Request-Sample']['us_market_data']['us_styles'][0]['name']
            car = Car()
            # import re
            # model = re.sub(' ', '-', model)
            # make = re.sub(' ', '-', make)
            # style = re.sub(' ', '-', style)
            car.ModelName = model
            car.VIN = vin
            car.MakeName = make
            car.StyleName = style
            car.Year = year
            car.add_car(vin, car)
            log_message = {
                'method name': 'vin_decode',
                'vin': vin,
                'model': model,
                'make': make,
                'style': style
            }
            # vin_decode = {vin, model, make, style}
            # this is for store the data in database
            AppHistory.app_data['VIN'] = vin
            AppHistory.app_data['MakeName'] = make
            AppHistory.app_data['ModelName'] = model
            AppHistory.app_data['StyleName'] = style
            LogHelper.get_logger().info(log_message)
            return car.get_car_data_by_vin(vin)

        except Exception as err:
            LogHelper.get_logger().error(err)
            # 1D4HR38N53F552088
