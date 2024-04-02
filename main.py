
import random
import strings
import requests
import cleverbotfreeapi
import json
import secureme


from resources import anime, game, quote
from resources.tools import zerochan as get_zerochan, run, get_urbandict, translate_text
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


@app.get("/couples", tags=['images'])
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
    

@app.get("/ud", tags=["tools"])
async def search_ud(query: str, max: int = 10):
    """Search meanings of words on Urban Dictionary

    - query: Word whose meaning you want
    - max: Max definitions to get
    """

    data = await get_urbandict(query, max)
    return data

@app.get("/translate", tags["tools")
def translate(query: str, target_lang: str):
    """Translate Any Text To Any Language
    
    - query: Text To Translate
    - lang code : Get This From Here [https://telegra.ph/Lang-Codes-03-19-3]
    """
    translation = translate_text(query, target_lang)
    if translation:
        return {"translation": translation}
   

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

    
     
