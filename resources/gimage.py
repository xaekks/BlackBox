import requests
from bs4 import BeautifulSoup
import os
import urllib.request
from typing import List
import os

async def scrape_and_save_image(query: str, limit: int = 5) -> List[str]:
    # Scrape images from Google
    search_url = f"https://www.google.com/search?tbm=isch&q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    directory = f"{query}_images"
    if not os.path.exists(directory):
        os.makedirs(directory)

    downloaded_images = []
    downloaded = 0
    for img in soup.find_all('img'):
        if downloaded >= limit:
            break
        try:
            url = img['src']
            if url.startswith('http'):
                filename = f"{directory}/{downloaded+1}.jpg"
                urllib.request.urlretrieve(url, filename)
                downloaded_images.append(f"https://nandha-api.onrender.com/{filename}")
                downloaded += 1
        except KeyError:
            pass
    return downloaded_images

