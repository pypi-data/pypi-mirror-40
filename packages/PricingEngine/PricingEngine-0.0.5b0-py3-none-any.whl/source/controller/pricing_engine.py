from source.model.data_writer import DataWriter
from source.model.prediction import Prediction
from source.model.vin_decode import VINDecoder
from utilities.app_history import AppHistory
from utilities.query_sql import QuerySql


class PricingEngine:

    def __init__(self):
        self.data_writer_obj = DataWriter()

    # This method fetches the information of a vehicle from database or else from api.
    @staticmethod
    def get_vehicle_info(vin):
        return VINDecoder.vin_decode(vin)  # Getting vin details from api

    # This method gives the prediction range of the car.
    @staticmethod
    def get_prediction_range():
        prediction = Prediction()
        return prediction.get_prediction_range()

    # This method gives the accuracy in percentage and the predicted price of a Car.
    # get_accuracy_and_prediction will return accuracy and prediction
    # just call get_accuracy_and_prediction() only

    @staticmethod
    def get_accuracy_and_prediction():
        prediction = Prediction()
        data = {
            'Accuracy': prediction.get_accuracy(),
            'Prediction': prediction.get_all_prediction()
        }
        return data

    @staticmethod
    def app_history_values():
        app_data = AppHistory.app_data
        return (app_data['Platform'], app_data['AlgorithmName'], app_data['PredictedField'],
                app_data['PredictedValue'], app_data['MMRAvgValue'], app_data['VIN'],
                app_data['MakeName'], app_data['ModelName'], app_data['StyleName'], app_data['Color'],
                app_data['AddrZip'], app_data['Mileage'])

    @staticmethod
    def app_summary_values():
        app_data = AppHistory.app_data
        app_summery_values = (app_data['Platform'], app_data['AlgorithmName'], app_data['PredictedAccuracy'],
                              app_data['cross_validation'], app_data['Remark'])
        return app_summery_values

    @staticmethod
    def prediction_result_values():
        app_data = AppHistory.app_data
        values = (app_data['Vehicle_id'], app_data['Platform'], app_data['AlgorithmName'], app_data['PredictedField'],
                  app_data['PredictedValue'])
        return values

    def store_records(self, table_name):
        value = getattr(self, table_name+'_values')()
        query = QuerySql.sql_query.get(table_name)
        self.data_writer_obj.data_writer(query, value)


