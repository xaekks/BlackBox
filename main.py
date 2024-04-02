
import random
import strings
import requests
import cleverbotfreeapi
import json
import secureme


from resources import anime, game, quote
from resources.zerochan import zerochan as get_zerochan
from resources.fonts import get_fonts
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()







@app.get("/", include_in_schema=False)
def serve_index():
    index_file = "index.html"
    return FileResponse(index_file)


@app.get("/zerochan", tags=['anime'])
async def ZeroChanWeb(name: str):
    mm = await get_zerochan(name)
    if not bool(mm) == False:
        images = {'images': mm}
        return images
    else:
        return {'Failed To Fetch 404 Try Other Names.'}
       
            
                
        

@app.get("/animequote", tags=['quote'])
async def anime_quote():
   url = random.choice(quote.anime_quote_url)
   return { "url": url }
    
@app.get("/neko", tags=['images'])
async def neko():
    url = random.choice(anime.neko)
    return {"url": url}


@app.get("/couple", tags=['images'])
async def get_couple_images():
    api_url = "https://api.erdwpe.com/api/randomgambar/couplepp"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        male_image = data["result"]["male"]
        female_image = data["result"]["female"]
        return {"male_image": male_image, "female_image": female_image, "Powered By": "Nandha API"}
    else:
        return {"error": "Failed to fetch images"}
        


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

@app.get("/run", tags=['tools'])
async def run_code(code: str, language: str):
    """
    `AVAILABLE LANGAUGES`:
    Matlab, bash, befunge93, bqn, brachylog, brainfuck, 
    cjam, clojure, cobol, coffeescript, cow, crystal,
    dart, dash, typescript, javascript, basic.net,
    fsharp.net, csharp.net, fsi, dragon, elixir,
    emacs, emojicode, erlang, file, forte, forth, 
    freebasic, awk, c, c++, d, fortran, go, golfscript, 
    groovy, haskell, husk, iverilog, japt, java, jelly, 
    julia, kotlin, lisp, llvm_ir, lolcode, lua, csharp, 
    basic, nasm, nasm64, nim, javascript, ocaml, octave,
    osabie, paradoc, pascal, perl, php, ponylang, prolog, pure, 
    powershell, pyth, python2, python, racket, raku, retina, rockstar, 
    rscript, ruby, rust, samarium, scala, smalltalk, sqlite3, swift, typescript, 
    vlang, vyxal, yeethon, zig
    """
    return run(code, language)
    



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


@app.get('/styletext', tags=['tools'])
async def style_text(query: str):
    fonts = await get_fonts(query)
    nandha = {
        'query': query,
        'fonts': fonts
}
    return nandha


@app.get('/encrypt/{string}', tags=['tools'])
async def encrypt(string: str):
     text = secureme.encrypt(string)
     encryption = {'encrypt': text}
     return encryption 

@app.get('/decrypt/{string}', tags=['tools'])
async def encrypt(string: str):
     text = secureme.decrypt(string)
     decryption = {'decrypt': text}
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

    
     
