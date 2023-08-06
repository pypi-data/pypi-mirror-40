import numpy as np
import pandas as pd
import lightgbm as lgb
import lmtoolkit.utils as utils

from eli5.permutation_importance import get_score_importances
from sklearn.model_selection import KFold, StratifiedKFold

def get_feature_importances(param, train, target, shuffle=False, seed=0, trial=50):
    y = target
    if shuffle:
        y = target.sample(frac=1.0)
    
    dtrain = lgb.Dataset(train, y, free_raw_data=False, silent=True)
    param['verbosity'] = -1
    
    evals_result = {}
    clf = lgb.train(params=param,
                    train_set=dtrain,
                    valid_sets=[dtrain],
                    num_boost_round=200,
                    evals_result=evals_result,
                    verbose_eval=-1)

    imp_df = pd.DataFrame()
    imp_df["feature"] = list(train.columns)
    imp_df["importance_gain"] = clf.feature_importance(importance_type='gain')
    imp_df["importance_split"] = clf.feature_importance(importance_type='split')
    imp_df['trn_score'] = evals_result['training'][param['metric']][-1]
    
    return imp_df

def get_null_importances(param, train, target, seed=0, trial=50):
    correlation_scores = []
    actual_imp_df = get_feature_importances(param, train, target)
    null_imp_df = pd.DataFrame()

    for i in range(trial):
        imp_df = get_feature_importances(param, train, target, True)
        imp_df['run'] = i + 1 
        null_imp_df = pd.concat([null_imp_df, imp_df], axis=0)

    for _f in actual_imp_df['feature'].unique():
        f_null_imps = null_imp_df.loc[null_imp_df['feature'] == _f, 'importance_gain'].values
        f_act_imps = actual_imp_df.loc[actual_imp_df['feature'] == _f, 'importance_gain'].values[0]
        gain_score = 100 * (f_null_imps < f_act_imps).sum() / f_null_imps.size

        f_null_imps = null_imp_df.loc[null_imp_df['feature'] == _f, 'importance_split'].values
        f_act_imps = actual_imp_df.loc[actual_imp_df['feature'] == _f, 'importance_split'].values[0]
        split_score = 100 * (f_null_imps < f_act_imps).sum() / f_null_imps.size

        correlation_scores.append((_f, split_score, gain_score))
    corr_scores_df = pd.DataFrame(correlation_scores, columns=['feature', 'split_score', 'gain_score'])
    return corr_scores_df
