import requests
import random
import time 
from urllib.parse import quoteq
from bs4 import BeautifulSoup as bs
from fastapi import HTTPException

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X6816C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36 OPR/81.1.4292.78446'}

async def imagine(prompt: str):
        api_url = "https://ai-api.magicstudio.com/api/ai-art-generator"
        form_data = {
        'prompt': prompt,
        'output_format': 'bytes',
        'request_timestamp': str(int(time.time())),
        'user_is_subscribed': 'false',
        }
        resp = requests.post(api_url, data=form_data)
        if resp.status_code == 200:
             return {
                 'image': resp.content }
        else:
           return {'Requtests Failed To Fetch 404'}
                
    
async def get_couples():
    api_url = "https://api.erdwpe.com/api/randomgambar/couplepp"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        male_image = data["result"]["male"]
        female_image = data["result"]["female"]
        nandha = {"male_image": male_image, "female_image": female_image}
        return nandha
    else:
        return {"error": "Failed to fetch images"}


async def get_ai(model: str, prompt: str):
      models = {
          'bard': 20,
          'gpt': 5,
          'palm': 1
      }
     
      names = list(models.keys())
  
      if model not in names:
           return {
             "Invalid model": "Available Models: [bard, gpt, palm]"
           }
      else:
         id = int(models[model])
         prompt = quote(prompt)
         url = f"https://lexica.qewertyy.dev/models?model_id={id}&prompt={prompt}"
         response = requests.post(url).json()
         return response


async def zerochan(string: str):
    url = f"https://www.zerochan.net/"+str(quote(string))
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
         soup = bs(response.text, 'html.parser')
         img_tags = soup.find_all('img')
         src_list = [img.get('src') for img in img_tags]
         return src_list
    return False


async def run(code, language):
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
        

async def get_urbandict(word, max=10):
    response = requests.get(f"http://api.urbandictionary.com/v0/define?term={quote(word)}")
    if response.status_code == 200:
        data = response.json()
        z = []
        for x in data["list"]:
            a = {}
            a["count"] = x["thumbs_up"] - x["thumbs_down"]
            a["data"] = x
            z.append(a)
        
        z = z[:max]
        
        def hhh(e):
            return e["count"]
        
        z.sort(key=hhh)
        z.reverse()
        
        results = []
        
        for i in z:
            ndict = {}
            ndict["definition"] = i["data"]["definition"]
            ndict["example"] = i["data"]["example"]
            results.append(ndict)
        
        json_data = {}
        json_data["success"] = True
        json_data["results"] = results
        return json_data
    else:
        return {"success": False, "error": "Failed to fetch data"}

async def translate_text(source_text, target_lang):
    response = requests.get(
        "https://translate.googleapis.com/translate_a/single",
        params={
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": source_text,
        },
    )
    if response.status_code == 200:
        translation = response.json()[0][0][0]
        return translation
    else:
        return {"success": False, "error": "Failed to fetch data"}
