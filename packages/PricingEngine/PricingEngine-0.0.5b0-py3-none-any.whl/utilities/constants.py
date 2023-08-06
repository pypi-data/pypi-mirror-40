# All the constants used in this project are kept here.
import socket


class Constants:
    # SQL TABLES NAME
    SQL_APP_QUERY = 'sql_query_app'
    PREDICTION_RESULT_QUERY = 'prediction_result'
    APP_SUMMARY_QUERY = 'app_summary'
    APP_HISTORY_QUERY = 'app_history'
    # END SQL TABLES NAME
    CROSS_VALIDATE_SCORE = None

    # FOLDER NAME AUTO CREATED
    GRAPH_DIRECTORY = 'graph'
    TEMP_DIRECTORY = 'temp_data'
    SAVE_MODEL_DIRECTORY = 'savemodel'
    # FOLDER CREATION

    # FILE PATH
    LOGGER_PATH = 'logger/pricingEngine.log'
    CSV_INPUT_DATA_PATH = 'datasource/csv/test.csv'
    RAW_DATA_FILENAME = SAVE_MODEL_DIRECTORY+'/raw_data.sav'
    TEMP_USER_DATA_FILE_PATH = TEMP_DIRECTORY+'/test.csv'
    LABEL_ENCODE_TEMP = SAVE_MODEL_DIRECTORY+'/label_encode'
    USER_DATA = '/datasource/csv'
    DECISION_TREE_REGRESSION = SAVE_MODEL_DIRECTORY+'/DecisionTreeRegression.sav'
    DATA_ENCODE_PATH = SAVE_MODEL_DIRECTORY+'/data_encode.sav'
    CONFIG_FILE_PATH = 'configuration/config.properties'
    SAVE_MODEL_PATH = SAVE_MODEL_DIRECTORY+'/'
    MODEL_SAVE_FILE_EXTENSION = '.sav'

    # END FILE PATH
    INPUT_DATABASE_CHOICE = 'inputDatabaseChoice'
    DATA_SELECTION = 'dataSelection'
    MODEL_MANAGER = 'ModelManager'
    IS_DATA_TRAIN = 'isTrain'
    RUN_ALGORITHMS = ['x_g_boost_regression', 'random_forest_regression', 'gradient_boosting_regression']
    ID = 'id'
    MAX_MMR_IS = 0
    RESULT_EXPORT = 0
    SAVE_TEST_REPORT = 0
    VIN_COUNT = 0
    X_TRAIN = ''
    # RELATED TO PREDICTION HELPER
    PLATFORM = 'Scikit-learn'
    PREDICTION_TARGET = 'SalesPrice'
    # USER_INPUT and PREDICTION_INPUT columns name must be in same sequence
    # USER_INPUT = ['Mileage', 'Color', 'Year', 'MMRAvgValue', 'ModelName', 'MakeName', 'StyleName', 'AddrZip']
    USER_INPUT = ['Mileage', 'MMRAvgValue', 'ModelName', 'MakeName', 'StyleName']
    PREDICTION_INPUT = ['id', 'Mileage', 'MMRAvgValue', 'ModelName', 'MakeName', 'StyleName',
                        'SalesPrice']
    ENCODING_DATA = ['ModelName', 'MakeName', 'StyleName']

    AUCTION_SOLD_FOR_MINIMUM_LIMIT = 300
    ACV_MINIMUM_LIMIT = 300
    MMR_MINIMUM_LIMIT = 50
    # FLAG is use for check raw data changes or not
    FLAG = 1
    TRUE = 1
    FALSE = 0
    MODEL_NEED_TO_TRAIN = 1
    # Total algorithm used for prediction
    TOTAL_ALGORITHMS = 2
    DATA_ENCODED_FAILED = False
    # DATA_COLUMN = 8 means raw data have 8 columns
    DATA_COLUMN = 8
    TOTAL_DATA_LENGTH = 7752
    TRAIN_TEST_SPLIT = 0.20
    VIN_NO = '1D4HR38N53F552088'
    MILEAGE = '165282'
    COLOR = 'Black'
    MMR = 500
    ALGORITHM_NAME = 'AlgorithmName'
    ADDRESS_ZIP = '95340'
    # END RELATED TO PREDICTION HELPER

    # VIN DECIDE URL
    VIN_DECODE_URL = 'https://api.dataonesoftware.com/webservices/vindecoder/decode'
    POST_VARIABLE_ONE = "client_id=12864&authorization_code=2dc00d18b69b68c8922163fa95a2711b25a2fc00&decoder_query="
    # END VIND DECODE URL

    DATA_FILTERS = [['SalesPrice', AUCTION_SOLD_FOR_MINIMUM_LIMIT], ['MMRAvgValue', MMR_MINIMUM_LIMIT]]
    USER_DATA_CSV = 0  # if USER_DATA_CSV = 1 then read user data from csv

    # ENVIRONMENT
    ENVIRONMENT = {'EnvKey': 'envName'}
    DEV_IP = '172.31.33.13'
    PROD_IP = '172.31.33.138'
    LOCAL_IP = socket.gethostbyname(socket.gethostname())
    SET_LOGGER = 'DEBUG'
    # END ENVIRONMENT

    # DATABASE SECTION
    DATABASE_SECTION = 'DatabaseSection'
    DATABASE_USER = 'databaseUser'
    DATABASE_PWD = 'databasePwd'
    DATABASE_HOST = 'databaseHost'
    DATABASE_NAME = 'databaseName'
    PATHS_SECTION = 'Paths'
    # END DATABASE SECTION

    # ERROR MESSAGE
    ERROR_DATA_NOT_ENOUGH = {"error": "Sorry, we can't predict of this car because <br/>"
                                      "We do not have enough information of this car"}
    TEMP = []
    SALES_PRICE = ''
    IS_CROSS_VALIDATION = 0
    APP_SUMMARY_QUERY_COLUMN = ['Platform', 'AlgoName', 'PredictedField', 'PredictedValue', 'MMRAvgValue', 'VIN',
                                'MakeName', 'ModelName', 'StyleName', 'Color', 'AddrZip', 'Mileage']
