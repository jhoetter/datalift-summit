import pandas as pd
import numpy as np
import json

def get_dataframe(path = "../../04_ModelPipeline/finished/output.csv"):
    # load the data
    return pd.read_csv(path, quoting=1)

def read_embeddings(path = "../../04_ModelPipeline/finished/embeddings.npy"):
    embeddings = np.load(path)
    return embeddings
