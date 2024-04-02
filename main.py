
import random
import strings
import requests
import cleverbotfreeapi
import json
import secureme


from resources import anime, game, quote
from resources.tools import zerochan as get_zerochan, get_couples, translate_text, run, get_urbandict, get_ai, get_guess_word
from resources.fonts import get_fonts
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()




credits = {'credits': 'Nandha API'}


@app.get("/", include_in_schema=False)
def serve_index():
    index_file = "index.html"
    return FileResponse(index_file)


@app.get("/zerochan", tags=['anime'])
async def ZeroChanWeb(name: str):
    mm = await get_zerochan(name)
    if not bool(mm) == False:
        images = {'images': mm, **credits}
        return images
    else:
        return {'Failed To Fetch 404 Try Other Names.'}
       
            
                
        

@app.get("/animequote", tags=['images'])
async def anime_quote():
   url = random.choice(quote.anime_quote_url)
   return { "url": url }
    
@app.get("/neko", tags=['images'])
async def neko():
    url = random.choice(anime.neko)
    nandha = {"url": url, **credits}
    return nandha
    


@app.get("/couples", tags=['images'])
async def get_couple_images():
        res = await get_couples()
        nandha = res.update(credits)
        return nandha
    else:
        return {"error": "Failed to fetch images"}
        

@app.get("/translate", tags=['tools')
async def translate(query: str, target_lang: str):
    """Translate Any Text To Any Language
    
    - query: Text To Translate
    - lang code : Get This From Here [https://telegra.ph/Lang-Codes-03-19-3]
    """
    translation = await translate_text(query, target_lang)
    if translation:
        return {"translation": translation, **credits}



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
    res = await run(code, language)
    nandha = res.update(credits)
    return nandha
    

@app.get("/ud", tags=["tools"])
async def search_ud(query: str, max: int = 10):
    """Search meanings of words on Urban Dictionary

    - query: Word whose meaning you want
    - max: Max definitions to get
    """

    data = await get_urbandict(query, max)
    nandha = data.update(credits)
    return nandha


@app.get("/chatbot/{prompt}", tags=['AI'])
async def chatbot(prompt: str):
    res = cleverbotfreeapi.cleverbot(prompt)
    nandha = {'text': res, **credits}
    return nandha



@app.get("/ai/{model}/{prompt}", tags=['AI'])
async def ai_models(model: str , prompt: str):
         res = await get_ai(model, prompt)
         nandha = res.update(credits)
         return nandha


@app.get('/styletext', tags=['tools'])
async def style_text(query: str):
    fonts = await get_fonts(query)
    nandha = {
        'query': query,
        'fonts': fonts, **credits
}
    return nandha


@app.get('/encrypt/{string}', tags=['tools'])
async def encrypt(string: str):
     text = secureme.encrypt(string)
     nandha = {'encrypt': text, **credits}
     return nandha

@app.get('/decrypt/{string}', tags=['tools'])
async def encrypt(string: str):
     text = secureme.decrypt(string)
     nandha = {'decrypt': text, **credits}
     return nandha
     
      
@app.get("/guess", tags=['tools'])
async def get_word():
     res = await get_guess_word()
     nandha = res.update(credits)
     return nandha
     
     

    
     
