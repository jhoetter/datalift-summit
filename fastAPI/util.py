import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def get_dataframe(path = "../labeled_and_processed_stories.csv"):
    return pd.read_csv(path)

def get_vectorized_matrix(df, target_attribute="full_text"):
    vectorizer = CountVectorizer().fit(df[target_attribute])
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

def get_top10_recommended_from_vector(df, vec1, vectorized_matrix, headline_attribute = "headline"):
    recommended_articles = []
    similarity_matrix = cosine_similarity(vec1, vectorized_matrix)
    scores = pd.Series(similarity_matrix[0]).sort_values(ascending = False)
    top_10_indices = list(scores.iloc[1:11].index)
    for i in top_10_indices:
        recommended_articles.append(list(df[headline_attribute])[i])
    return recommended_articles

def get_average_vector(df, interesting = True, label_attribute = "interesting"):
    if(interesting):
        temp_df = df[df[label_attribute] == "yes"]
    else:
        temp_df = df[df[label_attribute] == "no"] # was hab ich mir hier gedacht

    temp_vetorized = get_vectorized_matrix(temp_df)

    