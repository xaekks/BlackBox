import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def pin(query):
    headers = {
        'cookie': '_auth=1; _b="AVna7S1p7l1C5I9u0+nR3YzijpvXOPc6d09SyCzO+DcwpersQH36SmGiYfymBKhZcGg="; _pinterest_sess=TWc9PSZHamJOZ0JobUFiSEpSN3Z4a2NsMk9wZ3gxL1NSc2k2NkFLaUw5bVY5cXR5alZHR0gxY2h2MVZDZlNQalNpUUJFRVR5L3NlYy9JZkthekp3bHo5bXFuaFZzVHJFMnkrR3lTbm56U3YvQXBBTW96VUgzVUhuK1Z4VURGKzczUi9hNHdDeTJ5Y2pBTmxhc2owZ2hkSGlDemtUSnYvVXh5dDNkaDN3TjZCTk8ycTdHRHVsOFg2b2NQWCtpOWxqeDNjNkk3cS85MkhhSklSb0hwTnZvZVFyZmJEUllwbG9UVnpCYVNTRzZxOXNJcmduOVc4aURtM3NtRFo3STlmWjJvSjlWTU5ITzg0VUg1NGhOTEZzME9SNFNhVWJRWjRJK3pGMFA4Q3UvcHBnWHdaYXZpa2FUNkx6Z3RNQjEzTFJEOHZoaHRvazc1c1UrYlRuUmdKcDg3ZEY4cjNtZlBLRTRBZjNYK0lPTXZJTzQ5dU8ybDdVS015bWJKT0tjTWYyRlBzclpiamdsNmtpeUZnRjlwVGJXUmdOMXdTUkFHRWloVjBMR0JlTE5YcmhxVHdoNzFHbDZ0YmFHZ1VLQXU1QnpkM1FqUTNMTnhYb3VKeDVGbnhNSkdkNXFSMXQybjRGL3pyZXRLR0ZTc0xHZ0JvbTJCNnAzQzE0cW1WTndIK0trY05HV1gxS09NRktadnFCSDR2YzBoWmRiUGZiWXFQNjcwWmZhaDZQRm1UbzNxc21pV1p5WDlabm1UWGQzanc1SGlrZXB1bDVDWXQvUis3elN2SVFDbm1DSVE5Z0d4YW1sa2hsSkZJb1h0MTFpck5BdDR0d0lZOW1Pa2RDVzNySWpXWmUwOUFhQmFSVUpaOFQ3WlhOQldNMkExeDIvMjZHeXdnNjdMYWdiQUhUSEFBUlhUVTdBMThRRmh1ekJMYWZ2YTJkNlg0cmFCdnU2WEpwcXlPOVZYcGNhNkZDd051S3lGZmo0eHV0ZE42NW8xRm5aRWpoQnNKNnNlSGFad1MzOHNkdWtER0xQTFN5Z3lmRERsZnZWWE5CZEJneVRlMDd2VmNPMjloK0g5eCswZUVJTS9CRkFweHc5RUh6K1JocGN6clc1JmZtL3JhRE1sc0NMTFlpMVErRGtPcllvTGdldz0="; _ir=0'
    }
    url = f"https://id.pinterest.com/search/pins/?autologin=true&q={query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    result = []
    images = []

    for a_tag in soup.select('div > a'):
        img_tag = a_tag.find('img')
        if img_tag:
            image_src = img_tag.get('src')
            result.append(image_src)

    for image in result:
        if image is not None:
            images.append(image.replace('236', '736'))

    images.pop(0)  # Removing the first image link as it might be a placeholder
    return images


def expand_url(url):
    response = requests.head(url, allow_redirects=True)
    return response.url

def get_pinterest_video_url(url):
    try:
        if "pin.it" in url:
            url = expand_url(url)
        
        parsed_url = urlparse(url)
        final_url = f"https://{parsed_url.hostname}{parsed_url.path}"

        response = requests.get(final_url)
        if not response.ok:
            raise Exception(f"HTTP error {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        video_tag = soup.find("video")
        if video_tag:
            video_url = video_tag.get("src")
            out_url = video_url.replace("/hls/", "/720p/").replace(".m3u8", ".mp4")
            return out_url
        else:
            return None
    except Exception as e:
        return None

        
