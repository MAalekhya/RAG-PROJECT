"""Core Gemini service for handling API interactions and tool calls.
Extracted logic to follow DRY principles.
"""
from __future__ import annotations
import os
from datetime import datetime, timezone
from typing import List, Optional, Any
from google import genai
from google.genai import types

# Load .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY") or os.environ.get("chatkey1")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-3-flash-preview"
        self.tools = [self.get_current_datetime]

    @staticmethod
    def get_current_datetime() -> str:
        """Return the current UTC date and time in ISO 8601 format."""
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    def chat(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and handle potential tool calls.
        Returns the final grounded response string.
        """
        # STEP 1: Initial call to Gemini
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=self.tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            ),
        )

        candidate = response.candidates[0]
        
        # STEP 2: Check for tool calls
        for part in candidate.content.parts:
            if part.function_call:
                fn = part.function_call
                
                # Execute tool locally (only get_current_datetime supported for now)
                if fn.name == "get_current_datetime":
                    result = self.get_current_datetime()
                else:
                    result = f"Error: Tool {fn.name} not implemented"

                # Package tool result
                tool_response_part = types.Part.from_function_response(
                    name=fn.name,
                    response={"result": result},
                )

                # STEP 3: Final call with tool result
                follow_up = self.client.models.generate_content(
                    model=self.model_id,
                    contents=[
                        types.Content(role="user", parts=[types.Part(text=prompt)]),
                        candidate.content, # What Gemini asked for
                        types.Content(role="user", parts=[tool_response_part]),
                    ],
                    config=types.GenerateContentConfig(
                        tools=self.tools,
                        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                    ),
                )
                return follow_up.text or "Error: Gemini returned an empty response after the tool call."

        # If no tool was needed
        return response.text or "Error: Gemini returned an empty response."

