from webbrowser import get
from fastapi import FastAPI
from recommender import *
from util import *

app = FastAPI()

# Setup the "database" in memory
df = get_dataframe()
embeddings = read_embeddings()

state = {"recommendations": []}


@app.get("/")
async def root():
    return {"message": f"Hello World"}


@app.get("/recommend")
async def get_recommendations():
    top_10 = get_top_10_recommendations(df, embeddings)
    return top_10[["headline", "body", "date"]].to_json(None, orient="records")

@app.get("/similar")
async def get_similar_stories(headline:str):
    if(df[df["headline"] == headline].empty):
        return 400
    else:
        top_10_similar = get_top_10_similar_stories(df=df, headline=headline, embeddings=embeddings)
        return top_10_similar[["headline", "body", "date"]].to_json(None, orient="records")
