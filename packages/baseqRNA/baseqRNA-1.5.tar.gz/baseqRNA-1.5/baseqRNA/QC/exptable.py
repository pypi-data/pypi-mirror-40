import pandas as pd
import numpy as np

def read_table(path):
    """
    Read the gene expression table, need to be a tsv.
    """
    try:
        df = pd.read_table(path, index_col=0)
    except:
        df = pd.read_csv(path, index_col=0)
    return df

def filter_low_exp(df, min_avg = 1):
    """
    Filter low expression with mean average value larger than 1;
    """
    return df.loc[df.mean(axis=1)>=min_avg, :]

def log2_transform(df):
    def process(x):
        return np.log2(x+1)
    return df.applymap(process)