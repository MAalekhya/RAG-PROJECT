import argparse
import threading
import time
import os
import sys
# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from core.message_handler import parse_message, create_message, dump_message

try:
    import google.generativeai as genai
except ImportError:
    print("Error: google-generativeai not installed")
    print("Install with: pip install google-generativeai")
    sys.exit(1)


def monitor_history_file(history_file: str, stop_event: threading.Event, on_message_received, poll_interval: float = 0.5):
    """Monitor history file for new messages and invoke callback for each."""
    with open(history_file, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)
        while not stop_event.is_set():
            line = f.readline()
            if not line:
                time.sleep(poll_interval)
                continue
            try:
                msg = parse_message(line)
            except Exception:
                continue
            on_message_received(msg)


def main():
    parser = argparse.ArgumentParser(description="Gemini AI bot for local file-backed chat")
    parser.add_argument("--nick", default="gemini-bot")
    parser.add_argument("--history-file", default="history.jsonl")
    parser.add_argument("--poll-interval", type=float, default=0.5)
    parser.add_argument("--api-key", required=True, help="Google Gemini API key (get from https://aistudio.google.com/app/apikeys)")
    args = parser.parse_args()

    bot_nick = args.nick
    history_file = args.history_file

    # Configure Gemini API
    try:
        genai.configure(api_key=args.api_key)
        model = genai.GenerativeModel("gemini-3-flash-preview")
        print(f"[{bot_nick}] Successfully connected to Gemini AI")
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        sys.exit(1)

    stop_event = threading.Event()

    def on_message_received(msg):
        """Gemini bot: respond to all non-command messages with AI-generated responses."""
        # Don't respond to own messages (prevent infinite loops)
        if msg.get("nick") == bot_nick:
            return
        # Only process chat messages (ignore join/leave)
        if msg.get("type") != "message":
            return
        
        message_text = msg.get("text", "").strip()
        if not message_text:
            return
        
        # Skip command messages (starting with !)
        if message_text.startswith("!"):
            return
        
        try:
            # Call Gemini API to generate response
            response = model.generate_content(message_text)
            ai_response = response.text.strip()
            
            # Send response back to history
            resp = create_message("message", bot_nick, ai_response)
            with open(history_file, "a", encoding="utf-8") as f:
                f.write(dump_message(resp) + "\n")
                f.flush()
            print(f"[{bot_nick}] Responded to '{message_text[:50]}...'")
        except Exception as e:
            # Log error silently to avoid crashing the bot
            print(f"[{bot_nick}] Error generating response: {e}")
            pass

    monitor_thread = threading.Thread(
        target=monitor_history_file,
        args=(history_file, stop_event, on_message_received, args.poll_interval),
        daemon=True
    )
    monitor_thread.start()

    print(f"[{bot_nick}] Started monitoring {history_file}")
    print(f"[{bot_nick}] Type messages in chat, and I'll respond with AI!")
    print(f"[{bot_nick}] Press Ctrl+C to stop")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[{bot_nick}] Shutting down...")
        stop_event.set()


if __name__ == "__main__":
    main()
