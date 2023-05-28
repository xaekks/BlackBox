
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


@app.get("/word")
async def ward():
     words_list = games.COMMON_WORDS
     random.shuffle(words_list)
     word = random.choice(words_list)
     chars = list(word)
     guess = '-'.join(chars)
     return {
        "guess": guess,
        "word": word
     }

    
     
