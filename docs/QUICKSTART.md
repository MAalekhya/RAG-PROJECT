# Quick Start Guide

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Interactive Chat (Two Terminals)

**Terminal 1:**
```bash
python chat.py --nick Alice
```

**Terminal 2:**
```bash
python chat.py --nick Bob
```

Type messages and they will appear in both terminals!

### 3. Run Echo Bot (Optional, Third Terminal)
```bash
python run_echo_bot.py --nick echo-bot
```

Then in Alice's terminal, send:
```
!echo hello world
```

The echo bot will respond with: `Echo: hello world`

## Project Structure

```
src/core/           → Core chat engine
src/bots/           → AI bot implementations
tests/              → Test suite
examples/           → Usage examples
docs/               → Documentation
archive/            → Deprecated files
```

See [docs/PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for full details.

## Key Files

- **chat.py** — Run interactive chat client
- **run_echo_bot.py** — Run echo bot
- **src/core/message_handler.py** — Message format and utilities
- **src/core/chat_user_client.py** — User client implementation
- **src/bots/echo_bot.py** — Example bot (template for AI bots)

## Common Tasks

### Add a New Bot
1. Create `src/bots/my_bot.py` following the pattern in `echo_bot.py`
2. Create `run_my_bot.py` entry point at root
3. Run: `python run_my_bot.py --nick my-bot`

### Run Tests
```bash
pytest tests/ -v
```

### Create a Message
```python
from src.core.message_handler import create_message
msg = create_message("message", "Alice", "Hello!")
```

## Message Format

All messages are JSON with this schema:
```json
{
  "type": "message|join|leave",
  "nick": "username",
  "text": "message body",
  "ts": "2026-01-29T10:00:00.000000Z",
  "id": "uuid-string",
  "source": "local"
}
```

Messages are appended to `history.jsonl` (one per line, newline-delimited JSON).

## Next Steps

- Read [docs/app_understanding.md](app_understanding.md) for architecture details
- Check [.github/copilot-instructions.md](../.github/copilot-instructions.md) for AI integration guidelines
- Explore [examples/](examples/) for usage patterns
- Extend with AI by creating a new bot in `src/bots/`
