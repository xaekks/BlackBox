import requests
import bs4
import re

def saveig(link):
    try:
        url = link.replace("instagram.com", "ddinstagram.com")
        url = url.replace("==", "%3D%3D")
        if url.endswith("="):
            return url[:-1]
        
        ddinsta = False
        getdata = requests.get(url).text
        soup = bs4.BeautifulSoup(getdata, 'html.parser')
        
        # post
        if "/p/" in url:
            meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
            if meta_tag.ok:
                res = meta_tag.json()
                meta = re.findall(r'href="(https?://[^"]+)"', res['data'])
                content_value = meta[0]
            else:
                raise ValueError("Api Error")
        
        # story
        elif "stories" in url:
            meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
            if meta_tag.ok:
                res = meta_tag.json()
                meta = re.findall(r'href="(https?://[^"]+)"', res['data'])
                content_value = meta[0]
            else:
                raise ValueError("Api Error")
        # video/reel
        else:
            meta_tag = soup.find('meta', attrs={'property': 'og:video'})
            if meta_tag:
                content_value = f"https://ddinstagram.com{meta_tag['content']}"
                ddinsta = True
            else:
                meta_tag = requests.post("https://saveig.app/api/ajaxSearch", data={"q": link, "t": "media", "lang": "en"})
                if meta_tag.ok:
                    res = meta_tag.json()
                    meta = re.findall(r'href="(https?://[^"]+)"', res['data'])
                    content_value = meta[0]
                else:
                    raise ValueError("Api Error")
        
        if ddinsta:
            return content_value
        else:
            return content_value
        
    except Exception as e:
        raise ValueError(f"Api Error")

