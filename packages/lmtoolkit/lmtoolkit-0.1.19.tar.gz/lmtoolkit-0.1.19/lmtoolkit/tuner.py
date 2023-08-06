import lightgbm as lgb
import pandas as pd
import numpy as np
import time
import lmtoolkit.utils as utils

from hyperopt import fmin, tpe, hp, Trials
from hyperopt.pyll.base import scope
from sklearn.metrics import get_scorer

class HyperparameterTuner:
    def __init__(self, param):
        self.param = param

    def __init_space_param(self):
        uniform_param = [
            ('learning_rate', 0.01, 1),
            ('feature_fraction', 0.75, 1),
            ('bagging_fraction', 0.75, 1),
            ('reg_alpha', 0, 1),
            ('reg_lambda', 0, 1),
        ]

        quniform_param = [
            ('max_bin', 50, 300, 10),
            ('num_leaves', 50, 150, 5),
            ('min_data_in_leaf', 5, 50, 5),
            ('max_depth', 5, 50, 5),
            ]

        param_spaces = {}
        for p in uniform_param:
            name, low, high = p[0], p[1], p[2]
            param_spaces[name] = hp.uniform(name, low, high)

        for p in quniform_param:
            name, low, high, q = p[0], p[1], p[2], p[3]
            param_spaces[name] = scope.int(hp.quniform(name, low, high, q))

        space = dict(
            num_boost_round=scope.int(hp.qloguniform('num_boost_round', 2, 10, 10)),
            param=param_spaces)
        return space

    def __generate_eval_function(self, param, train, target):
        trn_data = lgb.Dataset(train, target)
        seed_param = param
        metric = param['metric']
        def eval(param):
            for k, v in seed_param.items():
                param['param'][k] = v
            results = lgb.cv(param['param'], trn_data, param['num_boost_round'], stratified=False)
            loss = results['{}-mean'.format(metric)][-1]
            return loss if not utils.bigger_better_metric(metric) else -loss
        return eval

    def tune(self, train, target, max_runtime_secs=3600, trial_per_op=1):
        start = time.time()
        trials = Trials()
        exceed_timeout = False

        i = 1
        while not exceed_timeout:
            best = fmin(fn=self.__generate_eval_function(self.param, train, target),
                space=self.__init_space_param(),
                algo=tpe.suggest,
                max_evals=(1+i) * trial_per_op,
                trials=trials)
            i += 1
            exceed_timeout = (time.time() - start) > max_runtime_secs
        return best, trials
