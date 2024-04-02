import requests
from bs4 import BeautifulSoup as bs

from fastapi import HTTPException
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X6816C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36 OPR/81.1.4292.78446'}


async def zerochan(string: str):
    url = f"https://www.zerochan.net/"+str(string)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
         soup = bs(response.text, 'html.parser')
         img_tags = soup.find_all('img')
         src_list = [img.get('src') for img in img_tags]
         return src_list
    return False


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
        
