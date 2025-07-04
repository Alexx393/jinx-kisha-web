# apitools/scripture.py

import requests

def get_verse(query: str) -> str:
    """
    query: e.g. "John 3:16" or "Genesis 1:1"
    Returns the verse text or an error message.
    Uses bible-api.com (no API key needed).
    """
    ref = query.strip().replace(" ", "%20")  # URL-encode spaces
    url = f"https://bible-api.com/{ref}"
    try:
        resp = requests.get(url, timeout=10).json()
        if "error" in resp:
            return f"Verse {query} not found."
        verses = resp.get("verses", [])
        text = " ".join(v["text"].strip() for v in verses)
        return f"{resp.get('reference', query)} — {text}"
    except Exception as e:
        return f"⚠️ Scripture API error: {e}"
