import pandas as pd
import numpy as np
import lmtoolkit.scorer as scorer
from itertools import chain, combinations

from sklearn.metrics import mean_squared_error, log_loss

scorers = dict(
    rmse=scorer.rmse,
    binary_logloss=log_loss,
    auc=scorer.fast_auc,
)

def get_scorer(metric):
    return scorers[metric]

def bigger_better_metric(metric):
    return metric in ['auc', 'accuracy', 'f1']
