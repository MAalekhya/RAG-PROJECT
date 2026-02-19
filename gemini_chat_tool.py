"""Small helper module demonstrating a Gemini-style function-calling tool.

This file implements a local tool `get_current_datetime()` which returns the
current UTC timestamp in ISO8601 format, plus a tiny helper to detect when a
model response requests calling that tool (via the token
`CALL_TOOL:get_datetime`) and to run the tool and produce a follow-up.

Usage:
  # Simulate the model asking to call the tool
  python gemini_chat_tool.py --simulate "CALL_TOOL:get_datetime"

  # Simulate a model that does not call the tool
  python gemini_chat_tool.py --simulate "Hello, how are you?"

This is intentionally standalone and does not call any external API.
"""
from __future__ import annotations

from datetime import datetime
import argparse
import json
from typing import Optional, Dict, Any

try:
    import google.generativeai as genai
except Exception:
    genai = None


def get_current_datetime() -> str:
    """Return current UTC datetime in ISO8601 format including microseconds.

    This represents a function-like tool the model can request.
    """
    return datetime.utcnow().isoformat(timespec="microseconds") + "Z"


def detect_and_call_tool(model_text: str) -> Optional[str]:
    """Detect a structured tool call or token in `model_text` and run the tool.

    This looks for either:
    - A JSON-like tool_call object embedded in the text, e.g.:
      {"tool_call": {"name": "get_current_datetime", "arguments": {}}}
    - The token `CALL_TOOL:get_datetime` (case-insensitive)

    If a supported tool call is found, the corresponding local tool is executed
    and its string output is returned. Otherwise returns `None`.
    """
    # Try to find a JSON tool_call in the text
    try:
        # find the first JSON object in the text
        start = model_text.find("{")
        if start != -1:
            obj = json.loads(model_text[start:])
            tc = obj.get("tool_call") if isinstance(obj, dict) else None
            if tc and tc.get("name") == "get_current_datetime":
                return get_current_datetime()
    except Exception:
        pass

    # Fallback: token detection
    if "call_tool:get_datetime" in model_text.lower() or "CALL_TOOL:get_datetime" in model_text:
        return get_current_datetime()

    return None


TOOL_SCHEMA = [
    {
        "name": "get_current_datetime",
        "description": "Returns the current UTC date and time in ISO8601 format.",
        "parameters": {},
    }
]


def call_model_with_tools(api_key: Optional[str], model: str, user_prompt: str, use_real: bool = False) -> str:
    """Call Gemini (or simulate) with a structured tool schema and function-calling flow.

    If `use_real` is True and the `google.generativeai` client is installed, this
    attempts to call the real client. Regardless, the function will detect a
    tool call in the model output, execute the local tool, and then provide the
    tool output back to the model to obtain a final assistant response.
    """
    system_msg = (
        "You have the following tools available:\n" + json.dumps(TOOL_SCHEMA, indent=2)
    )

    # If real client available and requested, try to use it. This branch is
    # best-effort — concrete client signatures vary by release.
    if use_real and genai is not None and api_key:
        try:
            genai.configure(api_key=api_key)
            model_client = genai.GenerativeModel(model)
            prompt = f"System: {system_msg}\nUser: {user_prompt}"
            resp = model_client.generate_content(prompt)
            resp_text = getattr(resp, "text", str(resp)).strip()

            tool_output = detect_and_call_tool(resp_text)
            if tool_output is None:
                return resp_text

            # Send tool result back as a follow-up
            followup = (
                f"Tool get_current_datetime returned:\n{tool_output}\n"
                "Please produce the final assistant response incorporating this tool output."
            )
            resp2 = model_client.generate_content(f"System: {system_msg}\nUser: {user_prompt}\n{followup}")
            return getattr(resp2, "text", str(resp2)).strip()
        except Exception:
            # Fall through to simulated flow on error
            pass

    # Simulated model behavior: either the caller provides a simulated model
    # response via special tokens or we heuristically decide the model would
    # request the tool when the user asks for the current time.
    # Heuristic: if user explicitly asks for current time, simulate tool_call.
    if any(k in user_prompt.lower() for k in ("current time", "date and time", "what time")):
        # Simulate model deciding to call the tool using structured tool_call JSON
        simulated_model_response = json.dumps({"tool_call": {"name": "get_current_datetime", "arguments": {}}})
    else:
        # Simulate a normal assistant response
        simulated_model_response = "I'm not requesting any tools for that question."

    tool_output = detect_and_call_tool(simulated_model_response)
    if tool_output is None:
        return simulated_model_response

    # Create follow-up prompt with tool result and simulate final model reply
    followup_prompt = (
        f"Tool get_current_datetime returned:\n{tool_output}\n"
        "Please produce the final assistant response incorporating this tool output."
    )

    # Simulated final assistant reply
    final_reply = f"The current UTC date and time is {tool_output}."
    return final_reply


def demo_function_call_flow(simulated_model_text: str) -> str:
    """Demo: given an initial model response, run the tool if requested and
    produce a follow-up message that would be sent back to the model.

    Returns a JSON-like string showing the steps and results.
    """
    initial = {
        "stage": "initial_model_response",
        "model_text": simulated_model_text,
    }

    tool_result = detect_and_call_tool(simulated_model_text)

    if tool_result is None:
        final = {
            "stage": "no_tool_call",
            "final_text": simulated_model_text,
        }
        return json.dumps({"initial": initial, "final": final}, indent=2)

    # Construct follow-up that would be sent to the model containing tool output
    followup_prompt = (
        f"Tool get_current_datetime returned:\n{tool_result}\n"
        "Please produce the final assistant response incorporating this tool output."
    )

    final = {
        "stage": "tool_called",
        "tool_name": "get_current_datetime",
        "tool_output": tool_result,
        "followup_prompt": followup_prompt,
    }
    return json.dumps({"initial": initial, "final": final}, indent=2)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Demo Gemini function-calling tool for datetime")
    parser.add_argument("--simulate", help="Simulated model response to inspect and act on", required=True)
    args = parser.parse_args()

    out = demo_function_call_flow(args.simulate)
    print(out)


if __name__ == "__main__":
    _cli()
