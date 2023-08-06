import logging

from utilities.constants import Constants


class LogHelper:

    def __init__(self):
        print("Init")
    # this is for error logging

    @staticmethod
    def get_logger():
        try:
            logging_label = Constants.SET_LOGGER
            logger = logging.getLogger('pricingEngine')
            # file path
            handler = logging.FileHandler(Constants.LOGGER_PATH)
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s  '
                                          'Method Name:- %(funcName)20s() :%(lineno)s  File Path: %(pathname)s')
            handler.setFormatter(formatter)
            if logger.hasHandlers():
                logger.handlers.clear()
            logger.addHandler(handler)
            logger.setLevel(logging_label)
            return logger
        except IOError as errorNo:
            print(errorNo)
