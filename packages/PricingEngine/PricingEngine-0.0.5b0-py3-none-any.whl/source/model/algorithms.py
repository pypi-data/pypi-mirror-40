import numpy as np
import pandas as pd
from pandas.compat import FileNotFoundError
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict

from logger.logger_helper import LogHelper
from source.controller.pricing_engine import PricingEngine
from source.model.data_analysis import DataAnalysis
from source.model.prediction import Prediction
from source.model.pricing_data_reader import PricingDataReader
from source.model.user_data_label_encode import UserDataLabelEncoding
from utilities.app_history import AppHistory
from utilities.constants import Constants
from utilities.helper import Helper
from utilities.query_sql import QuerySql


class Algorithms:
    accuracy = ''
    prediction = ''
    algorithm_name = ''

    def __init__(self, user_data=None):
        if user_data is not None:
            self.user_data = user_data
            self.temp_user_data = user_data
            Constants.MODEL_NEED_TO_TRAIN = int(
                Helper.get_config_file_data(Constants.MODEL_MANAGER, Constants.IS_DATA_TRAIN))

    # Method to read data.
    def read(self):
        choice_of_data = self.choice_of_data()

        parsed_data = self.data_manipulation(choice_of_data)
        return self.reject_outliers(parsed_data)

    @staticmethod
    def data_manipulation(pricing_data):
        filename = Constants.DATA_ENCODE_PATH

        # in this function remove null values and encode string to number and store it for user data
        # machining and encoding
        try:
            if Constants.MODEL_NEED_TO_TRAIN == Constants.TRUE:
                pricing_data = Helper.get_valid_data(pricing_data)
                obj_helper = Helper()
                pricing_data = obj_helper.generate_label_encoder(pricing_data)
                # change data type from int to float
                pricing_data = obj_helper.convert_to_float(Constants.PREDICTION_INPUT, pricing_data, 1)
                LogHelper.get_logger().info("Original Data label encoding complete")
                Helper.save_in_disk(filename, pricing_data)
            return Helper.open_saved_file_from_disk(filename)
        except Exception as err:
            LogHelper.get_logger().error(err)

    @staticmethod
    def scaling(data):
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler().fit(Constants.X_TRAIN)
        return scaler.transform(data)
        # summarize transformed data

    # This method receives the type of input ex: database/ Excel/ Csv etc.
    # And process according to it.
    @staticmethod
    def choice_of_data():
        raw_data_filename = Constants.RAW_DATA_FILENAME
        csv_path = Helper.get_config_file_data(Constants.PATHS_SECTION, 'csv_input_data_path')

        try:

            if Constants.MODEL_NEED_TO_TRAIN == Constants.TRUE:
                # if Constants.FLAG = 1 means model will be retrain
                if int(Helper.get_config_file_data(Constants.INPUT_DATABASE_CHOICE,
                                                   Constants.DATA_SELECTION)) == Constants.FALSE:
                    # if read mysql database
                    raw_data = PricingDataReader.read_raw_data(QuerySql.sql_query.get(Constants.SQL_APP_QUERY))
                    # below two line will save TagDisplayName is null because it's required
                    raw_data = raw_data[raw_data['TagDisplayName']=='NULL']
                    LogHelper.get_logger().info('raw_data read from mysql')
                else:
                    raw_data = pd.DataFrame(data=pd.read_csv(csv_path))
                    raw_data = raw_data[raw_data['TagDisplayName'].isnull()]

                    LogHelper.get_logger().info('raw_data read from csv')
                raw_data['TagDisplayName'] = 1
                raw_data = Helper.remove_blank_space(raw_data)
                Helper.save_in_disk(raw_data_filename, raw_data)

            return Helper.open_saved_file_from_disk(raw_data_filename)
        except FileNotFoundError as err:
            LogHelper.get_logger().error(err)

    # This method is user to filter the outlier vehicles.
    # Here I have replace the mean with the more robust median and the standard deviation with the absolute distance to
    # the median. I then scaled the distances by their (again) median value so that m is on a reasonable relative scale.
    @staticmethod
    def reject_outliers(data, m=3):
        from scipy import stats
        z = np.abs(stats.zscore(data))
        data = data[(z < m).all(axis=1)]
        data = data[abs(data - np.mean(data)) < m * np.std(data)]
        return data[~data.isin(['NaN']).any(axis=1)]

    # Method to split data.
    def split(self, data):

        try:
            data = data.drop([Constants.ID], axis=1)

            x_train, x_test, y_train, y_test = train_test_split(data.drop([Constants.PREDICTION_TARGET], axis=1),
                                                                data.loc[:, Constants.PREDICTION_TARGET],
                                                                test_size=Constants.TRAIN_TEST_SPLIT,
                                                                random_state=42)
            Constants.X_TRAIN = x_train
            return pd.DataFrame(data=self.scaling(x_train), columns=Constants.USER_INPUT), pd.DataFrame(
                data=self.scaling(x_test), columns=Constants.USER_INPUT), y_train, y_test
        except Exception as err:
            LogHelper.get_logger().error(err)

    def store_prediction_and_accuracy(self):
        data_obj = {'PredictedAccuracy': self.accuracy, 'PredictedValue': str(int(self.prediction[0])),
                    'AlgorithmName': self.algorithm_name, 'Remark': str(Constants.USER_INPUT),
                    'cross_validation': str(Constants.CROSS_VALIDATE_SCORE)}
        AppHistory.app_data.update(data_obj)
        _prediction = Prediction()
        _prediction.add_prediction(self.prediction, self.algorithm_name)
        _prediction.add_score(data_obj)
        LogHelper.get_logger().info(data_obj)
        # this is help to store details in database

    @staticmethod
    def store(target):
        pricing_engine = PricingEngine()
        pricing_engine.store_records(target)

    def user_data_label_encoding(self, user_data):
        user_data = UserDataLabelEncoding.user_data_label_encode(user_data)
        return user_data

    @staticmethod
    def cross_validation(x_data, algorithm_name):
        for column in list(x_data.columns):
            if column == Constants.ID:
                x_data = x_data[Constants.PREDICTION_INPUT].copy()
                x_data = x_data.drop([Constants.ID], axis=1)
        y_target = x_data.loc[:, Constants.PREDICTION_TARGET]
        model = Helper.open_saved_file_from_disk(Constants.SAVE_MODEL_PATH + algorithm_name + '.sav')
        scores = cross_val_score(model, x_data, y_target, cv=5)
        Constants.CROSS_VALIDATE_SCORE = list(scores)
        predictions = cross_val_predict(model, x_data, y_target, cv=5)
        data_analysis = DataAnalysis()
        data_analysis.simple_graph_plot(y_target, predictions, algorithm_name)
        LogHelper.get_logger().info({'cross validation score ': scores})

    # array name like this['random_forest_regression', 'gradient_boosting_regression']
    def run(self, algorithm_name_array, child_class_obj):
        try:
            pricing_data = self.read()

            x_train, x_test, y_train, y_test = self.split(pricing_data)

            self.user_data = self.scaling(self.user_data_label_encoding(self.user_data))
            self.user_data = pd.DataFrame(data=self.user_data, columns=Constants.USER_INPUT)
            if Constants.DATA_ENCODED_FAILED:
                return
            # self.mean_variance(pricing_data)
            Constants.TOTAL_ALGORITHMS = len(algorithm_name_array)
            for self.algorithm_name in algorithm_name_array:
                Constants.ALGORITHM_NAME = self.algorithm_name
                self.accuracy, self.prediction = getattr(child_class_obj(x_train, y_train, x_test, y_test,
                                                         self.user_data, self.algorithm_name),
                                                         self.algorithm_name)()

                if Constants.IS_CROSS_VALIDATION == Constants.TRUE:
                    # K -fold cross validation test on unknown dataset
                    data = pd.read_csv('temp_data/test.csv')
                    data = UserDataLabelEncoding.user_data_label_encode(data)
                    self.cross_validation(data, self.algorithm_name)

                self.store_prediction_and_accuracy()
                self.store(Constants.APP_HISTORY_QUERY)
                self.store(Constants.APP_SUMMARY_QUERY)
            # DataAnalysis.outlier_graph(pricing_data, 'data density test')
        except Exception as err:
            LogHelper.get_logger().debug(err)

    @staticmethod
    def mean_variance(data):
        feature_column = list(Constants.USER_INPUT)
        for column in feature_column:
            mean = np.mean(data[column])
            median = np.median(data[column])
            variance = np.var(data[column])
            print(column, ': Median: ', median, 'Mean', mean, 'Variance', variance)
            # data_analaysis.simple_graph_plot(data[column], 50, title=column, kind='hist')
