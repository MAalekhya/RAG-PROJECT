"""Gemini Chat with Native Function Calling — get_current_datetime tool.

Uses the NEW `google-genai` SDK (google.genai) which has proper, stable
function-calling support.

Usage:
    python gemini_chat.py
"""
from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Environment setup
# ---------------------------------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("chatkey1")
if not API_KEY:
    raise EnvironmentError(
        "No Gemini API key found. Set GOOGLE_API_KEY in your .env file."
    )

client = genai.Client(api_key=API_KEY)

# ---------------------------------------------------------------------------
# Model name
# ---------------------------------------------------------------------------
MODEL_NAME = "gemini-3-flash-preview"

# ---------------------------------------------------------------------------
# Tool implementation  (local Python function)
# ---------------------------------------------------------------------------

def get_current_datetime() -> dict:
    """Return the current local datetime as a structured dict."""
    now = datetime.now()
    return {
        "date":        now.strftime("%Y-%m-%d"),
        "time":        now.strftime("%H:%M:%S"),
        "datetime":    now.strftime("%Y-%m-%d %H:%M:%S"),
        "day_of_week": now.strftime("%A"),
        "timezone":    "local",
    }


# Map tool names → callables so we can dispatch by name
TOOL_REGISTRY: dict[str, callable] = {
    "get_current_datetime": get_current_datetime,
}

# ---------------------------------------------------------------------------
# Tool schema  (tells Gemini what tools it can call)
# ---------------------------------------------------------------------------
TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_current_datetime",
                description=(
                    "Returns the current local date and time. "
                    "Call this whenever the user asks about the current "
                    "time, date, day of the week, or datetime."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={},   # no input parameters needed
                ),
            )
        ]
    )
]

# ---------------------------------------------------------------------------
# Generation config
# ---------------------------------------------------------------------------
CONFIG = types.GenerateContentConfig(
    system_instruction=(
        "You are a helpful assistant. When the user asks about the current "
        "date or time, always use the get_current_datetime tool to fetch "
        "accurate real-time information rather than guessing."
    ),
    tools=TOOLS,
)

# ---------------------------------------------------------------------------
# Function calling helpers
# ---------------------------------------------------------------------------

def handle_function_calls(response) -> list[types.Part]:
    """Inspect the model response, execute any requested tools, return result parts."""
    result_parts: list[types.Part] = []

    # Gemini API → Agent: inspect each part of the model's response for tool call requests
    print("\n" + "-" * 50)
    print("[STEP 2] Gemini API → Agent")
    print("         Gemini has replied. Agent is now checking")
    print("         if Gemini wants to call a tool...")

    for part in response.candidates[0].content.parts:
        # Agent decides: does this part contain a tool call request from Gemini?
        if not part.function_call:
            continue

        fn_name = part.function_call.name
        fn_args = dict(part.function_call.args) if part.function_call.args else {}

        # Gemini API → Agent: model has decided to call a tool; agent reads the request
        print(f"\n[STEP 3] Gemini API → Agent (Tool Request)")
        print(f"         Gemini says: 'Please call the tool: {fn_name}'")
        print(f"         Arguments Gemini passed: {fn_args}")

        # Agent → Tool: agent dispatches the tool call locally
        print(f"\n[STEP 4] Agent → Tool")
        print(f"         Agent is now running the local function: {fn_name}()")

        if fn_name in TOOL_REGISTRY:
            output = TOOL_REGISTRY[fn_name](**fn_args)   # Agent → Tool: execute tool
            # Tool → Agent: tool returns result
            print(f"\n[STEP 5] Tool → Agent")
            print(f"         Tool '{fn_name}' finished and returned the result:")
            print(f"         {output}")
        else:
            output = {"error": f"Unknown tool: {fn_name}"}
            print(f"\n[STEP 5] Tool → Agent (ERROR)")
            print(f"         Tool '{fn_name}' not found! Error: {output}")

        # Agent → Gemini API: wrap the tool result and send it back to the model
        print(f"\n[STEP 6] Agent → Gemini API (Tool Result)")
        print(f"         Agent is sending the tool result back to Gemini...")

        result_parts.append(
            types.Part.from_function_response(
                name=fn_name,
                response={"result": output},
            )
        )

    return result_parts


def chat_turn(chat, user_input: str) -> str:
    """Send a user message, handle any tool calls, and return the final reply."""

    # User → Agent → Gemini API: agent forwards the user message to the model
    print("\n" + "=" * 50)
    print("[STEP 1] User → Agent → Gemini API")
    print(f"         User said: '{user_input}'")
    print("         Agent is sending this message to Gemini API...")
    response = chat.send_message(user_input)

    # Agentic loop: keep handling tool calls until the model produces text
    while True:
        # Agent decides: did Gemini request a tool call in its response?
        tool_result_parts = handle_function_calls(response)

        if not tool_result_parts:  # Agent decides: no tool call → Gemini produced final text
            print("\n[STEP 2b] Agent decides: No tool call needed.")
            print("          Gemini produced a direct text response. Done!")
            print("-" * 50)
            break

        # Agent → Gemini API: send tool results back so Gemini can form its final reply
        print("\n[STEP 7] Agent → Gemini API (Final Request)")
        print("         Agent is sending the tool result back to Gemini.")
        print("         Asking Gemini to now form its final answer using the tool result...")
        response = chat.send_message(tool_result_parts)

        print("\n[STEP 8] Gemini API → Agent (Final Response)")
        print("         Gemini has used the tool result to form its final reply.")
        print("-" * 50)

    # Gemini API → Agent → User: return the model's final text response
    print("\n[STEP 9] Gemini API → Agent → User")
    print("         Agent is returning Gemini's final answer to the user.")
    print("=" * 50)
    return response.text.strip()


# ---------------------------------------------------------------------------
# Interactive chat loop
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Gemini Chat with Function Calling  (google-genai SDK)")
    print(f"  Model : {MODEL_NAME}")
    print("  Tool  : get_current_datetime")
    print("  Type  'quit' or 'exit' to stop.")
    print("=" * 60)
    print()

    # Create a persistent chat session (maintains conversation history)
    chat = client.chats.create(model=MODEL_NAME, config=CONFIG)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Goodbye!")
            break

        try:
            reply = chat_turn(chat, user_input)
            print(f"\nGemini: {reply}\n")
        except Exception as exc:
            print(f"\n[error] {exc}\n")


if __name__ == "__main__":
    main()
