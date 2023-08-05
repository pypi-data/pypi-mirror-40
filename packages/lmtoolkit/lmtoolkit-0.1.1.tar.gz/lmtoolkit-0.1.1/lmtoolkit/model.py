import lightgbm as lgb
import pandas as pd
import numpy as np

def lgbm_predict(train, test, target, features, categorical_feats, param, cv, subset=[], num_round=10000, early_stopping_rounds=200, verbose_eval=-1):
    use_subset = len(subset) > 0
    full_oof = np.zeros(len(train))
    predictions = np.zeros(len(test))
    
    feature_importance_df = pd.DataFrame()

    for fold, (trn_idx, val_idx) in enumerate(cv.split(train.values, target.values)):        
        if use_subset:
            trn_idx = trn_idx[np.isin(trn_idx, subset)]
            subval_idx = val_idx[np.isin(val_idx, subset)]
            
            val_data = lgb.Dataset(train.iloc[subval_idx][features],
                               label=target.iloc[subval_idx],
                               categorical_feature=categorical_feats
                              )
            
        trn_data = lgb.Dataset(train.iloc[trn_idx][features],
                               label=target.iloc[trn_idx],
                               categorical_feature=categorical_feats
                              )
        
        model = lgb.train(param,
                        trn_data,
                        num_round,
                        valid_sets = [trn_data, val_data],
                        verbose_eval=verbose_eval,
                        early_stopping_rounds = early_stopping_rounds)
        
        full_oof[val_idx] = model.predict(train.iloc[val_idx][features], num_iteration=model.best_iteration)

        fold_importance_df = pd.DataFrame()
        fold_importance_df["feature"] = features
        fold_importance_df["importance"] = model.feature_importance()
        fold_importance_df["fold"] = fold + 1
        feature_importance_df = pd.concat([feature_importance_df, fold_importance_df], axis=0)

        predictions += model.predict(test[features], num_iteration=model.best_iteration) / cv.n_splits
    return predictions, full_oof, full_oof[subset], feature_importance_df
