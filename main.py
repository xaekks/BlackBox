import random
import requests
import cleverbotfreeapi
import json
import os


from pydantic import BaseModel
from typing import List
from resources import anime, quote
from resources.tools import balckbox_requests, youtube_dl, imagine, zerochan as get_zerochan, get_couples, translate_text, get_urbandict, get_ai
from resources.fonts import get_fonts
from resources.grs import GoogleReverseImageSearch
from resources.insta import saveig
from resources.code_runner import CodeRunner, run
from resources.gpt import GptReply, gpt_func
from resources.trhozory import hozory_translate
from resources.stack import search_stackoverflow
from resources.gemini import gemini_func, Gemini
from resources.truth_dare import truth_string, dare_string
from resources.pinterest import pin, get_pinterest_video_url
from resources.gogo import get_source

from fastapi import FastAPI, HTTPException, File, UploadFile, Form

from fastapi.responses import FileResponse, Response 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


credits = {'credits': 'Nandha API'}


@app.get("/", include_in_schema=False)
def serve_index():
    index_file = "index.html"
    return FileResponse(index_file)





####################################################################################################################################


@app.get('/truth', tags=['Game'])
def truth():
    string = random.choice(truth_string)
    nandha = {"truth": string, **credits}
    return nandha

@app.get('/dare', tags=['Game'])
def truth():
    string = random.choice(dare_string)
    nandha = {"dare": string, **credits}
    return nandha

####################################################################################################################################

#tools


@app.post('/ytdl', tags=['Tools'])
async def youtube(url: str):
    try:
        return youtube_dl(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get('/htranslate', tags=['Tools'])
def hozory(text:str, code:str):
   try:
     results = hozory_translate(text, code)
     return results
   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))


@app.get("/insta", tags=['Tools'])
async def saveig_endpoint(link: str):
    try:       
        downloaded_media = saveig(link)
        nandha = {"url": downloaded_media, **credits}
        return nandha
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/pinterest", tags=['Tools'])
async def search(query: str):
    result_images = pin(query)
    return {"images": result_images, "count": len(result_images), **credits}

@app.get("/stackoverflow", tags=['Tools'])
async def stackoverflow_search(query: str):
    questions = search_stackoverflow(query)
    if questions:
        return {"results": questions, **credits}
    else:
        return {"message": "No questions found for the query."}

@app.get("/vidpinterest", tags=['Tools'])
async def get_pinterest_video(pinterest_url: str):
    """
    To Get Download link of pinterest urls
    """
    video_url = get_pinterest_video_url(pinterest_url)
    if video_url:
        return {"video_url": video_url, **credits}
    else:
        return {"message": "No video found on the page."}

@app.post("/reverse", tags=['Tools'])
async def reverse_image_search(img_url: str):
    google = GoogleReverseImageSearch()
    search_results = google.reverse_search_image(address=img_url)
    nandha = {"url": search_results, **credits}
    return nandha

@app.get("/gtranslate", tags=['Tools'])
async def translate(query: str, target_lang: str):
    """Translate Any Text To Any Language
    
    - query: Text To Translate
    - lang code : Get This From Here [https://telegra.ph/Lang-Codes-03-19-3]
    """
    translation = await translate_text(query, target_lang)
    if translation:
        return {"translation": translation, **credits}

@app.post("/run", tags=['Tools'])
async def run_code(

  code: str = Form("print('hello')"),
  lang: str = Form("python")
  
  ):
    """
    `Available Langauges`:
    ```
    Matlab, bash, befunge93, bqn, brachylog, brainfuck, 
    cjam, clojure, cobol, coffeescript, cow, crystal, 
    dart, dash, typescript, javascript, basic.net, fsharp.net, 
    csharp.net, fsi, dragon, elixir, emacs, emojicode, erlang,
    file, forte, forth, freebasic, awk, c, c++, d, fortran, go,
    golfscript, groovy, haskell, husk, iverilog, japt, java, 
    jelly, julia, kotlin, lisp, llvm_ir, lolcode, lua, csharp, 
    basic, nasm, nasm64, nim, javascript, ocaml, octave, osabie, 
    paradoc, pascal, perl, php, ponylang, prolog, pure, powershell,
    pyth, python2, python, racket, raku, retina, rockstar, rscript, 
    ruby, rust, samarium, scala, smalltalk, sqlite3, swift, 
    typescript, vlang, vyxal, yeethon, zig```
    """
    res = await run(code, lang)
    nandha = {**res, **credits}
    return nandha
    

@app.get("/ud", tags=["Tools"])
async def search_ud(query: str, max: int = 10):
    """Search meanings of words on Urban Dictionary

    - query: Word whose meaning you want
    - max: Max definitions to get
    """

    data = await get_urbandict(query, max)
    nandha = {**data, **credits}
    return nandha
  

@app.get('/styletext', tags=['Tools'])
async def style_text(query: str):
    fonts = await get_fonts(query)
    nandha = {
        'query': query,
        'fonts': fonts, **credits
}
    return nandha



####################################################################################################################################


@app.get("/zerochan", tags=['Anime'])
async def ZeroChanWeb(name: str):
    mm = await get_zerochan(name)
    if not bool(mm) == False:
        images = {'images': mm, **credits}
        return images
    else:
        return {'Failed To Fetch 404 Try Other Names.'}


@app.get("/animequote", tags=['Anime'])
async def anime_quote():
   url = random.choice(quote.anime_quote_url)
   return { "url": url, **credits}
    
@app.get("/neko", tags=['Anime'])
async def neko():
    url = random.choice(anime.neko)
    nandha = {"url": url, **credits}
    return nandha
    

@app.get("/couples", tags=['Anime'])
async def get_couple_images():
        res = await get_couples()
        nandha = {**res, **credits}
        return nandha
        

####################################################################################################################################


@app.get("/chatbot/{prompt}", tags=['AI'])
async def chatbot(prompt: str):
    res = cleverbotfreeapi.cleverbot(prompt)
    nandha = {'text': res, **credits}
    return nandha

@app.get("/imagine", tags=['AI'])
async def imagine_draw(prompt: str):
    xx = await imagine(prompt)
    nandha = xx['image']   
    return Response(content=nandha, media_type='image/jpeg')

@app.post("/nandhaai", tags=['AI'])
async def nandha_ai(
  gemini: str = Form(...),
  role: str = Form(...)
  
  ):
    result = await gemini_func(text, role)
    return result


class Prompt(BaseModel):
      prompt: str

@app.post("/blackbox", tags=['AI'])
async def blackbox(
  prompt: str = Form(...)
):
     res = await balckbox_requests(prompt)
     nandha = {**res, **credits}
     return nandha




@app.post("/chatgpt", tags=['AI'])
async def ChatGPT(
   prompt: str = Form(...),
   system: str = Form('helpful friendly chat bot')
):
     res = gpt_func(prompt, system)
     nandha = {**res, **credits}
     return nandha


@app.get("/ai/{model}/{prompt}", tags=['AI'])
async def ai_models(model: str , prompt: str):
         res = await get_ai(model, prompt)
         nandha = {**res, **credits}
         return nandha

####################################################################################################################################


@app.get("/gogosource/{episode_id}", include_in_schema=False)
async def gogosource(episode_id: str):
    try:
         res = get_source(episode_id)
         nandha = {**res, **credits}
         return nandha
    except Exception as e:
        return {error : e.message}

      

     
     

    
     
