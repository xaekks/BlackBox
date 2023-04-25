
import random 

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    string = {"hello?"}
    return string


from resources.nekos import nekos

@app.get("/nekos") # to get random nekos images
async def nekos():
    nekos = random.choice(nekos)
    string = {"url": nekos}
    return string 
     
