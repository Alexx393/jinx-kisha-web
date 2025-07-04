import os
import sounddevice as sd
import numpy as np
from elevenlabs import ElevenLabs, Voice, Stream, stream
from dotenv import load_dotenv
import openai
import subprocess

# === Load .env vars if available ===
load_dotenv()

# === API KEYS ===
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY") or "your-elevenlabs-api-key"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "your-openai-api-key"

# === Initialize Clients ===
client = ElevenLabs(api_key=ELEVEN_API_KEY)
openai.api_key = OPENAI_API_KEY

# === Audio Settings ===
SAMPLERATE = 44100
DURATION = 5  # Seconds

# === Record Audio ===
def record_audio():
    print("🎤 Listening...")
    audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='float32')
    sd.wait()
    return audio.flatten()

# === Transcribe Audio with OpenAI Whisper ===
def transcribe_audio(audio):
    print("🧠 Transcribing...")
    audio_bytes = (audio * 32767).astype(np.int16).tobytes()
    with open("temp_input.wav", "wb") as f:
        f.write(audio_bytes)
    result = openai.Audio.transcribe("whisper-1", open("temp_input.wav", "rb"))
    return result["text"]

# === Call Kisha locally using Ollama ===
def get_kisha_response(prompt):
    print("⚡ Thinking...")
    result = subprocess.run(["ollama", "run", "kisha-vortex"], input=prompt.encode(), capture_output=True)
    response = result.stdout.decode().strip()
    print(f"Kisha 🧠: {response}")
    return response

# === Speak using ElevenLabs v2 Stream API ===
def speak(response):
    print("🔊 Speaking...")
    audio_stream = stream(
        text=response,
        voice=Voice(name="Bella"),  # Change if needed
        model="eleven_monolingual_v1"
    )
    Stream(audio_stream).play()

# === Main Loop ===
while True:
    try:
        audio = record_audio()
        prompt = transcribe_audio(audio)
        if not prompt.strip():
            continue
        print(f"You 💬: {prompt}")
        response = get_kisha_response(prompt)
        speak(response)
    except KeyboardInterrupt:
        print("🛑 Exiting.")
        break
    except Exception as e:
        print(f"💥 Error: {e}")
