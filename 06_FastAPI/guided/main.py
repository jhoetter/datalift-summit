from webbrowser import get
from fastapi import FastAPI
from recommender import *
from util import *

app = FastAPI()

# Setup the "database" in memory
df = get_dataframe()
embeddings = read_embeddings()

# default route
@app.get("/")
async def root():
    return {"message": f"Hello World"}

# route that gets all the dataframe data necessary for frontend display
@app.get("/data")
async def get_data():
    # TODO get the data and return the it in json format
    return ...

# TODO specify the fastAPI recommendation route
...
async def get_recommendations():
    # TODO get the top 10 recommendations and return the "headline", "body" and "date" of them as a json
    return ...

# route that gets the top 10 similar records based on a given record
@app.get("/similar")
async def get_similar_stories(headline:str):
    # TODO return an error code if there is no entry with that headline
    if(...):
        return ...
    else:
        top_10_similar = get_top_10_similar_stories(df=df, headline=headline, embeddings=embeddings)
        return top_10_similar[["headline", "body", "date"]].to_json(None, orient="records")