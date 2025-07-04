# voice/Kisha_voice.py

from elevenlabs import generate, play, Voice, set_api_key
import os

# Optional: Load from env or store securely
set_api_key("sk_a303eb57cc126a53b6a7ac1f794a971543ba5c2c403ecf4e")  # replace with your real key

VOICE_ID = "SAz9YHcvj6GT2YYXdXww"  # River voice (emo husky)
MODEL = "eleven_multilingual_v2"

def speak_text(text: str):
    try:
        audio = generate(
            text=text,
            voice=Voice(voice_id=VOICE_ID),
            model=MODEL
        )
        play(audio)
    except Exception as e:
        print(f"[Voice Error]: {e}")
