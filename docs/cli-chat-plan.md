# CLI Chat App — Implementation Plan 🔧

**TL;DR:** Build a Python 3.10+ command-line chat using `asyncio` TCP streams as a simple chat interface and foundation for a future AI-based chat. Design modular hooks (a `message_handler` and `bots` adapters), persist minimal message history for context, and keep the CLI interface simple for now.

---

## Steps ✅
1. Implement `handle_client` and `broadcast` in `server.py`.
2. Create `client.py` with `connect_and_run` and async stdin handling (use `loop.run_in_executor()` on Windows; `aioconsole` optional).
3. Add `message_handler.py` to validate and process messages and define protocol: JSON-per-line with fields `type`, `nick`, `text`, `ts`, `id`, `source`.
4. Add CLI flags: `--host`, `--port`, `--nick`, `--retries`, `--history-file`, `--bot` and include usage in `README.md`.
5. Create `bots/` with a simple `echo_bot.py` and a `bot_adapter` interface for future AI integration; add tests under `tests/`.

---

## Further Considerations ⚠️
- Concurrency: Use `asyncio` tasks; on Windows read stdin via `loop.run_in_executor()` (or `aioconsole`).
- History & context: persist messages to `history.jsonl` (one JSON per line) to allow later AI context or replay. 
- Bot hooks: design message pipeline so `bots.bot_adapter` can subscribe or intercept messages for automated replies.
- Security/privacy: consider opt-in history and data retention before integrating external AI APIs.

---

## Minimal file layout 📁
- `server.py` — `handle_client`, `broadcast`, server entry point
- `client.py` — `connect_and_run`, stdin handling, reconnection
- `message_handler.py` — message validation and middleware hooks
- `bots/` — `echo_bot.py`, `bot_adapter.py` (adapter interface)
- `history.jsonl` — optional message history storage
- `README.md` — run, test, and AI-extension notes
- `cli-chat-plan.md` — this plan
- `tests/` — unit tests for protocol, bots, and reconnection

---

If you want, I can scaffold the project files now (`server.py`, `client.py`, `message_handler.py`, an `echo_bot`, `requirements.txt`, `README.md`) and include a minimal working example and tests. Would you like me to create that scaffold next?