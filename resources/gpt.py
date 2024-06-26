
import requests
import uuid


from fastapi import HTTPException
from pydantic import BaseModel


class GptReply(BaseModel):
      prompt: str
      system: str = "You're a helpful and friendly chat bot"
  

auth_code = 'wb62oTDbOKMJZ' 
cookies_code = 'fTcjnRLr8E3IMrksLSrs'
api_url = "https://liaobots.work/api/chat"



def gpt_func(prompt: str, system: str):
    headers = {
        "Cookie": f"gkp2={cookies_code}",
        "Origin": "https://liaobots.work",
        "Referer": "https://liaobots.work/en",
        "Sentry-Trace": f"{str(uuid.uuid4())}-{str(uuid.uuid4())}",
        "X-Auth-Code": auth_code,
    }
    payload = {
       "conversationId": str(uuid.uuid4()),
       "model":{"id":"gpt-4o-free","name":"GPT-4o-free","maxLength":31200,"tokenLimit":7800,"model":"ChatGPT","provider":"OpenAI","context":"8K"},
       "messages":[{"role":"user","content": prompt}],
       "key":"","prompt": system
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return { "reply": response.text }
    else:
        raise HTTPException(status_code=404, detail=f"Request Status code: {response.status_code}")
       


