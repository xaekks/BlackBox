
import random
import requests
import cleverbotfreeapi
import json


from typing import List
from resources import anime, quote
from resources.tools import imagine, zerochan as get_zerochan, get_couples, translate_text, run, get_urbandict, get_ai
from resources.fonts import get_fonts
from resources.grs import GoogleReverseImageSearch
from resources.insta import saveig
from resources.trhozory import hozory_translate
from resources.stack import search_stackoverflow
from resources.pinterest import pin, get_pinterest_video_url
from resources.gogo import get_source
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, Response 

app = FastAPI()




credits = {'credits': 'Nandha API'}


@app.get("/", include_in_schema=False)
def serve_index():
    index_file = "index.html"
    return FileResponse(index_file)



@app.get('/htranslate', tags=['tools'])
def hozory(text:str, code:str):
   try:
     results = hozory_translate(text, code)
     return results
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))


@app.get("/insta", tags=['tools'])
async def saveig_endpoint(link: str):
    try:       
        downloaded_media = saveig(link)
        nandha = {"url": downloaded_media, **credits}
        return nandha
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pinterest", tags=['tools'])
async def search(query: str):
    result_images = pin(query)
    return {"images": result_images, "count": len(result_images), **credits}

@app.get("/stackoverflow", tags=['tools'])
async def stackoverflow_search(query: str):
    questions = search_stackoverflow(query)
    if questions:
        return {"results": questions, **credits}
    else:
        return {"message": "No questions found for the query."}

@app.get("/vidpinterest", tags=['tools'])
async def get_pinterest_video(pinterest_url: str):
    """
    To Get Download link of pinterest urls
    """
    video_url = get_pinterest_video_url(pinterest_url)
    if video_url:
        return {"video_url": video_url, **credits}
    else:
        return {"message": "No video found on the page."}
        
@app.get("/zerochan", tags=['anime'])
async def ZeroChanWeb(name: str):
    mm = await get_zerochan(name)
    if not bool(mm) == False:
        images = {'images': mm, **credits}
        return images
    else:
        return {'Failed To Fetch 404 Try Other Names.'}


@app.get("/imagine", tags=['AI'])
async def imagine_draw(prompt: str):
    xx = await imagine(prompt)
    nandha = xx['image']   
    return Response(content=nandha, media_type='image/jpeg')

@app.post("/reverse", tags=['tools'])
async def reverse_image_search(img_url: str):
    google = GoogleReverseImageSearch()
    search_results = google.reverse_search_image(address=img_url)
    nandha = {"url": search_results, **credits}
    return nandha

        
@app.get("/animequote", tags=['images'])
async def anime_quote():
   url = random.choice(quote.anime_quote_url)
   return { "url": url, **credits}
    
@app.get("/neko", tags=['images'])
async def neko():
    url = random.choice(anime.neko)
    nandha = {"url": url, **credits}
    return nandha
    


@app.get("/couples", tags=['images'])
async def get_couple_images():
        res = await get_couples()
        nandha = {**res, **credits}
        return nandha
        

@app.get("/gtranslate", tags=['tools'])
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
    nandha = {**res, **credits}
    return nandha
    

@app.get("/ud", tags=["tools"])
async def search_ud(query: str, max: int = 10):
    """Search meanings of words on Urban Dictionary

    - query: Word whose meaning you want
    - max: Max definitions to get
    """

    data = await get_urbandict(query, max)
    nandha = {**data, **credits}
    return nandha


@app.get("/chatbot/{prompt}", tags=['AI'])
async def chatbot(prompt: str):
    res = cleverbotfreeapi.cleverbot(prompt)
    nandha = {'text': res, **credits}
    return nandha



@app.get("/ai/{model}/{prompt}", tags=['AI'])
async def ai_models(model: str , prompt: str):
         res = await get_ai(model, prompt)
         nandha = {**res, **credits}
         return nandha


@app.get('/styletext', tags=['tools'])
async def style_text(query: str):
    fonts = await get_fonts(query)
    nandha = {
        'query': query,
        'fonts': fonts, **credits
}
    return nandha


@app.get("/gogosource/{episode_id}", include_in_schema=False)
async def gogosource(episode_id: str):
         res = get_source(episode_id)
         nandha = {**res, **credits}
         return nandha

      

     
     

    
     
