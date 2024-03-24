
import random, strings

from resources import nekos, games

from lexica import AsyncClient
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




@app.get("/chatbot/{model}/{prompt}")
async def AI_CHAT(model: str, prompt: str):
    AI_MODEL = {
        "bard",
        "gpt",
        "gemini",
        "llama",
        "mistral",
        "palm"
    }

    if model not in AI_MODEL:
        x = f"try valid model: {AI_MODEL}"
        return x
    else:
        try:
            client = AsyncClient()
            language_model = getattr(locals()[model], model)
            response = await client.ChatCompletion(prompt, language_model)
            return response
        except Exception as e:
            return str(e)


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

    
     
