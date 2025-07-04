#!/usr/bin/env python3

import sys
import os
import subprocess
import argparse
import logging

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from core import Kisha_brain

# Logging
logging.basicConfig(filename="kisha.log", level=logging.INFO)

def health_check():
    try:
        subprocess.run(["ollama", "list"], capture_output=True, check=True)
        print("✅ Ollama daemon reachable.")
    except Exception as e:
        print(f"🚨 Ollama not reachable: {e}")
        sys.exit(1)

def main_chat():
    print("🧠 Booting up Kisha’s local brain (chat mode)...")
    print("Type 'quit' or 'exit' to shut her down gracefully.\n")

    while True:
        try:
            user_input = input("You > ")
            if user_input.strip().lower() in ["quit", "exit"]:
                print("\n🧠 Kisha signing off. Stay sharp, genius.")
                break

            reply = Kisha_brain.kisha_response(user_input)
            print(f"Kisha > {reply}\n")

        except KeyboardInterrupt:
            print("\n\n🧠 Kisha interrupted. Bye!")
            break
        except Exception as e:
            logging.exception("💥 Unexpected error in chat loop.")
            print(f"💥 Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["chat", "voice", "api"], default="chat")
    args = parser.parse_args()

    health_check()

    if args.mode == "chat":
        main_chat()
    elif args.mode == "voice":
        print("🔊 Voice test mode not yet implemented.")
    elif args.mode == "api":
        print("🌐 API server launch not yet implemented.")
