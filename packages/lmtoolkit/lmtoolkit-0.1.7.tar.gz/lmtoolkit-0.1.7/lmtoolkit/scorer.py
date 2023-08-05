from sklearn.metrics import mean_squared_error
import numpy as np

def neg_rmse(y_true, y_pred):
    return -mean_squared_error(y_true, y_pred) ** 0.5

def fast_auc(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_true = y_true[np.argsort(y_pred)]
    nfalse = 0
    auc = 0
    n = len(y_true)
    for i in range(n):
        y_i = y_true[i]
        nfalse += (1 - y_i)
        auc += y_i * nfalse
    auc /= (nfalse * (n - nfalse))
    return auc
