
import random
import strings
import requests
import cleverbotfreeapi
import json
import secureme


from resources import anime, game, quote

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()



class CodeRequest(BaseModel):
    code: str
    language: str



@app.get("/", include_in_schema=False)
def serve_index():
    index_file = "index.html"
    return FileResponse(index_file)


@app.get("quote", tags=['quote'])
async def anime_quote():
   url = random.choice(quote.anime_quote_url)
   return { "url": url }
    
@app.get("/neko", tags=['images'])
async def neko():
    url = random.choice(anime.neko)
    return {"url": url}



def run(code, language):
    res = requests.get("https://emkc.org/api/v2/piston/runtimes")
    langs = next((lang for lang in res.json() if lang["language"] == language), None)

    if langs is not None:
        data = {
            "language": language,
            "version": langs["version"],
            "files": [
                {
                    "name": f"file.{langs['aliases'][0] if langs['aliases'] else 'xz'}",
                    "content": code,
                },
            ],
        }

        r = requests.post("https://emkc.org/api/v2/piston/execute", json=data)

        if r.status_code == 200:
            return {
                "language": r.json()["language"],
                "version": r.json()["version"],
                "code": data["files"][0]["content"].strip(),
                "output": r.json()["run"]["output"].strip()
            }
        else:
            raise HTTPException(status_code=r.status_code, detail=f"Status Text: {r.reason}")
    else:
        raise HTTPException(status_code=404, detail="Error: language is not found.")

@app.post("/run")
async def run_code(code_request: CodeRequest):
    return run(code_request.code, code_request.language)
    



@app.get("/chatbot/{prompt}", tags=['AI'])
async def chatbot(prompt: str):
    res = cleverbotfreeapi.cleverbot(prompt)
    response = {'text': res}
    return response



@app.get("/ai/{model}/{prompt}", tags=['AI'])
async def ai_models(model: str , prompt: str):
     models = {
          'bard': 20,
          'gpt': 5,
          'palm': 1}
     
     names = list(models.keys())
     if model not in names:
           return "available models names: [bard, gpt, palm]"
     else:
         id = int(models[model])
         url = "https://lexica.qewertyy.dev/models?model_id={id}&prompt={prompt}"
         response = requests.post(url.format(id=id, prompt=prompt)).json()
         return response 



@app.get('/encrypt/{string}', tags=['tools'])
async def encrypt(string: str):
     text = secureme.encrypt(string)
     encryption = json.dumps({'encrypt': text})
     return encryption 

@app.get('/decrypt/{string}', tags=['tools'])
async def encrypt(string: str):
     text = secureme.decrypt(string)
     decryption = json.dumps({'decrypt': text})
     return decryption 
     
    

    
@app.get("/guess", tags=['tools'])
async def ward():
     words_list = game.COMMON_WORDS
     random.shuffle(words_list)
     answer = random.choice(words_list)
     chars = list(answer)
     random.shuffle(chars)
     question = '-'.join(chars)
     return {
        "question": question,
        "answer": answer 
     }

    
     
