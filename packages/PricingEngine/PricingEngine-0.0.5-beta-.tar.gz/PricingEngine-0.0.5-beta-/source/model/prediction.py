import numpy as np
from logger.logger_helper import LogHelper
from utilities.constants import Constants
# This is the object of the Prediction it contains the result of algorithm.


class Prediction:

    prediction_range = []
    prediction_with_algorithm_name = {}
    accuracy = {}

    # this function have two parameter one is prediction other is algorithm name
    def add_prediction(self, prediction, algorithm):
        try:
            if len(self.prediction_range) == Constants.TOTAL_ALGORITHMS:
                self.prediction_range.clear()
                self.prediction_with_algorithm_name.clear()
                self.accuracy.clear()
            self.prediction_range.append(prediction[0])
            self.prediction_with_algorithm_name.update({algorithm: prediction[0]})
        except RuntimeError as err:
            LogHelper.get_logger().error(err)
        except Exception as err:
            LogHelper.get_logger().error(err)

    """get_prediction_range will be return car price range begin and end"""
    def get_prediction_range(self):
        try:
            self.prediction_range.sort()

            result = {
                'begin': self.prediction_range[0],
                'end': np.floor(np.mean(self.prediction_range)),
            }
            result = {"ACV Range": result}
            return result
        except Exception as err:
            LogHelper.get_logger().error(err)

    """get_prediction will be return car price mean value"""
    def get_prediction(self):
        try:
            return np.mean(self.prediction_range)
        except Exception as err:
            LogHelper.get_logger().error(err)

    """get_all_prediction method will be return algorithm name with predicted price"""
    def get_all_prediction(self):
        try:
            return self.prediction_with_algorithm_name
        except Exception as err:
            LogHelper.get_logger().error(err)

    # function have one parameter accuracy
    # withing accuracy have two dist value algo and accuracy of that algo
    def add_score(self, score):
        self.accuracy.update({score['AlgorithmName']: score['PredictedAccuracy']})

    # get_accuracy method is return accuracy of dataset
    def get_accuracy(self):
        return self.accuracy
