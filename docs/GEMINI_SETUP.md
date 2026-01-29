# Gemini AI Integration Guide

## Setup Instructions

### 1. Get a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikeys)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Gemini Bot

```bash
python run_gemini_bot.py --nick gemini-bot --api-key YOUR_API_KEY_HERE
```

Replace `YOUR_API_KEY_HERE` with your actual API key.

## Full Usage Example

**Terminal 1 (User):**
```bash
python chat.py --nick Alice
```

**Terminal 2 (User):**
```bash
python chat.py --nick Bob
```

**Terminal 3 (Gemini Bot):**
```bash
python run_gemini_bot.py --nick gemini-bot --api-key sk-...
```

Now when Alice or Bob send messages, Gemini AI will respond!

## Example Conversation

```
Alice> What is the capital of France?
[timestamp] gemini-bot: The capital of France is Paris, the largest city in the country and the center of French culture, art, and politics.

Bob> Tell me a joke
[timestamp] gemini-bot: Why don't scientists trust atoms? Because they make up everything!
```

## Advanced Usage

### Custom Poll Interval (faster responses)
```bash
python run_gemini_bot.py --nick gemini-bot --api-key YOUR_KEY --poll-interval 0.3
```

### Custom History File
```bash
python run_gemini_bot.py --nick gemini-bot --api-key YOUR_KEY --history-file my_chat.jsonl
```

### Environment Variable (Optional)

Instead of passing the API key every time, set it as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
python run_gemini_bot.py --nick gemini-bot --api-key $env:GEMINI_API_KEY
```

**Windows (CMD):**
```cmd
set GEMINI_API_KEY=your-api-key-here
python run_gemini_bot.py --nick gemini-bot --api-key %GEMINI_API_KEY%
```

**macOS/Linux:**
```bash
export GEMINI_API_KEY="your-api-key-here"
python run_gemini_bot.py --nick gemini-bot --api-key $GEMINI_API_KEY
```

## Features

- **Real-time responses** — Gemini responds to every message in the chat
- **Error handling** — Gracefully handles API errors without crashing
- **Command filtering** — Ignores commands (messages starting with !)
- **Self-awareness** — Won't respond to its own messages (prevents loops)
- **Configurable** — Customize nick, polling interval, history file

## Troubleshooting

### "google-generativeai not installed"
```bash
pip install google-generativeai
```

### "Error: Invalid API Key"
- Verify your API key from [Google AI Studio](https://aistudio.google.com/app/apikeys)
- Make sure you copied the entire key without spaces

### Bot not responding
- Check if `history.jsonl` is being written by the chat clients
- Verify the bot is running (should print messages)
- Try reducing poll-interval: `--poll-interval 0.3`

### Rate limiting errors
- Google Gemini has rate limits
- Wait a few seconds and send another message
- Consider adding delays between bot responses

## API Pricing

Google Gemini offers a **free tier** with rate limits:
- 60 requests per minute
- For production use, check [Google AI pricing](https://ai.google.dev/pricing)

## Next Steps

- Explore [src/bots/gemini_bot.py](../../src/bots/gemini_bot.py) to customize bot behavior
- Add context/system prompts to guide AI responses
- Integrate with other services (logging, webhooks, etc.)
- Try other AI models as they become available

## Security Note

⚠️ **Never commit API keys to git!**

Use environment variables or `.env` files (add to `.gitignore`):
```python
import os
api_key = os.getenv("GEMINI_API_KEY")
```
