# CLI File-Backed Chat (Prototype)

This is a minimal **local-only** command-line chat prototype intended as the starting point for building a ChatGPT-like app later.

Key points:
- No network required — clients communicate by appending/reading a local `history.jsonl` file (one JSON message per line).
- Minimal dependencies; runs on Python 3.10+.
- Includes a simple `echo-bot` example that responds to messages starting with `!echo `.

Usage (basic):
1. Open two terminals and run: `python client.py --nick Alice` and `python client.py --nick Bob`.
2. Type messages and press Enter; messages appear in each terminal as they are appended to `history.jsonl`.
3. Use `/quit` or Ctrl+C to exit.

Notes & next steps:
- This file-backed approach is a simple prototype and not suitable for production or multi-host setups.
- The project includes `message_handler.py` and a `bots/` directory with a sample bot; later we will replace the storage with a proper transport (Redis, sockets, or WebSockets) and add AI integration hooks.
