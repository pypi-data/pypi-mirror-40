from scipy.stats import randint as sp_randint
from sklearn.model_selection import RandomizedSearchCV


class RegrassionFineTune:
    # parameters for GridSearchCV
    # specify parameters and distributions to sample from

    def __init__(self):
        pass

    param_dist = {"n_estimators": sp_randint(10, 1000).rvs(100),
                  "max_depth": sp_randint(1, 40).rvs(15),
                  "min_samples_split": sp_randint(2, 11).rvs(5),
                  "min_samples_leaf": sp_randint(1, 11).rvs(5),
                  }

    def randome_forest(self, model):
        param = {"bootstrap": [True, False]}
        param.update(self.param_dist)
        return self.run_fine_tune(model, param)

    def x_g_boost(self, model):
        float_value = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        param = {'loss': ['ls', 'lad', 'huber', 'quantile'],
                 'learning_rate': [0.1, 0.2, 0.3, 0.4],
                 'subsample': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
                 'min_weight_fraction_leaf': [0, 0.1, 0.2, 0.3, 0.4, 0.5],
                 'min_impurity_decrease': float_value,
                 'max_features': ['sqrt', 'log2', 'auto'],
                 }
        param.update(self.param_dist)
        return self.run_fine_tune(model, param)

    def gradient_boosting(self, model):
        param = {
                 'warm_start': [False, True],
                 }
        param.update(self.param_dist)
        return self.x_g_boost(model)

    def bagging_tuning(self, model):
        float_value = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        param = {
            'n_estimators': sp_randint(5, 100).rvs(20),
            'max_samples': float_value,
            'max_features': float_value,
            'oob_score': float_value,
            'verbose': [0, 1, 2, 3, 4]
        }
        return self.run_fine_tune(model, param, n_iter_search=20)

    def run_fine_tune(self, model, param, n_iter_search=100, k_fold=5):
        # run randomized search
        random_search = RandomizedSearchCV(model, param_distributions=param, n_iter=n_iter_search, cv=k_fold)
        return random_search
