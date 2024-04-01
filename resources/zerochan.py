import requests
from bs4 import BeautifulSoup as bs

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
