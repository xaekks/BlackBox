
import random 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    string = "welcome to Nandha-Api"
    return string


@app.get("/neko")
async def Nekos():
    string = {"url": "example.url"}
    return string 
     
