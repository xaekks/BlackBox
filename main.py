
import random, strings

from resources.nekos import neko

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return strings.HOME


@app.get("/neko")
async def Nekos():
    url = random.choice(neko)
    string = {"url": url}
    return string 
     
