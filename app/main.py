from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import openai
import httpx

# Load environment
load_dotenv()

# API KEYS
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# OpenAI client setup
openai.api_key = OPENAI_API_KEY

# FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Kisha is online and listening 👂"}

@app.get("/config")
async def config_check():
    return {
        "OPENAI_API_KEY": OPENAI_API_KEY[:5] + "..." if OPENAI_API_KEY else "❌ Not Set",
        "ELEVEN_API_KEY": ELEVEN_API_KEY[:5] + "..." if ELEVEN_API_KEY else "❌ Not Set"
    }

@app.post("/ask")
async def ask_kisha(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return JSONResponse(content={"error": "Missing prompt"}, status_code=400)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Kisha, a superintelligent assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        reply = response['choices'][0]['message']['content']
        return {"response": reply}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/talk")
async def kisha_talk(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text:
        return JSONResponse(content={"error": "Missing text"}, status_code=400)

    url = "https://api.elevenlabs.io/v1/text-to-speech/XrExE9yKIg1WjnnlVkGX"  # Example voice ID

    headers = {
        "accept": "audio/mpeg",
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        # Save as temp audio
        audio_path = "voice_output.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)
        return {"message": f"Kisha spoke '{text}'", "audio_file": audio_path}
    else:
        return JSONResponse(content={"error": response.text}, status_code=response.status_code)
