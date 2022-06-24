from embedders.classification.contextual import TransformerSentenceEmbedder
from scipy.spatial.distance import cdist
import numpy as np
import pandas as pd

INTERESTING_LABEL_ATTRIBUTE = "__Interesting__MANUAL"

def get_top_10_recommendations(df, embeddings) -> pd.DataFrame:
    
    # TODO use the code from the notebook from 04_ModelPipeline to get the top10 recommendations here

    top_10_recommendations = ...

    return top_10_recommendations

def get_top_10_similar_stories(df, headline, embeddings) -> pd.DataFrame:
    idx = df[df["headline"] == headline].index.item()

    # TODO calc the dists to the one entry and return the top 10 similar ones. Note: be careful not to include the original story which will have the highest similarity score
    dists = ...
    top_10_similar_idx = dists.argsort()[...]

    return df.loc[top_10_similar_idx]
