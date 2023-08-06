# import matplotlib.pyplot as plt
# k_range = range(40, 52)
# scores = []
# for k in k_range:
#     # leaf_size , n_jobs has not effect 45, random_state=6, warm_start=True, min_samples_leaf=5
#     knn = RandomForestRegressor(n_estimators=k, random_state=5, min_samples_leaf=1, max_depth=21)
#
#     knn.fit(self.x_train, self.y_train)
#     scores.append(knn.score(self.x_test, self.y_test))
# plt.figure()
# plt.xlabel('k')
# plt.ylabel('accuracy')
# plt.scatter(k_range, scores)
# # plt.xticks([0, 15, 20, 25, 30, 35, 40, 50])
#
# plt.show()
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from source.model.data_analysis import DataAnalysis
from utilities.constants import Constants
from utilities.helper import Helper


class RegrassionTest:
    @staticmethod
    def random_forest_regrassion():
        data = pd.read_csv('D:/pricingengine/datasource/csv/ivv.csv')
        data = data[Constants.PREDICTION_INPUT].copy()
        pricing_data = Helper.get_valid_data(data)
        obj_helper = Helper()
        pricing_data = obj_helper.generate_label_encoder(pricing_data)
        # change data type from int to float
        data = pricing_data.drop([Constants.ID], axis=1)
        e_estimator = []
        randome_state = []
        c = 80
        for count in range(2, 10):
            e_estimator.append(c)
            c += 10

        c = 0
        for count in range(10, 150):
            c += 2
            randome_state.append(c+2)
        d = DataAnalysis()

        param_grid = [
            {'n_estimators': e_estimator, 'max_depth': e_estimator},
            # {'bootstrap':[False], 'n_estimators': e_estimator, 'max_depth':randome_state},
            # {'n_estimators': e_estimator, 'max_depth': randome_state, 'random_state': randome_state},
        ]
        x_train, x_test, y_train, y_test = train_test_split(data.drop([Constants.PREDICTION_TARGET], axis=1),
                                                            data.loc[:, Constants.PREDICTION_TARGET],
                                                            test_size=Constants.TRAIN_TEST_SPLIT,
                                                            random_state=42)
        rfr = RandomForestRegressor()
        print('wait.......')
        grid_search = GridSearchCV(rfr, param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(x_train, y_train)
        # print(grid_search.best_params_)
        # d.simple_graph_plot(grid_search.predict(x_test),y_test, 'test')
        from sklearn.ensemble import GradientBoostingRegressor
        gbr = GradientBoostingRegressor()
        rfr = RandomForestRegressor()
        gbr.fit(x_train, y_train)
        # d.simple_graph_plot(y_test, rfr.predict(x_test), 'without bagging')
        print(grid_search.score(x_test, y_test))
        baging = BaggingRegressor(grid_search)
        baging.fit(x_train, y_train)
        # d.simple_graph_plot(y_test, baging.predict(x_test), 'with bagging')

        print(baging.score(x_test, y_test))


RegrassionTest.random_forest_regrassion()