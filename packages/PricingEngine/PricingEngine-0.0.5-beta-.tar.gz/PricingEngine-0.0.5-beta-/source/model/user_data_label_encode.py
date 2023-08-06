import pandas as pd

from logger.logger_helper import LogHelper
from utilities.constants import Constants
from utilities.helper import Helper


class UserDataLabelEncoding:
    # User data encode respect to corresponding value
    @staticmethod
    def user_data_label_encode(user_data):
        try:
            main_user_data = pd.DataFrame(data=user_data)
            user_data = main_user_data[Constants.ENCODING_DATA].copy()
            encode_data = Constants.ENCODING_DATA
            encoded_array = Helper.open_saved_file_from_disk(Constants.LABEL_ENCODE_TEMP)
            for count in range(len(encode_data)):
                data = encoded_array.get(encode_data[count]).get(user_data[encode_data[count]].values[0])
                if data is None:
                    Constants.DATA_ENCODED_FAILED = True
                    return
                user_data[encode_data[count]] = data
            main_user_data.update(user_data)

            msg = "User Data label encoding completed"
            LogHelper.get_logger().info(msg)
            obj_helper = Helper()
            return obj_helper.convert_to_float(Constants.USER_INPUT, main_user_data)
        except Exception as err:
            LogHelper.get_logger().error(err)
