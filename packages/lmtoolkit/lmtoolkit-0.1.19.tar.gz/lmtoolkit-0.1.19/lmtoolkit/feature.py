import numpy as np
import pandas as pd
import lightgbm as lgb
import lmtoolkit.utils as utils
import lmtoolkit.importances as imp
import itertools

from eli5.permutation_importance import get_score_importances
from sklearn.model_selection import KFold, StratifiedKFold

class ValBaseFeatureSelector(object):
    def __init__(self, param, n_splits=5, stratified=False, random_state=0):
        self.param = param
        self.features = []
        self.n_splits = n_splits
        self.random_state = random_state
        self.fold_importances = []
        self.stratified = stratified
        self.feature_names = []

    def fit(self, train, target):
        if self.stratified:
            assert 'float' in target.dtype
            cv = StratifiedKFold(n_splits=self.n_splits,
                    shuffle=True, random_state=self.random_state)
        else:
            cv = KFold(n_splits=self.n_splits,
                    shuffle=True, random_state=self.random_state)

        for fold, (trn_idx, val_idx) in enumerate(cv.split(train)):
            feature_importances = self._get_feature_importances(
                    self.param, 
                    train.iloc[trn_idx],
                    target.iloc[trn_idx],
                    train.iloc[val_idx],
                    target.iloc[val_idx])

            self.fold_importances.append(feature_importances)
        self.feature_names = train.columns.tolist()
        return self

    def get_important_features(self):
        return []

    def _get_feature_importances(self, param, X_train, y_train, X_val=None, y_val=None):
        return np.zeros(len(self.feature_names))

    def _train_lgb(self, param, X_train, y_train, X_val, y_val):
        trn_data = lgb.Dataset(X_train, y_train)
        val_data = lgb.Dataset(X_val, y_val)
        valid_sets = [trn_data, val_data]
        param['verbosity'] = -1
        clf = lgb.train(param,
                        trn_data,
                        10000,
                        valid_sets=valid_sets,
                        early_stopping_rounds=200,
                        verbose_eval=-1)
        return clf

class TrainBaseFeatureSelector(object):
    def __init__(self, param):
        self.param = param
        self.importances = []
        self.feature_names = []

    def fit(self, train, target):
        self.importances = self._get_feature_importances(
                self.param, train, target)
        self.feature_names = train.columns.tolist()
        return self

    def get_important_features(self):
        return []

    def _get_feature_importances(self, param, X_train, y_train):
        return np.zeros(len(self.feature_names))

class SplitSelector(ValBaseFeatureSelector):
    def __init__(self, param, min_split=1, **kwargs):
        self.min_split = min_split
        super().__init__(param, **kwargs)

    def _get_feature_importances(self, param, X_train, y_train, X_val, y_val):
        estimator = self._train_lgb(param, X_train, y_train, X_val, y_val)
        return estimator.feature_importance()

    def get_important_features(self):
        importances = np.mean(self.fold_importances, 0)
        return [f for f, imp in zip(self.feature_names, importances) if imp >= self.min_split]

class PermutationSelector(ValBaseFeatureSelector):
    def get_important_features(self):
        importances = np.mean(self.fold_importances, 0)
        return [f for f, imp in zip(self.feature_names, importances) if imp > 0]

    def _get_feature_importances(self, param, X_train, y_train, X_val, y_val):
        estimator = self._train_lgb(param, X_train, y_train, X_val, y_val)
        if 'metric' not in param.keys():
            metric = 'binary_logloss' if param['objective'] == 'binary' else 'rmse'
        else:
            metric = param['metric']

        scorer = self.__build_permutation_importances_scorer(estimator,
                                                             X_train,
                                                             metric)
        _, score_decreases = get_score_importances(scorer,
                                                   X_val.values,
                                                   y_val.values)

        return np.mean(score_decreases, axis=0)

    def __build_permutation_importances_scorer(self, estimator, train, metric):
        def score(X, y):
            return utils.get_scorer(metric)(y, estimator.predict(X))
        return score

class NullSelector(TrainBaseFeatureSelector):
    def get_important_features(self, importance_type='split', threshold=25):
        idx = 0 if importance_type == 'split' else 1
        importances = [x[idx] for x in self.importances]
        return [self.feature_names[i] for i, imp in enumerate(importances) if imp >= threshold]

    def _get_feature_importances(self, param, X_train, y_train):
        corr_df = imp.get_null_importances(param, X_train, y_train)
        return list(zip(corr_df['split_score'], corr_df['gain_score']))
