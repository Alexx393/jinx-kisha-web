import os
import json
from core.config import get_config

cfg = get_config()
META_PATH = cfg["memory"]["meta"]

# === Default ===
DEFAULT_META = {
    "lessons": [],
    "topics": [],
    "alerts": [],
    "custom_flags": {}
}

# === Helpers ===
def _ensure_meta_exists():
    if not os.path.exists(META_PATH):
        save_meta(DEFAULT_META)

def load_meta():
    _ensure_meta_exists()
    with open(META_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_META.copy()

def save_meta(data):
    # Atomic write for safety
    temp_path = META_PATH + ".tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, META_PATH)

# === Meta ops ===
def add_lesson(keyword: str):
    keyword = keyword.strip().lower()
    if not keyword:
        return
    meta = load_meta()
    if keyword not in meta["lessons"]:
        meta["lessons"].append(keyword)
        save_meta(meta)

def flag_topic(topic: str):
    topic = topic.strip().lower()
    if not topic:
        return
    meta = load_meta()
    if topic not in meta["topics"]:
        meta["topics"].append(topic)
        save_meta(meta)

def set_custom_flag(key: str, value):
    meta = load_meta()
    meta["custom_flags"][key] = value
    save_meta(meta)

def get_custom_flag(key: str, default=None):
    meta = load_meta()
    return meta["custom_flags"].get(key, default)
