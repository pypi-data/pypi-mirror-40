import pandas as pd
import numpy as np

def conditional_oof_predict(df, target, model, pipeline, query=None, n_fold=5, **kwargs):
    preds = []
    features = list(df.columns.drop(target).values)

    row = df.shape[0]
    fold_ranges = _create_fold_ranges(df, n_fold)
    full_ranges = set(range(row))
    for val_idx, val_range in enumerate(fold_ranges):
        train_idx = list(full_ranges - set(list(val_range)))
        train_df = df.iloc[train_idx]

        if query is not None:
            train_df.query(query)

        X_train, y_train = train_df[features], train_df[target]
        X_train = pipeline.fit_transform(X_train, y_train)

        test_df = df.iloc[val_range]
        X_test, y_test = test_df[features], test_df[target]
        X_test = pipeline.transform(X_test)

        model.fit(X_train, y_train, **kwargs)
        preds += list(model.predict(X_test).reshape(-1))

        # reset for the next fold
        model.__init__()
    return np.array(preds)


def oof_predict(model, X, y, n_fold=5, **kwargs):
    preds = []

    row = X.shape[0]
    fold_ranges = _create_fold_ranges(X, n_fold)
    full_ranges = set(range(row))
    for val_idx, val_range in enumerate(fold_ranges):
        X_test, y_test = X[val_range], y[val_range]
        train_idx = list(full_ranges - set(list(val_range)))
        X_train, y_train = X[train_idx], y[train_idx]

        # reset before training
        model.fit(X_train, y_train, **kwargs)
        preds += list(model.predict(X_test).reshape(-1))
        model.__init__()
    return np.array(preds)

def _create_fold_ranges(X, n_fold):
    row = X.shape[0]
    split_points = list(range(0, row, row // n_fold))
    if len(split_points) < n_fold+1:
        split_points.append(row)
    else:
        split_points[-1] = row

    fold_ranges = [range(split_points[i-1], split_points[i])\
                   for i in range(1, n_fold+1)]
    return fold_ranges
