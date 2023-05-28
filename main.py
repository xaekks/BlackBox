
import random, strings , resources


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return strings.HOME


@app.get("/neko")
async def neko():
    url = random.choice(resources.nekos.neko)
    string = {"url": url}
    return string


@app.get("/ward")
async def ward():
     ward_list = resources.games.COMMON_WARDS
     random.shuffle(ward_list)
     ward = random.choice(ward_list)
     chars = list(ward)
     quess = '-'.join(chars)
     return {
        "guess": guess,
        "ward": ward
     }

    
     
