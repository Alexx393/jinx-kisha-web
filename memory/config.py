import os
from core.config import get_config

cfg = get_config()
MEMORY_META_PATH = cfg["memory"]["meta"]
MEMORY_DB_PATH = cfg["memory"]["path"]

# Ensure folders exist
os.makedirs(os.path.dirname(MEMORY_META_PATH), exist_ok=True)
os.makedirs(os.path.dirname(MEMORY_DB_PATH), exist_ok=True)
