# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import pandas as pd
from fastapi import FastAPI, Query,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from auto_com import AutoComplete
import os
from fastapi.staticfiles import StaticFiles
import dotenv
from pprint import pprint


templates = Jinja2Templates(directory='./templates/')

app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")

opsch_conn_info = {
            "hosts" : f"https://192.168.52.196:8200",
            "id" : "admin",
            "pwd" : "admin"
        }

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

    
@app.get("/search")
async def search(q):
    print(q)
    auto_complete = AutoComplete(opsch_conn_info)    
    search_res = auto_complete.run(q)    
    data = search_res
    pprint(data)
    return data
    

if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8080)