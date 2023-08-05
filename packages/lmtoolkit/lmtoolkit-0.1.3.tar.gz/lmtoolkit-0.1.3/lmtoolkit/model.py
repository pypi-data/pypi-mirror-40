import lightgbm as lgb
import pandas as pd
import numpy as np
from hyperopt import fmin, tpe, hp, Trials
from scorer import neg_rmse, fast_auc

def lgbm_fit_predict(train,
                     target,
                     features,
                     param,
                     cv,
                     test=None,
                     categorical_feats='auto',
                     subset=[],
                     num_round=10000,
                     early_stopping_rounds=200,
                     verbose_eval=-1):

    use_subset = len(subset) > 0
    use_test = test is not None

    oof = np.zeros(len(train))
    predictions = np.zeros(len(test)) if use_test else None
    
    feature_importance_df = pd.DataFrame()

    for fold, (trn_idx, val_idx) in enumerate(cv.split(train.values, target.values)):        
        if use_subset:
            trn_idx = trn_idx[np.isin(trn_idx, subset)]
            used_val_idx = val_idx[np.isin(val_idx, subset)]
        else:
            used_val_idx = val_idx

        val_data = lgb.Dataset(train.iloc[used_val_idx][features],
                           label=target.iloc[used_val_idx],
                           categorical_feature=categorical_feats)

            
        trn_data = lgb.Dataset(train.iloc[trn_idx][features],
                               label=target.iloc[trn_idx],
                               categorical_feature=categorical_feats)
        
        model = lgb.train(param,
                        trn_data,
                        num_round,
                        valid_sets = [trn_data, val_data],
                        verbose_eval=verbose_eval,
                        early_stopping_rounds = early_stopping_rounds)
        
        oof[val_idx] = model.predict(train.iloc[val_idx][features],
                                     num_iteration=model.best_iteration)
        if use_test:
            predictions += model.predict(test[features],
                                         num_iteration=model.best_iteration) / cv.n_splits

        fold_importance_df = pd.DataFrame()
        fold_importance_df["feature"] = features
        fold_importance_df["importance"] = model.feature_importance()
        fold_importance_df["fold"] = fold + 1
        feature_importance_df = pd.concat([feature_importance_df,
                                           fold_importance_df], axis=0)

    return predictions, oof, oof[subset], feature_importance_df

def lgbm_tune(train,
              target,
              features,
              cv,
              objective='regression',
              metric='rmse',
              categorical_feats=[],
              max_evals=100,
              num_round=10000,
              early_stopping_rounds=200,
              verbose_eval=-1,
              random_state=42):

    # define evaluation function and metrics
    scorer_getter = dict(rmse=neg_rmse, auc=fast_auc)
    scorer = scorer_getter[metric]

    def eval(param):
        _, oof, _, _ = lgbm_fit_predict(train,
                                        target,
                                        features,
                                        categorical_feats,
                                        param,
                                        cv,
                                        num_round=num_round,
                                        early_stopping_rounds=early_stopping_rounds,
                                        verbose_eval=verbose_eval)
        return -scorer(target, oof)

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
        objective=[objective],
        metric=[metric],
    )

    space = {
        'learning_rate': hp.uniform('learning_rate', 0.01, 1),
        'feature_fraction': hp.uniform('feature_fraction', 0, 1),
        'bagging_fraction': hp.uniform('bagging_fraction', 0, 1),
        'reg_alpha': hp.uniform('reg_alpha', 0, 1),
        'reg_lambda': hp.uniform('reg_lambda', 0, 1)
    }

    for k, v in param_list_spaces.items():
        space[k] = hp.choice(k, v)

    # run optimization
    trials = Trials()
    best = fmin(fn=eval,
        space=space,
        algo=tpe.suggest,
        max_evals=max_evals,
        trials=trials)

    # convert indices to real value
    best_params = best
    for k, v in best_params:
        if k in param_list_spaces.keys():
            best_params[k] = param_list_spaces[k][v]
    return best_params, trials
