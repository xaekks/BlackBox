
import random 

from resources.nekos import neko

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    string = "welcome to Nandha-Api"
    return string


@app.get("/neko")
async def Nekos():
    url = random.choice(neko)
    string = {"url": url}
    return string 
     
