# Gemini AI Integration - Quick Start

## What's Been Added

✅ **src/bots/gemini_bot.py** — Full Gemini AI bot implementation
✅ **run_gemini_bot.py** — Entry point to launch the bot
✅ **requirements.txt** — Updated with `google-generativeai`
✅ **docs/GEMINI_SETUP.md** — Complete setup and troubleshooting guide

## 3-Step Setup

### Step 1: Get API Key
Visit [Google AI Studio](https://aistudio.google.com/app/apikeys) and create a free API key.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run (3 Terminals)

**Terminal 1 - Chat User 1:**
```bash
python chat.py --nick Alice
```

**Terminal 2 - Chat User 2:**
```bash
python chat.py --nick Bob
```

**Terminal 3 - Gemini Bot:**
```bash
python run_gemini_bot.py --nick gemini-bot --api-key YOUR_API_KEY
```

Now type messages and Gemini AI will respond!

## Example

```
Alice> What is machine learning?
[timestamp] gemini-bot: Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed...

Bob> Tell me a poem about AI
[timestamp] gemini-bot: In circuits deep and data vast,
Intelligence learns from the past...
```

## Features

- ✓ Real-time AI responses to chat messages
- ✓ Prevents infinite loops (ignores own messages)
- ✓ Command filtering (ignores !echo, etc.)
- ✓ Error handling
- ✓ Customizable polling interval
- ✓ Free tier available

## Files

| File | Purpose |
|------|---------|
| `src/bots/gemini_bot.py` | Bot implementation |
| `run_gemini_bot.py` | Launch entry point |
| `docs/GEMINI_SETUP.md` | Full setup guide |
| `requirements.txt` | Dependencies (updated) |

## Troubleshooting

**"google-generativeai not installed"**
```bash
pip install google-generativeai
```

**"Invalid API Key"**
- Double-check your key from Google AI Studio
- Ensure no trailing spaces

**Bot not responding**
- Verify `history.jsonl` exists and has messages
- Check bot terminal output for errors
- Try reducing `--poll-interval 0.3`

## Next Steps

Read [docs/GEMINI_SETUP.md](GEMINI_SETUP.md) for:
- Environment variable setup
- Rate limit handling
- Advanced customization
- Security best practices
