import json
import requests
import logging
import threading

from core.config import get_config
from memory.memory_core import save_interaction, get_recent_context, search_memory
from memory.meta_memory import load_meta, save_meta
from apitools import scripture, weather, custom_tools
from voice.Kisha_voice import speak_text

# Setup logging
logging.basicConfig(filename="kisha.log", level=logging.INFO)

config = get_config()
MODEL_NAME = config['local']['default_model']
OLLAMA_API = config['local'].get('api_url', 'http://localhost:11434/api/generate')
FALLBACK_MODELS = config['local'].get('fallbacks', [])

kisha_mode = "vortex"

def process_with_ollama_http(prompt: str, model: str = MODEL_NAME) -> str:
    try:
        payload = {
            "model": model,
            "prompt": prompt
        }
        response = requests.post(OLLAMA_API, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        logging.exception(f"💥 Ollama HTTP error: {e}")
        return f"💥 Error with {model}: {str(e)}"

def check_for_tools(prompt: str):
    lower = prompt.lower()
    if "weather" in lower:
        return weather.get_weather(prompt)
    if "bible" in lower or "verse" in lower:
        return scripture.get_verse(prompt)
    if "tool:" in lower:
        return custom_tools.handle_custom_tool(prompt)
    return None

def apply_mode_styling(text: str) -> str:
    if kisha_mode == "chill":
        return chillify(text)
    elif kisha_mode == "silent":
        return "..."
    elif kisha_mode == "prophet":
        return f"📖 {text}"
    return text

def chillify(text: str) -> str:
    subs = {
        "Greetings.": "ssup,",
        "Hello.": "hey there!",
        "How can I assist you today?": "what’s up?",
        "I am": "I’m",
        "Let us": "let's",
        "I will": "i'll",
        "What brings you to this realm?": "what’s on your mind?",
        "It is": "it’s"
    }
    for old, new in subs.items():
        text = text.replace(old, new)
    return text

def kisha_response(user_input: str) -> str:
    tool_output = check_for_tools(user_input)
    if tool_output:
        styled = apply_mode_styling(tool_output)
        threading.Thread(target=speak_text, args=(styled,)).start()
        return styled

    if "what did i ask" in user_input.lower():
        recent = get_recent_context(limit=5)
        return f"Here's what I remember so far:\n\n{recent}"

    context = get_recent_context(limit=10) if config["memory"]["enabled"] else ""
    prompt = f"{context}\nUser: {user_input}\nKisha:" if context else f"User: {user_input}\nKisha:"

    response = process_with_ollama_http(prompt)

    if not response and FALLBACK_MODELS:
        for fallback in FALLBACK_MODELS:
            response = process_with_ollama_http(prompt, model=fallback)
            if response:
                break

    if config["memory"]["enabled"]:
        save_interaction(user_input, response)

    if config.get("self_improvement", {}).get("reflection", False):
        meta = load_meta()
        keyword = user_input.lower().split()[0]
        if keyword.isalpha() and keyword not in meta["lessons"]:
            meta["lessons"].append(keyword)
            save_meta(meta)

    styled_response = apply_mode_styling(response)
    threading.Thread(target=speak_text, args=(styled_response,)).start()
    return styled_response
