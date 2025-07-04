from elevenlabs import generate, play, set_api_key, Voice

# 🛑 Replace with your actual valid key
set_api_key("sk_a303eb57cc126a53b6a7ac1f794a971543ba5c2c403ecf4e")

audio = generate(
    text="Hey Alex, it's Kisha. Can you hear me now?",
    voice=Voice(voice_id="SAz9YHcvj6GT2YYXdXww"),  # River = husky emo girl
    model="eleven_multilingual_v2"
)

play(audio)
