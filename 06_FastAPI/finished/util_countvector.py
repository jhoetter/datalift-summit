import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def get_dataframe(path = "../labeled_and_processed_stories.csv"):
    return pd.read_csv(path)

def fit_and_return_vectorizer(df, target_attribute="full_text"):
    return CountVectorizer().fit(df[target_attribute])

def get_vectorized_matrix(df, vectorizer, target_attribute="full_text"):
    vectorized_matrix = vectorizer.transform(df[target_attribute])
    return vectorized_matrix

def get_cosine_similarity_matrix(vectorized_matrix):
    return cosine_similarity(vectorized_matrix, vectorized_matrix)

def get_top10_recommended_from_headline(df, headline, cosine_similarity_matrix, headline_attribute = "headline"):
    recommended_articles = []
    idx = df[df[headline_attribute] == headline].index[0]
    score_series = pd.Series(cosine_similarity_matrix[idx]).sort_values(ascending = False)
    top_10_indices = list(score_series.iloc[1:11].index)
    
    for i in top_10_indices:
        recommended_articles.append(list(df[headline_attribute])[i])
        
    return recommended_articles

def get_top10_recommended_from_vector(df, vec1, vectorized_matrix):
    recommended_articles = []
    similarity_matrix = cosine_similarity(vec1, vectorized_matrix)
    scores = pd.Series(similarity_matrix[0]).sort_values(ascending = False)
    top_10_indices = list(scores.iloc[1:11].index)
    for i in top_10_indices:
        # TODO return an object with all attributes plus similarity score
        recommended_articles.append({
            "headline": list(df["headline"])[i],
            "body" : list(df["body"])[i],
            "date" : list(df["date"])[i],
            "matching_score" : scores[i]
        })
    return recommended_articles

def get_average_interesting_vector(df, vectorizer, label_attribute = "interesting"):
    temp_df = df[df[label_attribute] == "yes"]
    temp_vectorized = get_vectorized_matrix(temp_df, vectorizer)
    return temp_vectorized.mean(axis=0)


    