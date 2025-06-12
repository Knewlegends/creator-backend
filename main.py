from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, os

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ScriptRequest(BaseModel):
    prompt: str

@app.post("/generate-script")
async def generate_script(req: ScriptRequest):
    openai_key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {openai_key}"}
    json_data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": req.prompt}]
    }
    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
    return res.json()

class VoiceRequest(BaseModel):
    script: str
    voice_id: str

@app.post("/generate-voice")
async def generate_voice(req: VoiceRequest):
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    headers = {
        "xi-api-key": eleven_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": req.script,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    res = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{req.voice_id}", headers=headers, json=payload)
    return res.json()
