
from uuid import uuid4
import requests, re
import base64


async def BlackBoxChat(user_id, messages):
    data = {
        "messages": messages,
        "user_id": user_id,
        "codeModelMode": True,
        "agentMode": {},
        "trendingAgentMode": {},
    }
  
    headers = {"Content-Type": "application/json"}
    url = "https://www.blackbox.ai/api/chat"
  
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_text = response.text
        cleaned_response_text = re.sub(r'^\$?@?\$?v=undefined-rv\d+@?\$?|\$?@?\$?v=v\d+\.\d+-rv\d+@?\$?', '', response_text)
        text = cleaned_response_text.strip()[2:]
        if "$~~~$" in text:
            text = re.sub(r'\$~\$.*?\$~\$', '', text, flags=re.DOTALL)
        data = {'reply': text}
      
        return data
    return {'reply': f'Sorry something went wrong status code: {str(response.status_code)}'}


async def BlackBox(image, prompt):
    user_id = str(uuid4())  
    file_name = user_id + '.jpeg'
  
    if image and len(image) > 50:
      
        files = {
            'fileName': (None, file_name),
            'userId': (None, user_id),
            'image': (file_name, image, 'image/jpeg')
        }
      
        api_url = "https://www.blackbox.ai/api/upload"
      
        response = requests.post(api_url, files=files)
        if response.status_code == 200:
            response_json = response.json()
            messages = [
                {
                    "role": "user", 
                    "content": response_json['response'] + "\n#\n" + prompt
                }
            ]
            reply = await BlackBoxChat(user_id, messages)
            return reply
          
        else:
            return {'reply': f'File uploading went wrong status code: {str(response.status_code)}'}
    else:
        messages = [
            {
                "role": "user", 
                "content": prompt
            }
        ]
        reply = await BlackBoxChat(user_id, messages)
        return reply
    
