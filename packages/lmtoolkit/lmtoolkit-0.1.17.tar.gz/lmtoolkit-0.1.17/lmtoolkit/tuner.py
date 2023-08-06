import lightgbm as lgb
import pandas as pd
import numpy as np

from hyperopt import fmin, tpe, hp, Trials
from sklearn.metrics import get_scorer
from lmtoolkit.scorer import neg_rmse, fast_auc, neg_logloss

class Tuner:
    def __init__(self, estimator):
        self.estimator = estimator
        self.loss_metric = self.estimator.objective == 'regression' or ('loss' in self.estimator.metric)

    def tune(self, train, target, seed_param={}, max_evals=100):
        def eval(param):
            self.estimator.update_param(param)
            self.estimator.refit(train, target)
            score = self.estimator.eval()[0]
            return -1 * score if self.loss_metric else score

        space, param_list_spaces = self.__generate_lgbm_hyperparameter_spaces(seed_param)

        # run optimization
        trials = Trials()
        best = fmin(fn=eval,
            space=space,
            algo=tpe.suggest,
            max_evals=max_evals,
            trials=trials)
        best_params = self.__get_param_values(best, param_list_spaces)
        return best_params, trials

    def __get_param_values(self, best, param_list_spaces):
        best_params = best
        for k, v in best_params.items():
            if k in param_list_spaces.keys():
                best_params[k] = param_list_spaces[k][v]
        return best_params

    def __generate_lgbm_hyperparameter_spaces(self, seed_param, random_state=42):
        # defines parameter spaces
        def lr(low, high):
            return list(range(low, high))

        param_list_spaces = dict(
            max_bin=lr(50, 300),
            num_leaves=lr(50, 150),
            min_data_in_leaf=lr(50, 150),
            min_child_samples=lr(10, 50),
            max_depth=lr(1, 50),
            bagging_freq=[1],
            random_state=[random_state],
            objective=[self.estimator.objective],
            metric=[self.estimator.metric],
        )

        space = {
            'learning_rate': hp.uniform('learning_rate', 0.01, 1),
            'feature_fraction': hp.uniform('feature_fraction', 0, 1),
            'bagging_fraction': hp.uniform('bagging_fraction', 0, 1),
            'reg_alpha': hp.uniform('reg_alpha', 0, 1),
            'reg_lambda': hp.uniform('reg_lambda', 0, 1)
        }

        for k, v in seed_param.items():
            param_list_spaces[k] = v

        for k, v in param_list_spaces.items():
            space[k] = hp.choice(k, v)


        return space, param_list_spaces
