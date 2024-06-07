import requests
from bs4 import BeautifulSoup as bs

baseUrl = "https://anitaku.so"

def login():
    email = "gojosatoru3221@proton.me"
    password = "1000gojo"
    s = requests.session()
    animelink = f"{baseUrl}/login.html"
    response = s.get(animelink)
    response_html = response.text
    soup = bs(response_html, "html.parser")
    source_url = soup.select('meta[name="csrf-token"]')
    token = source_url[0].attrs["content"]

    data = f"email={email}&password={password}&_csrf={token}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; vivo 1916) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
        "authority": "gogo-cdn.com",
        "referer": f"{baseUrl}/",
        "content-type": "application/x-www-form-urlencoded",
    }
    s.headers = headers

    r = s.post(animelink, data=data, headers=headers)

    if r.status_code == 200:
        s.close()
        print("Gogoanime cookie generated successfully")
        return s.cookies.get_dict().get("auth")

def get_source(episode_id):
    try:
        auth_cookie = login()
        headers = {
            'Cookie': f'auth={auth_cookie}',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; vivo 1916) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'
        }
        response = requests.get(f'{baseUrl}/{episode_id}', headers=headers)
        html = response.text
        soup = bs(html, 'html.parser')
        links_data = {}
        links = soup.select('div.cf-download a')
        for link in links:
            links_data[link.get_text().strip()] = link['href'].strip()
        return links_data
    except Exception as e:
        return e
