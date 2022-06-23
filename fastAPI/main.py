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
    return df.to_json(None, orient="records")

# route that gets the top 10 recommendations based on the labeled data
@app.get("/recommend")
async def get_recommendations():
    top_10 = get_top_10_recommendations(df, embeddings)
    return top_10[["headline", "body", "date"]].to_json(None, orient="records")

# route that gets the top 10 similar records based on a given record
@app.get("/similar")
async def get_similar_stories(headline:str):
    if(df[df["headline"] == headline].empty):
        return 400
    else:
        top_10_similar = get_top_10_similar_stories(df=df, headline=headline, embeddings=embeddings)
        return top_10_similar[["headline", "body", "date"]].to_json(None, orient="records")