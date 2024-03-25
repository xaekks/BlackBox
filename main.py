
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


@app.get("/ai/{model}/{prompt}")
async def chatbot(model, prompt):
     models = {
          'bard': 20,
          'gpt': 5,
          'palm': 1}
     url = "https://lexica.qewertyy.dev/models?model_id={id}&prompt={prompt}"
     names = list(models.keys())
     if model not in names:
           return "available model names: bard, gpt, palm"
     else:
         id = models[model]
         response = requests.get(url.format(id=id, prompt=prompt)).json()
         return response 



@app.get("/word")
async def ward():
     words_list = games.COMMON_WORDS
     random.shuffle(words_list)
     word = random.choice(words_list)
     chars = list(word)
     random.shuffle(chars)
     guess = '-'.join(chars)
     return {
        "guess": guess,
        "word": word
     }

    
     
