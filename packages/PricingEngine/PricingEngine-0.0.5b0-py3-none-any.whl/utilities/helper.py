# All the general helper methods are kept here.
import configparser
import os
import pickle
import shutil

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from logger.logger_helper import LogHelper, Constants


class Helper:
    def __init__(self):
        self.range = []

    # This method fetches the required data from the dataset and returns the dataset.
    @staticmethod
    def get_valid_data(pricing_data):

        #  Removes all the null value
        pricing_data.dropna(inplace=True)
        pricing_data = Helper.filter_data(pricing_data)
        input_data = Constants.PREDICTION_INPUT
        columns = []
        for count in pricing_data.columns:
            columns.append(count.strip())
        result = {}
        for count in range(len(input_data)):
            result[input_data[count]] = pricing_data.loc[:, input_data[count].strip()]
        df = pd.DataFrame(data=result)
        return df

    # This method is used to filter the data according to the data filters specified.
    @staticmethod
    def filter_data(pricing_data):

        filter_values = Constants.DATA_FILTERS

        for count in range(len(filter_values)):
            pricing_data = pricing_data[pricing_data[filter_values[count][0]] > filter_values[count][1]]

        return pricing_data

    # This method encodes data to integer.
    def encode_data_to_int(self, value, pricing_data):
        label_encoder = LabelEncoder()
        temp_col = pricing_data.loc[:, value]
        pricing_data.loc[:, value] = label_encoder.fit_transform(pricing_data.loc[:, value])
        encoded_value = dict(zip(temp_col, pricing_data.loc[:, value]))
        return encoded_value, pricing_data

    # this method loops the value ang generates the label encoded value.
    def generate_label_encoder(self, pricing_data):
        filename = Constants.LABEL_ENCODE_TEMP
        arr_input = Constants.ENCODING_DATA
        obj_lable_encode = LabelEncodeStore()
        for count in range(len(arr_input)):
            encoded_value, pricing_data = self.encode_data_to_int(arr_input[count], pricing_data)
            obj_lable_encode.encoded_array.update({arr_input[count]: encoded_value})
        self.save_in_disk(filename, obj_lable_encode.encoded_array)

        return pricing_data

    # This method converts all the values to float.
    def convert_to_float(self, column_name, pricing_data, start_index=0):
        try:
            for count in range(start_index, len(column_name)):
                pricing_data[column_name[count]] = pricing_data[column_name[count]].astype(float)
            return pricing_data
        except Exception as err:
            LogHelper.get_logger().error(err)

    # This method is use to get data from config file
    @staticmethod
    def get_config_file_data(key, value=''):
        config = configparser.RawConfigParser()
        config_file_path = Constants.CONFIG_FILE_PATH
        config.read(config_file_path)
        if value == '':
            return dict(config.items(key))
        else:
            return config.get(key, value)

    @staticmethod
    def save_in_disk(filename, file_object):

        with open(filename, 'wb') as f:
            pickle.dump(file_object, f)

    # it will be return file object
    @staticmethod
    def open_saved_file_from_disk(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    #  this method is use to remove directory
    @staticmethod
    def remove_directory(path):
        if os.path.isdir(path):
            shutil.rmtree(path)

    # This methods is use to create directory if not exits.
    @staticmethod
    def crate_directory(full_path):
        os.makedirs(full_path, exist_ok=True)

    @staticmethod
    def remove_blank_space(pricing_data):
        # for column in Constants.ENCODING_DATA:
        #     for count in range(len(pricing_data)):
        #         pricing_data[column][count] = re.sub(' ', '-', pricing_data[column][count])
        return pricing_data


# this is for store label encode data in dict format
class LabelEncodeStore:
    encoded_array = {}
