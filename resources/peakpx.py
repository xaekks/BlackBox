import requests
from bs4 import BeautifulSoup

def get_image_links(url, key, limit):
    page = 1
    link_img = []

    while len(link_img) < limit:
        data = requests.get(f"{url}&page={page}").content
        soup = BeautifulSoup(data, "html.parser")
        ul = soup.find("ul", id="list_ul").find_all("li")

        for li in ul:
            try:
                img = li.find("img")["data-srcset"].split(" ")[0]
                link_img.append(img)
                if len(link_img) >= limit:
                    break
            except:
                pass

        page += 1

    return link_img



