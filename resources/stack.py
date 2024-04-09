import requests

def search_stackoverflow(query):
    url = f"https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=relevance&q={query}&accepted=True&site=stackoverflow"
    response = requests.get(url)
    
    if response.status_code == 404:
        print("Query not found")
        return None

    data = response.json()
    results = []
    for item in data["items"][:10]:  # max 10
        title = item["title"]
        link = item["link"]
        tags = item["tags"]
        results.append({"text": title, "link": link, "tags": tags})

    return results


  
