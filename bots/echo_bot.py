import argparse
import threading
import time
import os
from message_handler import parse_message, create_message, dump_message


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
    parser = argparse.ArgumentParser(description="Echo bot for local file-backed chat")
    parser.add_argument("--nick", default="echo-bot")
    parser.add_argument("--history-file", default="history.jsonl")
    parser.add_argument("--poll-interval", type=float, default=0.5)
    args = parser.parse_args()

    bot_nick = args.nick
    history_file = args.history_file

    stop_event = threading.Event()

    def on_message_received(msg):
        """Echo bot: ignore own messages, filter for non-message types, respond to !echo commands."""
        # Don't respond to own messages (prevent infinite loops)
        if msg.get("nick") == bot_nick:
            return
        # Only process chat messages (ignore join/leave)
        if msg.get("type") != "message":
            return
        
        message_text = msg.get("text", "")
        if message_text.startswith("!echo "):
            payload = message_text[len("!echo "):]
            response = create_message("message", bot_nick, "Echo: " + payload)
            with open(history_file, "a", encoding="utf-8") as f:
                f.write(dump_message(response) + "\n")
                f.flush()

    monitor_thread = threading.Thread(
        target=monitor_history_file,
        args=(history_file, stop_event, on_message_received, args.poll_interval),
        daemon=True
    )
    monitor_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()


if __name__ == "__main__":
    main()
