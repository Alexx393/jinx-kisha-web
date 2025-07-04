# core/config.py

import json
import os

def get_config():
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    CONFIG_PATH = os.path.join(ROOT, "core", "config.json")

    try:
        with open(CONFIG_PATH, "r") as f:
            cfg = json.load(f)

        # Always resolve memory paths absolutely:
        if "memory" in cfg:
            mem = cfg["memory"]
            if "path" in mem:
                mem["path"] = os.path.join(ROOT, mem["path"])
            if "meta" in mem:
                mem["meta"] = os.path.join(ROOT, mem["meta"])

        return cfg

    except Exception as e:
        print(f"💥 Error loading config.json: {e}")
        return {}
