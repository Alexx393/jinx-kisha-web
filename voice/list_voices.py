# voice/list_voices.py

import os
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key="sk_a303eb57cc126a53b6a7ac1f794a971543ba5c2c403ecf4e"
)

print("✨ Available Voices:")
for v in client.voices.get_all().voices:
    print(f"- {v.name} (ID: {v.voice_id})")
