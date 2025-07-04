# apitools/weather.py

import requests

def get_weather(prompt: str) -> str:
    """
    Extract a location from the prompt and return current weather.
    Expects prompts like "weather in London" or "what's the weather at Paris?"
    """
    # crude location extraction
    parts = prompt.lower().split("in ")
    if len(parts) < 2:
        return "Specify a location, bro. e.g., 'weather in Nairobi'."
    location = parts[-1].strip().rstrip('?')
    # Free geocoding
    geo = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}").json()
    results = geo.get("results")
    if not results:
        return f"Couldn't find `{location}`."
    lat, lon = results[0]["latitude"], results[0]["longitude"]
    # Free weather fetch
    weather = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    ).json()
    cw = weather.get("current_weather", {})
    return (
        f"Weather in {location.title()}: "
        f"{cw.get('temperature')}°C, wind {cw.get('windspeed')} km/h, "
        f"conditions code {cw.get('weathercode')}."
    )
