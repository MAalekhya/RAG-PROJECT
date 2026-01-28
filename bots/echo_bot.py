import argparse
import threading
import time
import os
from message_handler import parse_message, create_message, dump_message


def tail_history(history_file: str, stop_event: threading.Event, on_message, poll: float = 0.5):
    with open(history_file, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)
        while not stop_event.is_set():
            line = f.readline()
            if not line:
                time.sleep(poll)
                continue
            try:
                msg = parse_message(line)
            except Exception:
                continue
            on_message(msg)


def main():
    parser = argparse.ArgumentParser(description="Simple echo bot for local file-backed chat")
    parser.add_argument("--nick", default="echo-bot")
    parser.add_argument("--history-file", default="history.jsonl")
    parser.add_argument("--poll-interval", type=float, default=0.5)
    args = parser.parse_args()

    nick = args.nick
    history_file = args.history_file

    stop_event = threading.Event()

    def on_message(msg):
        # Don't respond to own messages
        if msg.get("nick") == nick:
            return
        if msg.get("type") != "message":
            return
        text = msg.get("text", "")
        if text.startswith("!echo "):
            payload = text[len("!echo "):]
            resp = create_message("message", nick, "Echo: " + payload)
            with open(history_file, "a", encoding="utf-8") as f:
                f.write(dump_message(resp) + "\n")
                f.flush()

    t = threading.Thread(target=tail_history, args=(history_file, stop_event, on_message, args.poll_interval), daemon=True)
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        t.join(timeout=1)


if __name__ == "__main__":
    main()
