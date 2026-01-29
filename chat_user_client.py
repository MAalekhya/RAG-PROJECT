import argparse  # parse command-line arguments
import json  # read/write JSON strings
import threading  # run background tail thread
import time  # sleep for polling
import uuid  # generate unique IDs for messages
import datetime  # get timestamps
import os  # filesystem helpers
import sys  # system utilities (unused but common)
from message_handler import create_message, dump_message, parse_message  # helper functions for messages


def get_current_utc_timestamp():
    """Return current UTC timestamp in ISO8601 format with trailing Z."""
    return datetime.datetime.utcnow().isoformat() + "Z"


def append_message_to_history(history_file: str, message: dict):
    """Append a serialized JSON message to the history file atomically (newline-delimited)."""
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(dump_message(message) + "\n")
        f.flush()  # ensure it's written to disk immediately


def monitor_history_file(history_file: str, stop_event: threading.Event, on_message_received, poll_interval: float = 0.5):
    """
    Continuously monitor history_file for new lines and invoke on_message_received callback.
    
    Pattern: Seek to end on startup, poll periodically for new lines, parse JSON,
    skip malformed lines silently, invoke callback for each valid message.
    """
    with open(history_file, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)  # move to end to only see new lines
        while not stop_event.is_set():
            line = f.readline()
            if not line:  # no new line yet
                time.sleep(poll_interval)
                continue
            try:
                msg = parse_message(line)  # convert JSON line into dict
            except Exception:
                continue  # skip malformed lines silently
            on_message_received(msg)  # invoke handler with parsed message


def display_message_to_console(current_user_nick: str, message: dict):
    """Format and display a received message depending on its type (join/leave/message)."""
    timestamp = message.get("ts", "")
    sender_nick = message.get("nick", "")
    message_text = message.get("text", "")
    message_type = message.get("type", "message")
    
    if message_type == "join":
        print(f"[{timestamp}] -- {sender_nick} joined --")
    elif message_type == "leave":
        print(f"[{timestamp}] -- {sender_nick} left --")
    else:  # normal chat message
        print(f"[{timestamp}] {sender_nick}: {message_text}")


def run_interactive_chat_client(nick: str, history_file: str, poll_interval: float = 0.5):
    """
    Main entry point for interactive chat client.
    
    Responsibilities:
    - Ensure history file exists
    - Start background thread to monitor incoming messages
    - Send join announcement
    - Run interactive input loop to capture user messages
    - Handle quit commands and Ctrl+C gracefully
    - Send leave announcement on exit
    """
    # Ensure history file exists
    open(history_file, "a", encoding="utf-8").close()

    stop_event = threading.Event()

    def on_message_received(msg):
        """Callback: process and display each new message from history file."""
        try:
            display_message_to_console(nick, msg)
        except Exception:
            pass  # ignore errors in displaying

    # Start background thread to monitor history file
    monitor_thread = threading.Thread(
        target=monitor_history_file,
        args=(history_file, stop_event, on_message_received, poll_interval),
        daemon=True
    )
    monitor_thread.start()

    # Announce join
    join_message = create_message("join", nick, "")
    append_message_to_history(history_file, join_message)

    try:
        while True:
            try:
                user_input = input(f"{nick}> ")
            except EOFError:
                break

            message_text = user_input.strip()
            if not message_text:
                continue  # ignore empty input

            # Handle quit commands
            if message_text.lower() in ("/quit", "/exit"):
                leave_message = create_message("leave", nick, "")
                append_message_to_history(history_file, leave_message)
                break

            # Send regular chat message
            chat_message = create_message("message", nick, message_text)
            append_message_to_history(history_file, chat_message)

    except KeyboardInterrupt:
        # On Ctrl+C, send leave message
        leave_message = create_message("leave", nick, "")
        append_message_to_history(history_file, leave_message)

    finally:
        stop_event.set()  # signal monitor thread to stop
        monitor_thread.join(timeout=1)  # wait briefly for thread to exit


def main():
    """Parse CLI arguments and launch the interactive chat client."""
    parser = argparse.ArgumentParser(
        description="Local file-backed interactive chat client (prototype)"
    )
    parser.add_argument("--nick", required=True, help="Your nickname")
    parser.add_argument("--history-file", default="history.jsonl", help="Path to history file")
    parser.add_argument("--poll-interval", type=float, default=0.5, help="History poll interval (seconds)")
    args = parser.parse_args()

    run_interactive_chat_client(
        nick=args.nick,
        history_file=args.history_file,
        poll_interval=args.poll_interval
    )


if __name__ == "__main__":
    main()
