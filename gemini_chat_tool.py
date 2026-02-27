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
    # Ensure the terminal can handle all characters on Windows
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    DIVIDER = "=" * 60
    STEP    = ">>>"   # step marker (plain ASCII, works on all terminals)
    OK      = "[OK]"
    TOOL    = "[TOOL CALL]"
    TEXT    = "[TEXT]"

    print(f"\n{DIVIDER}")
    print("  GEMINI FUNCTION-CALLING WORKFLOW  ")
    print(f"{DIVIDER}\n")

    # ── STEP 1: Load API Key ─────────────────────────────────────────
    print(f"{STEP} STEP 1: Load API Key")
    print("   Reading GOOGLE_API_KEY from your .env file...")
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("chatkey1")
    if not api_key:
        raise SystemExit(
            "ERROR: No API key found.\n"
            "Set GOOGLE_API_KEY in your .env file or as an environment variable."
        )
    print(f"   {OK} API key loaded successfully.\n")

    # ── STEP 2: Register the Tool ────────────────────────────────────
    print(f"{STEP} STEP 2: Register Local Tool")
    print("   We define a Python function `get_current_datetime()`")
    print("   and pass it to the SDK. Gemini will receive a description")
    print("   of what this tool does and can choose to call it.")
    tools = [get_current_datetime]
    print(f"   {OK} Tool registered: get_current_datetime\n")

    # ── STEP 3: Send User Prompt to Gemini (1st API Call) ────────────
    print(f"{STEP} STEP 3: Send User Prompt -> Gemini (1st API Call)")
    print(f"   User prompt: \"{user_prompt}\"")
    print("   Gemini will read the prompt AND the tool description.")
    print("   It will decide: 'Do I need to call a tool, or can I answer directly?'")
    print("   Sending request to Gemini API...")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            tools=tools,
            # Disable auto-calling so WE stay in control of all function calls.
            # Without this, the model's built-in tools (e.g. google_search) can
            # trigger a KeyError because the SDK can't find them in our function map.
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    print(f"   {OK} Got response from Gemini.\n")

    # ── STEP 4: Inspect Gemini's Response ───────────────────────────
    print(f"{STEP} STEP 4: Inspect Gemini's Response")
    print("   Gemini can return two kinds of response parts:")
    print("     (a) A plain text answer   -> no tool needed")
    print("     (b) A function_call part  -> Gemini wants us to run a tool")
    print("   Checking response parts now...\n")

    for part in response.candidates[0].content.parts:
        if part.function_call:
            fn = part.function_call
            print(f"   {TOOL} Gemini returned a FUNCTION CALL: {fn.name}()")
            print(f"      Arguments Gemini sent: {dict(fn.args)}")
            print("      -> This means Gemini does NOT know the current time by itself.")
            print("         It's asking US (our Python code) to run the tool and report back.\n")

            # ── STEP 5: Execute the Tool Locally ────────────────────
            print(f"{STEP} STEP 5: Execute the Tool Locally (on our machine)")
            print("   Running get_current_datetime() in Python...")
            tool_result = get_current_datetime()
            print(f"   {OK} Tool returned: {tool_result}\n")

            # ── STEP 6: Package Tool Result ──────────────────────────
            print(f"{STEP} STEP 6: Package the Tool Result")
            print("   We wrap the result in a `function_response` part.")
            print("   This tells Gemini: 'Here is what your requested tool returned.'")
            tool_response_part = types.Part.from_function_response(
                name=fn.name,
                response={"result": tool_result},
            )
            print(f"   {OK} Packaged result: {{\"result\": \"{tool_result}\"}}\n")

            # ── STEP 7: Send Tool Result Back -> Gemini (2nd API Call)
            print(f"{STEP} STEP 7: Send Tool Result -> Gemini (2nd API Call)")
            print("   We replay the full conversation so far:")
            print("     [1] Original user message")
            print("     [2] Gemini's function_call turn (what it asked for)")
            print("     [3] Our function_response (what the tool returned)")
            print("   Gemini will now compose a final, grounded answer...")

            follow_up = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
                    response.candidates[0].content,       # Gemini's tool-call turn
                    types.Content(role="user", parts=[tool_response_part]),
                ],
                config=types.GenerateContentConfig(
                    tools=tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                ),
            )
            print(f"   {OK} Got final response from Gemini.\n")

            # ── STEP 8: Final Answer ─────────────────────────────────
            print(f"{STEP} STEP 8: Final Answer")
            print(DIVIDER)
            print(f"Gemini: {follow_up.text}")
            print(f"{DIVIDER}\n")

        elif not part.function_call:
            # ── No Tool Needed Path ──────────────────────────────────
            print(f"   {TEXT} Gemini returned a PLAIN TEXT answer.")
            print("      -> The question did not require any tool call.\n")
            print(f"{STEP} STEP 5: Final Answer (no tool was needed)")
            print(DIVIDER)
            print(f"Gemini: {response.text}")
            print(f"{DIVIDER}\n")
            return


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
