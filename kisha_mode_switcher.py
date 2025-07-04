# File: kisha_mode_switcher.py

"""
This module sets up a dual-model architecture for Kisha: Vortex Mode (LLaMA3:8b) and Zen Mode (Zephyr:7b).
Kisha can switch between tactical intelligence (Vortex) and calm responsiveness (Zen).
"""

import subprocess
import json

# Paths to your Ollama models
MODELS = {
    "vortex": "kisha-vortex",  # LLaMA3:8b model fine-tuned with vortex core identity
    "zen": "zephyr:7b-beta"     # Chill lightweight model for fallback and soft interactions
}

# Current mode status
status_file = "./core/mode_status.json"

def switch_mode(mode):
    if mode not in MODELS:
        print(f"[ERROR] Invalid mode: {mode}")
        return

    model_name = MODELS[mode]

    try:
        print(f"[INFO] Switching Kisha to '{mode.upper()}' mode using model '{model_name}'")
        subprocess.run(["ollama", "run", model_name], check=True)

        with open(status_file, 'w') as f:
            json.dump({"current_mode": mode}, f)

        print(f"[SUCCESS] Kisha is now in {mode.upper()} mode")
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] Failed to switch mode: {e}")


def get_current_mode():
    try:
        with open(status_file, 'r') as f:
            data = json.load(f)
            return data.get("current_mode", "vortex")
    except FileNotFoundError:
        return "vortex"


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python kisha_mode_switcher.py [vortex|zen]")
    else:
        switch_mode(sys.argv[1])
