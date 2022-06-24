from webbrowser import get
from fastapi import FastAPI
from recommender import *
from util import *

app = FastAPI()

# default route
@app.get("/")
async def root():
    return {"message": f"Hello World"}

