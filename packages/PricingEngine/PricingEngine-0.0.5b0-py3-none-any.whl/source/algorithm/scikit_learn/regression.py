import numpy as np
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

from logger.logger_helper import LogHelper
from source.algorithm.scikit_learn.regrassion_fine_tune import RegrassionFineTune
from source.model.algorithms import Algorithms
from utilities.constants import Constants
from utilities.helper import Helper


class Regression(Algorithms):
    def __init__(self, x_train, y_train, x_test, y_test, user_data, algorithm_name):
        Constants.MAX_MMR_IS = max(x_train['MMRAvgValue'])
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.user_data = user_data
        self.filename = Constants.SAVE_MODEL_PATH + algorithm_name + Constants.MODEL_SAVE_FILE_EXTENSION
        self.regrassion_fine_tuneing = RegrassionFineTune()
    # random forest regression algorithm implemented

    def random_forest_regression(self):
        try:
            if Constants.MODEL_NEED_TO_TRAIN == Constants.TRUE:
                # Parameters
                #     ----------
                #     n_estimators : integer, optional (default=10)
                #         The number of trees in the forest.
                #
                #     criterion : string, optional (default="mse")
                #         The function to measure the quality of a split. Supported criteria
                #         are "mse" for the mean squared error, which is equal to variance
                #         reduction as feature selection criterion, and "mae" for the mean
                #         absolute error.
                #
                #         .. versionadded:: 0.18
                #            Mean Absolute Error (MAE) criterion.
                #
                #     max_features : int, float, string or None, optional (default="auto")
                #         The number of features to consider when looking for the best split:
                #
                #         - If int, then consider `max_features` features at each split.
                #         - If float, then `max_features` is a percentage and
                #           `int(max_features * n_features)` features are considered at each
                #           split.
                #         - If "auto", then `max_features=n_features`.
                #         - If "sqrt", then `max_features=sqrt(n_features)`.
                #         - If "log2", then `max_features=log2(n_features)`.
                #         - If None, then `max_features=n_features`.
                #
                #         Note: the search for a split does not stop until at least one
                #         valid partition of the node samples is found, even if it requires to
                #         effectively inspect more than ``max_features`` features.
                #
                #     max_depth : integer or None, optional (default=None)
                #         The maximum depth of the tree. If None, then nodes are expanded until
                #         all leaves are pure or until all leaves contain less than
                #         min_samples_split samples.
                #
                #     min_samples_split : int, float, optional (default=2)
                #         The minimum number of samples required to split an internal node:
                #
                #         - If int, then consider `min_samples_split` as the minimum number.
                #         - If float, then `min_samples_split` is a percentage and
                #           `ceil(min_samples_split * n_samples)` are the minimum
                #           number of samples for each split.
                #
                #         .. versionchanged:: 0.18
                #            Added float values for percentages.
                #
                #     min_samples_leaf : int, float, optional (default=1)
                #         The minimum number of samples required to be at a leaf node:
                #
                #         - If int, then consider `min_samples_leaf` as the minimum number.
                #         - If float, then `min_samples_leaf` is a percentage and
                #           `ceil(min_samples_leaf * n_samples)` are the minimum
                #           number of samples for each node.
                #
                #         .. versionchanged:: 0.18
                #            Added float values for percentages.
                #
                #     min_weight_fraction_leaf : float, optional (default=0.)
                #         The minimum weighted fraction of the sum total of weights (of all
                #         the input samples) required to be at a leaf node. Samples have
                #         equal weight when sample_weight is not provided.
                #
                #     max_leaf_nodes : int or None, optional (default=None)
                #         Grow trees with ``max_leaf_nodes`` in best-first fashion.
                #         Best nodes are defined as relative reduction in impurity.
                #         If None then unlimited number of leaf nodes.
                #
                #     min_impurity_split : float,
                #         Threshold for early stopping in tree growth. A node will split
                #         if its impurity is above the threshold, otherwise it is a leaf.
                #
                #         .. deprecated:: 0.19
                #            ``min_impurity_split`` has been deprecated in favor of
                #            ``min_impurity_decrease`` in 0.19 and will be removed in 0.21.
                #            Use ``min_impurity_decrease`` instead.
                #
                #     min_impurity_decrease : float, optional (default=0.)
                #         A node will be split if this split induces a decrease of the impurity
                #         greater than or equal to this value.
                #
                #         The weighted impurity decrease equation is the following::
                #
                #             N_t / N * (impurity - N_t_R / N_t * right_impurity
                #                                 - N_t_L / N_t * left_impurity)
                #
                #         where ``N`` is the total number of samples, ``N_t`` is the number of
                #         samples at the current node, ``N_t_L`` is the number of samples in the
                #         left child, and ``N_t_R`` is the number of samples in the right child.
                #
                #         ``N``, ``N_t``, ``N_t_R`` and ``N_t_L`` all refer to the weighted sum,
                #         if ``sample_weight`` is passed.
                #
                #         .. versionadded:: 0.19
                #
                #     bootstrap : boolean, optional (default=True)
                #         Whether bootstrap samples are used when building trees.
                #
                #     oob_score : bool, optional (default=False)
                #         whether to use out-of-bag samples to estimate
                #         the R^2 on unseen data.
                #
                #     n_jobs : integer, optional (default=1)
                #         The number of jobs to run in parallel for both `fit` and `predict`.
                #         If -1, then the number of jobs is set to the number of cores.
                #
                #     random_state : int, RandomState instance or None, optional (default=None)
                #         If int, random_state is the seed used by the random number generator;
                #         If RandomState instance, random_state is the random number generator;
                #         If None, the random number generator is the RandomState instance used
                #         by `np.random`.
                #
                #     verbose : int, optional (default=0)
                #         Controls the verbosity of the tree building process.
                #
                #     warm_start : bool, optional (default=False)
                #         When set to ``True``, reuse the solution of the previous call to fit
                #         and add more estimators to the ensemble, otherwise, just fit a whole
                #         new forest.
                #
                #     Attributes
                #     ----------
                #     estimators_ : list of DecisionTreeRegressor
                #         The collection of fitted sub-estimators.
                #
                #     feature_importances_ : array of shape = [n_features]
                #         The feature importances (the higher, the more important the feature).
                #
                #     n_features_ : int
                #         The number of features when ``fit`` is performed.
                #
                #     n_outputs_ : int
                #         The number of outputs when ``fit`` is performed.
                #
                #     oob_score_ : float
                #         Score of the training dataset obtained using an out-of-bag estimate.
                #
                #     oob_prediction_ : array of shape = [n_samples]
                #         Prediction computed with out-of-bag estimate on the training set.
                rfr = RandomForestRegressor()
                rfr = self.regrassion_fine_tuneing.randome_forest(rfr)
                self.bagging_regrassion(rfr)
            return self.get_prediction_accuracy()
        except Exception as err:
            LogHelper.get_logger().error(err)

    # gradient_boosting_regression method for fit and predict data
    def gradient_boosting_regression(self):
        try:
            if Constants.MODEL_NEED_TO_TRAIN == Constants.TRUE:
                # Parameters
                #     ----------
                #     loss : {'ls', 'lad', 'huber', 'quantile'}, optional (default='ls')
                #         loss function to be optimized. 'ls' refers to least squares
                #         scikit_learn. 'lad' (least absolute deviation) is a highly robust
                #         loss function solely based on order information of the input
                #         variables. 'huber' is a combination of the two. 'quantile'
                #         allows quantile scikit_learn (use `alpha` to specify the quantile).
                #
                #     learning_rate : float, optional (default=0.1)
                #         learning rate shrinks the contribution of each tree by `learning_rate`.
                #         There is a trade-off between learning_rate and n_estimators.
                #
                #     n_estimators : int (default=100)
                #         The number of boosting stages to perform. Gradient boosting
                #         is fairly robust to over-fitting so a large number usually
                #         results in better performance.
                #
                #     max_depth : integer, optional (default=3)
                #         maximum depth of the individual scikit_learn estimators. The maximum
                #         depth limits the number of nodes in the tree. Tune this parameter
                #         for best performance; the best value depends on the interaction
                #         of the input variables.
                #
                #     criterion : string, optional (default="friedman_mse")
                #         The function to measure the quality of a split. Supported criteria
                #         are "friedman_mse" for the mean squared error with improvement
                #         score by Friedman, "mse" for mean squared error, and "mae" for
                #         the mean absolute error. The default value of "friedman_mse" is
                #         generally the best as it can provide a better approximation in
                #         some cases.
                #
                #         .. versionadded:: 0.18
                #
                #     min_samples_split : int, float, optional (default=2)
                #         The minimum number of samples required to split an internal node:
                #
                #         - If int, then consider `min_samples_split` as the minimum number.
                #         - If float, then `min_samples_split` is a percentage and
                #           `ceil(min_samples_split * n_samples)` are the minimum
                #           number of samples for each split.
                #
                #         .. versionchanged:: 0.18
                #            Added float values for percentages.
                #
                #     min_samples_leaf : int, float, optional (default=1)
                #         The minimum number of samples required to be at a leaf node:
                #
                #         - If int, then consider `min_samples_leaf` as the minimum number.
                #         - If float, then `min_samples_leaf` is a percentage and
                #           `ceil(min_samples_leaf * n_samples)` are the minimum
                #           number of samples for each node.
                #
                #         .. versionchanged:: 0.18
                #            Added float values for percentages.
                #
                #     min_weight_fraction_leaf : float, optional (default=0.)
                #         The minimum weighted fraction of the sum total of weights (of all
                #         the input samples) required to be at a leaf node. Samples have
                #         equal weight when sample_weight is not provided.
                #
                #     subsample : float, optional (default=1.0)
                #         The fraction of samples to be used for fitting the individual base
                #         learners. If smaller than 1.0 this results in Stochastic Gradient
                #         Boosting. `subsample` interacts with the parameter `n_estimators`.
                #         Choosing `subsample < 1.0` leads to a reduction of variance
                #         and an increase in bias.
                #
                #     max_features : int, float, string or None, optional (default=None)
                #         The number of features to consider when looking for the best split:
                #
                #         - If int, then consider `max_features` features at each split.
                #         - If float, then `max_features` is a percentage and
                #           `int(max_features * n_features)` features are considered at each
                #           split.
                #         - If "auto", then `max_features=n_features`.
                #         - If "sqrt", then `max_features=sqrt(n_features)`.
                #         - If "log2", then `max_features=log2(n_features)`.
                #         - If None, then `max_features=n_features`.
                #
                #         Choosing `max_features < n_features` leads to a reduction of variance
                #         and an increase in bias.
                #
                #         Note: the search for a split does not stop until at least one
                #         valid partition of the node samples is found, even if it requires to
                #         effectively inspect more than ``max_features`` features.
                #
                #     max_leaf_nodes : int or None, optional (default=None)
                #         Grow trees with ``max_leaf_nodes`` in best-first fashion.
                #         Best nodes are defined as relative reduction in impurity.
                #         If None then unlimited number of leaf nodes.
                #
                #     min_impurity_split : float,
                #         Threshold for early stopping in tree growth. A node will split
                #         if its impurity is above the threshold, otherwise it is a leaf.
                #
                #         .. deprecated:: 0.19
                #            ``min_impurity_split`` has been deprecated in favor of
                #            ``min_impurity_decrease`` in 0.19 and will be removed in 0.21.
                #            Use ``min_impurity_decrease`` instead.
                #
                #     min_impurity_decrease : float, optional (default=0.)
                #         A node will be split if this split induces a decrease of the impurity
                #         greater than or equal to this value.
                #
                #         The weighted impurity decrease equation is the following::
                #
                #             N_t / N * (impurity - N_t_R / N_t * right_impurity
                #                                 - N_t_L / N_t * left_impurity)
                #
                #         where ``N`` is the total number of samples, ``N_t`` is the number of
                #         samples at the current node, ``N_t_L`` is the number of samples in the
                #         left child, and ``N_t_R`` is the number of samples in the right child.
                #
                #         ``N``, ``N_t``, ``N_t_R`` and ``N_t_L`` all refer to the weighted sum,
                #         if ``sample_weight`` is passed.
                #
                #         .. versionadded:: 0.19
                #
                #     alpha : float (default=0.9)
                #         The alpha-quantile of the huber loss function and the quantile
                #         loss function. Only if ``loss='huber'`` or ``loss='quantile'``.
                #
                #     init : BaseEstimator, None, optional (default=None)
                #         An estimator object that is used to compute the initial
                #         predictions. ``init`` has to provide ``fit`` and ``predict``.
                #         If None it uses ``loss.init_estimator``.
                #
                #     verbose : int, default: 0
                #         Enable verbose output. If 1 then it prints progress and performance
                #         once in a while (the more trees the lower the frequency). If greater
                #         than 1 then it prints progress and performance for every tree.
                #
                #     warm_start : bool, default: False
                #         When set to ``True``, reuse the solution of the previous call to fit
                #         and add more estimators to the ensemble, otherwise, just erase the
                #         previous solution.
                #
                #     random_state : int, RandomState instance or None, optional (default=None)
                #         If int, random_state is the seed used by the random number generator;
                #         If RandomState instance, random_state is the random number generator;
                #         If None, the random number generator is the RandomState instance used
                #         by `np.random`.
                #
                #     presort : bool or 'auto', optional (default='auto')
                #         Whether to presort the data to speed up the finding of best splits in
                #         fitting. Auto mode by default will use presorting on dense data and
                #         default to normal sorting on sparse data. Setting presort to true on
                #         sparse data will raise an error.
                #
                #         .. versionadded:: 0.17
                #            optional parameter *presort*.
                #
                #     Attributes
                #     ----------
                #     feature_importances_ : array, shape = [n_features]
                #         The feature importances (the higher, the more important the feature).
                #
                #     oob_improvement_ : array, shape = [n_estimators]
                #         The improvement in loss (= deviance) on the out-of-bag samples
                #         relative to the previous iteration.
                #         ``oob_improvement_[0]`` is the improvement in
                #         loss of the first stage over the ``init`` estimator.
                #
                #     train_score_ : array, shape = [n_estimators]
                #         The i-th score ``train_score_[i]`` is the deviance (= loss) of the
                #         model at iteration ``i`` on the in-bag sample.
                #         If ``subsample == 1`` this is the deviance on the training data.
                #
                #     loss_ : LossFunction
                #         The concrete ``LossFunction`` object.
                #
                #     init : BaseEstimator
                #         The estimator that provides the initial predictions.
                #         Set via the ``init`` argument or ``loss.init_estimator``.
                #
                #     estimators_ : ndarray of DecisionTreeRegressor, shape = [n_estimators, 1]
                #         The collection of fitted sub-estimators.
                gbr = GradientBoostingRegressor()
                gbr = self.regrassion_fine_tuneing.gradient_boosting(gbr)
                self.bagging_regrassion(gbr)
            return self.get_prediction_accuracy()
        except Exception as err:
            LogHelper.get_logger().error(err)

    # x_g_boost_regression method for fit and predict data
    def x_g_boost_regression(self):
        try:
            if Constants.MODEL_NEED_TO_TRAIN == Constants.TRUE:
                # Parameters
                #         ----------
                #         max_depth : int
                #             Maximum tree depth for base learners.
                #         learning_rate : float
                #             Boosting learning rate (xgb's "eta")
                #         n_estimators : int
                #             Number of boosted trees to fit.
                #         silent : boolean
                #             Whether to print messages while running boosting.
                #         objective : string
                #             Specify the learning task and the corresponding learning objective.
                #             Only "rank:pairwise" is supported currently.
                #         booster: string
                #             Specify which booster to use: gbtree, gblinear or dart.
                #         nthread : int
                #             Number of parallel threads used to run xgboost.  (Deprecated, please use ``n_jobs``)
                #         n_jobs : int
                #             Number of parallel threads used to run xgboost.  (replaces ``nthread``)
                #         gamma : float
                #             Minimum loss reduction required to make a further partition on a leaf node of the tree.
                #         min_child_weight : int
                #             Minimum sum of instance weight(hessian) needed in a child.
                #         max_delta_step : int
                #             Maximum delta step we allow each tree's weight estimation to be.
                #         subsample : float
                #             Subsample ratio of the training instance.
                #         colsample_bytree : float
                #             Subsample ratio of columns when constructing each tree.
                #         colsample_bylevel : float
                #             Subsample ratio of columns for each split, in each level.
                #         reg_alpha : float (xgb's alpha)
                #             L1 regularization term on weights
                #         reg_lambda : float (xgb's lambda)
                #             L2 regularization term on weights
                #         scale_pos_weight : float
                #             Balancing of positive and negative weights.
                #         base_score:
                #             The initial prediction score of all instances, global bias.
                #         seed : int
                #             Random number seed.  (Deprecated, please use random_state)
                #         random_state : int
                #             Random number seed.  (replaces seed)
                #         missing : float, optional
                #             Value in the data which needs to be present as a missing value. If
                #             None, defaults to np.nan.
                xgb = XGBRegressor()
                xgb = self.regrassion_fine_tuneing.x_g_boost(xgb)
                self.bagging_regrassion(xgb)
            return self.get_prediction_accuracy()
        except Exception as err:
            LogHelper.get_logger().error(err)

    # # k_neighbors_regression method for fit and predict data
    # def k_neighbors_regression(self):
    #     try:
    #         if Constants.MODEL_NEED_TO_TRAIN == Constants.TRUE:
    #             knn = KNeighborsRegressor(n_neighbors=10, p=4)
    #             self.fit_for_training(knn)
    #         return self.get_prediction_accuracy()
    #     except Exception as err:
    #         LogHelper.get_logger().error(err)

    def bagging_regrassion(self, model):
        bagging = BaggingRegressor(model)
        bagging = self.regrassion_fine_tuneing.bagging_tuning(bagging)
        self.fit_for_training(bagging)

    # get prediction result and test accuracy
    def get_prediction_accuracy(self):
        try:
            # data_analysis = DataAnalysis()
            model = Helper.open_saved_file_from_disk(self.filename)

            # store accuracy and prediction in base class
            accuracy = "{0:.2f}".format(model.score(self.x_test, self.y_test))
            # data_analysis.simple_graph_plot(self.y_test, model.predict(self.x_test), 'test regression')

            # test is mmr < max data of our database
            # self.user_data = self.user_data[self.user_data['MMRAvgValue'] < Constants.MAX_MMR_IS]
            # if len(self.user_data) < 1:
            #     Constants.DATA_ENCODED_FAILED = True
            #     raise ValueError('MMR to high')

            prediction = abs(np.ceil(model.predict(self.user_data).astype(np.float)))

            if Constants.USER_DATA_CSV == Constants.TRUE:
                Constants.TEMP['Prediction'] = prediction
                Constants.TEMP.to_csv('temp_data/'+Constants.ALGORITHM_NAME+'prediction_result.csv', sep=',',
                                      encoding='utf-8')
                return accuracy + '%', prediction
            return accuracy + '%', prediction
        except Exception as err:
            LogHelper.get_logger().error(err)

    # fit for data train
    def fit_for_training(self, model):
        model.fit(self.x_train, self.y_train)
        print (model.best_params_)

        LogHelper.get_logger().info(Constants.ALGORITHM_NAME+' regression model trained')
        # save model in disk
        Helper.save_in_disk(self.filename, model)

