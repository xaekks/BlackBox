
import random, strings

from resources import nekos, games


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"WELCOME TO NANDHA-API"}



@app.get("/neko")
async def neko():
    url = random.choice(nekos.neko)
    string = {"url": url}
    return string


@app.get("/ward")
async def ward():
     ward_list = games.COMMON_WORDS
     random.shuffle(ward_list)
     ward = random.choice(ward_list)
     chars = list(ward)
     quess = '-'.join(chars)
     return {
        "guess": guess,
        "ward": ward
     }

    
     
