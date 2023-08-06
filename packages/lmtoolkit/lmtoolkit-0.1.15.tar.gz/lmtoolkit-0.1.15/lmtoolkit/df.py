import pandas as pd
import numpy as np
import dask.dataframe as dd
import os

def read(path, use_dask=False, verbose=False, **kwargs):
    fname = os.path.split(path)[-1]
    if use_dask:
        # TODO: switch to dask
        df = pd.read_csv(path, **kwargs)
    else:
        df = pd.read_csv(path, **kwargs)
        size = df.memory_usage().sum()

        df = reduce_mem_usage(df)
    if verbose:
        new_size = df.memory_usage().sum()
        reduction = (size-new_size) / size * 100
        print('%s memory reduced by %.2f%%' % (fname, reduction))
    return df

def reduce_mem_usage(df):
    start_mem = df.memory_usage().sum() / 1024**2
    
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type != object:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else: 
            df[col] = df[col].astype('category')

    return df
