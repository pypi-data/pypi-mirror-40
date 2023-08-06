import lightgbm as lgb
import pandas as pd
import numpy as np
from hyperopt import fmin, tpe, hp, Trials
from sklearn.metrics import get_scorer
from lmtoolkit.scorer import neg_rmse, fast_auc, neg_logloss

class Estimator(object):
    def __init__(self, cv=None, objective='regression', metric=None, verbose_eval=-1, num_boost_round=200, early_stopping_rounds=200, param={}, random_state=0):
        self.feature_importances = {}
        self.cv = cv
        self.objective = objective
        self.verbose_eval = verbose_eval
        self.num_boost_round = num_boost_round
        self.early_stopping_rounds = early_stopping_rounds
        self.models = []
        self.evals_results = []
        self.fitted_ = False

        self.param = param
        self.param['objective'] = objective
        self.param['metric'] = metric
        self.param['verbosity'] = verbose_eval
        self.param['random_state'] = random_state

        self.metric = metric
        if metric is None:
            self.metric = 'rmse' if objective == 'regression' else 'binary_logloss'

    def fit(self, X, y):
        self.fitted_ = True
        if self.cv is None:
            model, val_score = self.__fit_single_model(X, y)
            self.models.append(model)
        else:
            for fold, (trn_idx, val_idx) in enumerate(self.cv.split(X.values, y.values)):        
                X_train, X_val, y_train, y_val = X.iloc[trn_idx], X.iloc[val_idx], y.iloc[trn_idx], y.iloc[val_idx]
                model, val_score = self.__fit_single_model(X_train, y_train, X_val, y_val)
                self.models.append(model)
                self.evals_results.append(val_score)
        return self

    def predict(self, X):
        predictions = np.zeros(len(X))
        for model in self.models:
            predictions += model.predict(X) / len(self.models)
        return predictions

    def oof_fit_predict(self, X, y):
        oof = np.zeros(len(X))
        for fold, (trn_idx, val_idx) in enumerate(self.cv.split(X.values, y.values)):        
            X_train, X_val, y_train = X.iloc[trn_idx], X.iloc[val_idx], y.iloc[trn_idx]
            model, val_score = self.__fit_single_model(X_train, y_train)
            oof[val_idx] = model.predict(X_val)
        return oof

    def refit(self, X, y):
        self.__reset()
        self.fit(X, y)
        return self

    def eval(self):
        return np.mean(self.evals_results), np.std(self.evals_results)

    def update_param(self, param):
        for key, value in param.items():
            self.param[key] = value

    def __reset(self):
        self.models = []
        return self

    def __fit_single_model(self, X, y, X_val=None, y_val=None):
        trn_data = lgb.Dataset(X, label=y)
        valid_sets = [trn_data]
        num_boost_round = self.num_boost_round

        if X_val is not None:
            val_data = lgb.Dataset(X_val, label=y_val)
            valid_sets = [trn_data, val_data]
            num_boost_round = 10000
            evals_result = {}
        
            model = lgb.train(
                    self.param,
                    trn_data,
                    num_boost_round,
                    valid_sets=valid_sets,
                    verbose_eval=self.verbose_eval,
                    early_stopping_rounds=self.early_stopping_rounds,
                    evals_result=evals_result
                    )
            best_index = model.best_iteration
            val_score = evals_result['valid_1'][self.metric][best_index-1]
        else:
            model = lgb.train(self.param, trn_data, num_boost_round, valid_sets=valid_sets)
            val_score = np.nan

        return model, val_score


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
