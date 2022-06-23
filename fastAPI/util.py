import pandas as pd
import numpy as np
import json

def get_dataframe(path = "G:\\GitHub\\onetask\\datalift-summit\\04_ModelPipeline\\labeled_data_v1.json"):
    # load the data
    with open(path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["merged_texts"] = df["headline"] + ". "+ df["body"]
    return df

def read_embeddings(path = "G:\\GitHub\onetask\\datalift-summit\\04_ModelPipeline\\embeddings.npy"):
    embeddings = np.load(path)
    return embeddings
