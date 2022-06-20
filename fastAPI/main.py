from webbrowser import get
from fastapi import FastAPI
from util import *

app = FastAPI()

# Setup the "database" in memory
df = get_dataframe()
vectorizer = fit_and_return_vectorizer(df)
vectorized_matrix = get_vectorized_matrix(df, vectorizer)
cosine_similarity_matrix = get_cosine_similarity_matrix(vectorized_matrix)

state = {"recommendations": []}


@app.get("/")
async def root():
    return {"message": f"Hello World"}


@app.get("/recommend")
async def get_recommendations():
    avg_interesting_vector = get_average_interesting_vector(df, vectorizer)
    top_10_recommendations = get_top10_recommended_from_vector(
        df, avg_interesting_vector, vectorized_matrix)
    return top_10_recommendations
