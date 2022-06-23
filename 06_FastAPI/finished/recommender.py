from embedders.classification.contextual import TransformerSentenceEmbedder
from scipy.spatial.distance import cdist
from util import get_dataframe

import pandas as pd
import numpy as np
import json

def get_embeddings(path = "../../04_ModelPipeline/finished/output.csv", model_indentifier = "distilbert-base-cased"):
    # load the data
    df = get_dataframe(path = path)
    
    # load the embedder
    embedder = TransformerSentenceEmbedder(model_indentifier)

    # embedd the texts
    embeddings = np.array(embedder.transform(df["merged_texts"].values.tolist()))

    # return the embeddings
    return embeddings

def get_top_10_recommendations(df, embeddings):
    # average the interesting vector
    interesting_idxs = df[df["__Interesting__MANUAL"] == "yes"].index
    interesting_vector_avg = embeddings[interesting_idxs].mean(axis=0)

    # calculate the distances to the unlabeled data
    non_labeled_idxs = df[df["__Interesting__MANUAL"].isnull()].index
    dist_to_unlabeled = cdist(interesting_vector_avg.reshape(1,-1), embeddings[non_labeled_idxs], metric="cosine")[0]

    # sort the indices ascending
    sorted_unlabeled_idxs = dist_to_unlabeled.argsort()

    # translate them back to the original dataframe
    sorted_original_idxs = non_labeled_idxs[sorted_unlabeled_idxs]

    # get the 10 items with lowest distance
    top_10_recommendations = df.loc[sorted_original_idxs[0:10]]

    return top_10_recommendations

def get_top_10_similar_stories(df, headline, embeddings):
    idx = df[df["headline"] == headline].index.item()

    # careful this also includes the idx of the original story
    dists = cdist(embeddings[idx].reshape(1,-1), embeddings, metric="cosine")[0]
    top_10_similar_idx = dists.argsort()[1:11]

    return df.loc[top_10_similar_idx]
