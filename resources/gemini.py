
from pydantic import BaseModel

import requests
import json

API_KEY = "AIzaSyCV7FjStkDviA_Evd20rNRoB1dL5kDQzeg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"


class Gemini(BaseModel):
     text: str
     role: str


def GeminiFunc(text: str, role: str):
      headers = {
    "Content-Type": "application/json"
}

      data = {
    "contents": [
        {
            "parts": [
                {"text": text}
            ],
            "role": "User"
        }
    ],
    "system_instruction": {
        "parts": [
            {"text": role}
        ],
        "role": "model"
    }
}
      response = requests.post(API_URL, headers=headers, data=json.dumps(data))
      data = response.json()
  
      if date.get('candidates'):
            return {
              "reply": data['candidates'][0]['content']['parts'][0]['text']
            }
      else:
            return {
             "error": data
           }

        
    
