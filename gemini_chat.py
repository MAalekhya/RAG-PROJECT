#!/usr/bin/env python3
"""Simple Gemini chat CLI.

Usage:
  - Set environment variable `GOOGLE_API_KEY` with your API key.
  - Run: python gemini_chat.py --prompt "Hello" or
    python gemini_chat.py --interactive

This script tries to use the Generative Language REST endpoint directly
so it can run without additional Google client libraries.
"""
from __future__ import annotations

import argparse
import os
import sys
import json
from typing import Optional

try:
    import requests
except Exception:
    requests = None

try:
    import google.generativeai as genai
except Exception:
    genai = None


DEFAULT_MODEL = "gemini-3-flash-preview"


def get_api_key(cmd_key: Optional[str]) -> Optional[str]:
    if cmd_key:
        return cmd_key
    return os.environ.get("GOOGLE_API_KEY")


def call_gemini(api_key: str, model: str, prompt: str, temperature: float = 0.2, max_output_tokens: int = 512) -> str:
    """Call Gemini. Prefer the `google.generativeai` client (same as `gemini_bot`).

    If the client lib is available, use it with the same call pattern as
    `src/bots/gemini_bot.py`. Otherwise, provide a clear error explaining
    that the preferred client is missing.
    """
    if genai is not None:
        try:
            genai.configure(api_key=api_key)
            model_client = genai.GenerativeModel(model)
            # Use same call used in the bot
            resp = model_client.generate_content(prompt)
            # Response object exposes `.text` like in the bot
            return getattr(resp, "text", str(resp)).strip()
        except Exception as e:
            raise RuntimeError(f"Gemini client error: {e}")

    # If we reach here, `google.generativeai` is not installed.
    raise RuntimeError(
        "google-generativeai client not installed. Install with: pip install google-generativeai"
        "\n(Alternatively install 'requests' and implement a REST payload matching the Generative Language API.)"
    )
    


def interactive_loop(api_key: str, model: str) -> None:
    print(f"Gemini chat (model={model}). Type /quit to exit.")
    while True:
        try:
            prompt = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return

        if not prompt:
            continue
        if prompt.strip() in ("/quit", "/exit"):
            print("Bye.")
            return

        try:
            out = call_gemini(api_key, model, prompt)
            print("Gemini:", out)
        except Exception as e:
            print("Error:", e)


def main():
    parser = argparse.ArgumentParser(description="Simple Gemini chat client")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name (default: %(default)s)")
    parser.add_argument("--key", help="API key (overrides GOOGLE_API_KEY env var)")
    parser.add_argument("--prompt", help="Single-shot prompt to send")
    parser.add_argument("--interactive", action="store_true", help="Run interactive chat loop")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=512)

    args = parser.parse_args()

    api_key = get_api_key(args.key)
    print("API Key:", api_key)
    if not api_key:
        print("ERROR: No API key provided. Set GOOGLE_API_KEY or pass --key.")
        sys.exit(2)

    if args.interactive:
        interactive_loop(api_key, args.model)
        return

    if args.prompt:
        try:
            out = call_gemini(api_key, args.model, args.prompt, temperature=args.temperature, max_output_tokens=args.max_tokens)
            print(out)
        except Exception as e:
            print("Error:", e)
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
