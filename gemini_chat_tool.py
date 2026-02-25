"""Gemini function-calling demo: get current date/time via a real tool call.

Uses the new `google.genai` SDK and the Gemini API to:
  1. Register `get_current_datetime` as a callable tool.
  2. Send a user prompt to Gemini.
  3. If Gemini decides to call the tool, execute it locally and return the
     result so Gemini can produce a final, grounded answer.

Usage:
  python gemini_chat_tool.py --prompt "What is the current date and time?"
  python gemini_chat_tool.py --prompt "Tell me a joke"

The API key is read from the GOOGLE_API_KEY environment variable (or .env).
"""
from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

# Load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env values must be set manually if dotenv is not installed

# ── New SDK ──────────────────────────────────────────────────────────────────
try:
    from google import genai
    from google.genai import types
except ImportError:
    raise SystemExit(
        "ERROR: google-genai is not installed.\n"
        "Run:  pip install google-genai"
    )


# ── Tool definition ───────────────────────────────────────────────────────────

def get_current_datetime() -> str:
    """Return the current UTC date and time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ── Main chat function ────────────────────────────────────────────────────────

def chat_with_tool(user_prompt: str) -> None:
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("chatkey1")
    if not api_key:
        raise SystemExit(
            "ERROR: No API key found.\n"
            "Set GOOGLE_API_KEY in your .env file or as an environment variable."
        )

    client = genai.Client(api_key=api_key)

    # Tell the SDK about our local tool
    tools = [get_current_datetime]

    print(f"\nUser: {user_prompt}\n")

    # First call – Gemini may respond normally or request a tool call
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_prompt,
        config=types.GenerateContentConfig(tools=tools),
    )


    # Walk through candidate parts to check for function calls
    for part in response.candidates[0].content.parts:
        if part.function_call:
            fn = part.function_call
            print(f"[Tool call requested] → {fn.name}()")

            if fn.name == "get_current_datetime":
                tool_result = get_current_datetime()
                print(f"[Tool result]         → {tool_result}\n")

                # Send tool result back so Gemini can form a final answer
                tool_response_part = types.Part.from_function_response(
                    name=fn.name,
                    response={"result": tool_result},
                )

                follow_up = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=[
                        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
                        response.candidates[0].content,          # model's tool-call turn
                        types.Content(role="user", parts=[tool_response_part]),
                    ],
                    config=types.GenerateContentConfig(tools=tools),
                )
                print(f"Gemini: {follow_up.text}")
            else:
                print(f"[Unknown tool requested: {fn.name}]")
            return

    # No tool call – just print the text response
    print(f"Gemini: {response.text}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="Chat with Gemini using real function calling for datetime"
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help='Your message to Gemini, e.g. "What is the current date and time?"',
    )
    args = parser.parse_args()
    chat_with_tool(args.prompt)


if __name__ == "__main__":
    _cli()
