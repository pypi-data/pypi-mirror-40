import lightgbm as lgb
import pandas as pd
import numpy as np
from hyperopt import fmin, tpe, hp, Trials
from sklearn.metrics import get_scorer
from lmtoolkit.scorer import neg_rmse, fast_auc, neg_logloss
from eli5.permutation_importance import get_score_importances
import shap

class Estimator(object):
    def __init__(self, cv=None, objective='regression', metric='rmse', verbose_eval=-1, num_boost_round=200, early_stopping_rounds=200, param={}):
        self.feature_importances = {}
        self.cv = cv
        self.estimators = {}
        self.metric = metric
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

    def fit(self, X, y):
        self.fitted_ = True
        if self.cv is None:
            model, val_score = self.__fit_single_model(X, y)
            self.models.append(model)
        else:
            for fold, (trn_idx, val_idx) in enumerate(self.cv.split(X.values, y.values)):        
                # X_train, X_val, y_train, y_val = X.reindex(trn_idx), X.reindex(val_idx), y.reindex(trn_idx), y.reindex(val_idx)
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

            val_score = evals_result['valid_1'][self.metric][0]
        else:
            model = lgb.train(self.param, trn_data, num_boost_round, valid_sets=valid_sets)
            val_score = np.nan

        return model, val_score

class FeatureSelector:
    def __init__(self, estimator, train, target, scorer, n_iter=3):
        self.estimator = estimator
        self.train = train
        self.target = target
        self.scorer = scorer
        self.n_iter = n_iter

    def get_important_features(self):
        importances = self.get_permutation_importances()
        whitelist = self.get_dependent_features()
        features = self.train.columns.tolist()
        selected = [i for i, imp in enumerate(importances) if imp > 0 and i not in whitelist]
        return [features[i] for i in selected]

    def get_permutation_importances(self):
        importances = []
        for fold, (trn_idx, val_idx) in enumerate(self.estimator.cv.split(self.train.values, self.target.values)):        
            X_train, X_val, y_train, y_val = self.train.iloc[trn_idx], self.train.iloc[val_idx],\
                    self.target.iloc[trn_idx], self.target.iloc[val_idx]

            # retrain
            self.estimator.refit(X_train, y_train)
            score = self.__build_permutation_importances_scorer(self.estimator)
            _, score_decreases = get_score_importances(score, X_val.values, y_val.values, n_iter=self.n_iter)
            feature_importances = np.mean(score_decreases, axis=0)
            importances.append(feature_importances)

        return np.mean(importances, 0)

    def get_dependent_features(self):
        if not self.estimator.fitted_:
            self.estimator.fit(self.train, self.target)

        explainer = shap.TreeExplainer(self.estimator.models[0])
        try:
            interaction_values = explainer.shap_interaction_values(
                    self.train).mean(0)
        except MemoryError:
            interaction_values = explainer.shap_interaction_values(
                    self.train.sample(frac=0.2)).mean(0)

        dependents = set(np.argwhere(interaction_values > 0))
        return dependents

    def __build_permutation_importances_scorer(self, estimator):
        def score(X, y):
            X = pd.DataFrame(X, columns=self.train.columns)
            for c in self.train.columns:
                X[c] = X[c].astype(self.train[c].dtype)
            pred = estimator.predict(X)
            return self.scorer(y, pred)
        return score

class Tuner:
    def __init__(self, estimator, train, target, max_evals=100):
        self.estimator = estimator
        self.train = train
        self.target = target
        self.max_evals = max_evals
        self.loss_metric = self.estimator.objective == 'regression' or ('loss' in self.estimator.metric)

    def tune(self, seed_param={}):
        def eval(param):
            self.estimator.update_param(param)
            self.estimator.refit(self.train, self.target)
            score = self.estimator.eval()[0]
            return -1 * score if self.loss_metric else score

        space, param_list_spaces = self.__generate_lgbm_hyperparameter_spaces(seed_param)

        # run optimization
        trials = Trials()
        best = fmin(fn=eval,
            space=space,
            algo=tpe.suggest,
            max_evals=self.max_evals,
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
