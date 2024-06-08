from pydantic import BaseModel
import requests
import json

API_KEY = "AIzaSyCV7FjStkDviA_Evd20rNRoB1dL5kDQzeg"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class Gemini(BaseModel):
    text: str
    role: str

def gemini_func(text: str, role: str):
    data = Gemini(text=text, role=role)
    headers = {"Content-Type": "application/json"}
  
    response = requests.post(API_URL, headers=headers, json=data.dict())
    data = response.json()
  
    if data.get('candidates'):
        return {"reply": data['candidates'][0]['content']['parts'][0]['text']}
    else:
        return {"error": "API error"}

