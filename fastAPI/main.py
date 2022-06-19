from webbrowser import get
from fastapi import FastAPI
from util import *

app = FastAPI()

# Setup the "database" in memory
df = get_dataframe()
vectorizer = fit_and_return_vectorizer(df)
vectorized_matrix = get_vectorized_matrix(df, vectorizer)
cosine_similarity_matrix = get_cosine_similarity_matrix(vectorized_matrix)

@app.get("/")
async def root():
    return {"message": f"Hello World"}


@app.get("/recommend")
async def get_recommendations(idx: int = 0):
    if(idx > 9):
        idx = 9
    elif(idx <=0):
        idx = 0
    avg_interesting_vector = get_average_interesting_vector(df, vectorizer)
    print(avg_interesting_vector.shape)
    print(vectorized_matrix.shape)
    top_10_recommendations = get_top10_recommended_from_vector(df,avg_interesting_vector , vectorized_matrix)
    return {"message": f"recommend {top_10_recommendations[idx]}"}
