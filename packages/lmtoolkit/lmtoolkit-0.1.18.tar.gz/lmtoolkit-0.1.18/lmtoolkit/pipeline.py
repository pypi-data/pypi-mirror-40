import pandas as pd
import numpy as np
import category_encoders as ce

from sklearn.model_selection import *
from sklearn.preprocessing import *
from sklearn.impute import *
from sklearn.pipeline import *
from sklearn.compose import *

def get_custom(df, target, estimators, ignores=[], features=None, categories=[]):
    estimators = _get_standard_pipeline_estimators()
    for k, v in estimators.items():
        estimators[k] = v
    pipeline, cols = _base_pipeline(df, target, estimators, features, ignores, categories)
    return pipeline, cols

def get_standard(df, target, ignores=[], features=None, categories=[]):
    estimators = _get_standard_pipeline_estimators()
    pipeline, cols = _base_pipeline(df, target, estimators, features, ignores, categories)
    return pipeline, cols

def pipeline_split(df, target, pipeline, shuffle=True, use_test=True, compress=False, **kwargs):
    if use_test:
        X_train, X_test, y_train, y_test = train_test_split(df.drop(target, 1), df[target],\
                shuffle=shuffle, **kwargs)
        X_train = pipeline.fit_transform(X_train, y_train)
        X_test = pipeline.transform(X_test)
    else:
        if shuffle:
            df = df.sample(frac=1, replace=False)
        X_train, y_train = df.drop(target, 1), df[target]
        X_train = pipeline.fit_transform(X_train, y_train)
        X_test, y_test = None, None

    if compress:
        X_train = X_train.astype(np.int32)
        y_train = y_train.astype(np.int32)
        if use_test:
            X_test = X_test.astype(np.int32)
            y_test = y_test.astype(np.int32)

    y_train = y_train.values
    if use_test: y_test = y_test.values
    return X_train, X_test, y_train, y_test

# helpers, don't use directly
def _get_standard_pipeline_estimators():
    estimators = dict(
        num_imputer = SimpleImputer(strategy='median'),
        cat_imputer = SimpleImputer(strategy='median'),
        scaler = StandardScaler(),
        encoder = ce.TargetEncoder()
    )
    return estimators


def _base_pipeline(df, target, estimators, features, ignores, categories):
    if features is not None:
        df = df[features + [target]]
    num_cols = list(df.select_dtypes('number').columns)
    cat_cols = list(df.select_dtypes('object').columns) + list(df.select_dtypes('category').columns) + list(df.select_dtypes('bool').columns)

    # ignore columns, disabled if features is not None
    if features == None:
        for c in ignores + [target]:
            if c in num_cols:
                num_cols.remove(c)
            elif c in cat_cols:
                cat_cols.remove(c)
            else:
                pass
    cols = num_cols + cat_cols

    # get estimators
    num_imputer = estimators['num_imputer']
    cat_imputer = estimators['cat_imputer']
    scaler = estimators['scaler']
    encoder = estimators['encoder']

    # build pipeline
    num_pipeline = make_pipeline(num_imputer, scaler)
    num_transformer = ('DEFAULT_NUM_TRANSFORMER', num_pipeline, num_cols)

    if encoder is None:
        cat_pipeline = make_pipeline(cat_imputer, OrdinalEncoder())
    else:
        cat_pipeline = make_pipeline(cat_imputer, OrdinalEncoder(), encoder)
    cat_transformer = ('DEFAULT_CAT_TRANSFORMER', cat_pipeline, cat_cols)
    pipeline = ColumnTransformer([num_transformer, cat_transformer])
    return pipeline, cols
