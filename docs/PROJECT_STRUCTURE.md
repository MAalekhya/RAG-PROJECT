# Project Structure

## Directory Organization

This project uses a clean, modular directory structure optimized for extensibility and AI integration.

```
rag-project/
├── src/                          # Main source code
│   ├── __init__.py
│   ├── core/                     # Core chat engine
│   │   ├── __init__.py
│   │   ├── message_handler.py    # Message creation, parsing, validation
│   │   └── chat_user_client.py   # Interactive user client
│   └── bots/                     # AI bot implementations
│       ├── __init__.py
│       ├── echo_bot.py           # Example: echo bot
│       └── gemini_bot.py         # (Future) Gemini AI bot
│
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_message_handler.py   # Message handler tests
│
├── examples/                     # Usage examples
│   ├── __init__.py
│   ├── simple_input.py          # Basic input example
│   └── simple_open.py           # Basic open file example
│
├── docs/                        # Documentation
│   ├── README.md               # Project overview
│   ├── app_understanding.md    # Architecture explanation
│   ├── cli-chat-plan.md        # Development plan
│   ├── prompt_library.md       # Prompt templates
│   └── REFACTORING_SUMMARY.md  # Refactoring details
│
├── archive/                    # Temporary/deprecated files
│   ├── Demo.py
│   ├── client.py              # (old) Original client.py
│   └── ... (other demos)
│
├── .github/                    # GitHub configuration
│   └── copilot-instructions.md # AI agent guidelines
│
├── .gitignore
├── requirements.txt            # Python dependencies
│
├── chat.py                    # Main entry point - runs interactive chat client
├── run_echo_bot.py            # Entry point - runs echo bot example
│
└── history.jsonl              # Runtime: Chat message history (newline-delimited JSON)
```

## Key Directories

### `src/core/`
Core chat engine components:
- **message_handler.py** — JSON message creation, parsing, validation, and serialization
- **chat_user_client.py** — Interactive CLI user client with background message monitoring

### `src/bots/`
AI bot implementations following the standard pattern:
- **echo_bot.py** — Example bot that responds to `!echo` commands
- **gemini_bot.py** — (Future) Google Gemini AI bot integration
- **openai_bot.py** — (Future) OpenAI GPT bot integration

Each bot must implement:
```python
def monitor_history_file(history_file, stop_event, on_message_received, poll_interval)
def main()  # CLI entry point
def on_message_received(msg)  # Message callback
```

### `tests/`
Test suite using pytest:
- **test_message_handler.py** — Message creation/parsing roundtrip tests
- Additional tests go here as features are added

### `docs/`
Documentation:
- **README.md** — Project overview and quick start
- **app_understanding.md** — Architecture and design patterns
- **REFACTORING_SUMMARY.md** — Code refactoring changes
- **.github/copilot-instructions.md** — Guidelines for AI agents

### `archive/`
Temporary files and deprecated code:
- Old demo scripts
- Previous implementations (e.g., original `client.py`)
- Experimental code

## Entry Points

### Running Interactive Chat
```bash
python chat.py --nick Alice
```
Located at: `chat.py` → `src/core/chat_user_client.py`

### Running Echo Bot
```bash
python run_echo_bot.py --nick echo-bot
```
Located at: `run_echo_bot.py` → `src/bots/echo_bot.py`

### Running Tests
```bash
pytest tests/
```

## Import Patterns

### From Root Level Scripts
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from core.chat_user_client import main
from bots.echo_bot import main
```

### From Tests
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from core.message_handler import create_message, parse_message
```

### From Bots
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.message_handler import create_message, parse_message
```

## Adding New Components

### Adding a New AI Bot
1. Create `src/bots/my_bot.py`
2. Implement `monitor_history_file()` and `on_message_received()`
3. Create entry point: `run_my_bot.py` at root
4. Update documentation in `docs/`

### Adding Tests
1. Add test file to `tests/` (name: `test_*.py`)
2. Use pytest conventions
3. Update imports to reference `src/` modules

### Adding Documentation
1. Add markdown file to `docs/`
2. Reference in project overview or README

## Rationale

This structure provides:
- **Clear separation of concerns** — Core engine, bots, tests, docs
- **Easy extensibility** — Add new bots by following the pattern in `src/bots/`
- **AI-friendly** — Well-organized code helps AI agents understand patterns
- **Maintainability** — Temporary files isolated in `archive/`, clean main workspace
- **Standard layout** — Follows Python best practices (src/, tests/, docs/)
