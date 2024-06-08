from pydantic import BaseModel
import requests
import json

API_KEY = "AIzaSyCV7FjStkDviA_Evd20rNRoB1dL5kDQzeg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"


class Gemini(BaseModel):
    text: str
    role: str

def gemini_func(text: str, role: str):
    headers = {"Content-Type": "application/json"}
    payload = {
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

    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()
  
    if data.get('candidates') and data['candidates'][0].get('content'):
        return {"reply": data['candidates'][0]['content']['parts'][0]['text']}
    else:
        return {"reply": "Sorry Mortal I've Got Some Error Report in Support Chat"}

