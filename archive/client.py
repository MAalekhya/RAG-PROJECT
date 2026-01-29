import argparse  # parse command-line arguments
import json  # read/write JSON strings
import threading  # run background tail thread
import time  # sleep for polling
import uuid  # generate unique IDs for messages
import datetime  # get timestamps
import os  # filesystem helpers
import sys  # system utilities (unused but common)
from message_handler import create_message, dump_message, parse_message  # helper functions for messages

# Summary: Return current UTC timestamp in ISO8601 format as a string (UTC, trailing Z)
def now_iso():  # return current UTC time in ISO8601 format
    return datetime.datetime.utcnow().isoformat() + "Z"


# Summary: Append a serialized JSON message to the history file atomically (newline-delimited)
def write_message(history_file: str, message: dict):  # append a JSON message to history file
    with open(history_file, "a", encoding="utf-8") as f:  # open file for append
        f.write(dump_message(message) + "\n")  # write serialized JSON + newline
        f.flush()  # ensure it's written to disk immediately


# Summary: Continuously watch `history_file` for new lines and call `on_message` for each parsed message
def tail_history(history_file: str, stop_event: threading.Event, on_message, poll: float = 0.5):  # watch file for new lines
    # Simple tail implementation: seek to end and periodically read new lines
    with open(history_file, "r", encoding="utf-8") as f:  # open for read
        f.seek(0, os.SEEK_END)  # move to the end of file so we only see new lines
        while not stop_event.is_set():  # loop until told to stop
            line = f.readline()  # try to read a line
            print("Read line from the file :")
            print(line)
            if not line:  # no new line yet
                time.sleep(poll)  # wait a bit before checking again
                continue
            try:
                msg = parse_message(line)  # convert JSON line into dict
            except Exception:
                continue  # skip malformed lines
            on_message(msg)  # call the provided handler with the message


# Summary: Format and print a received message depending on its type (join/leave/message)
def print_message(me_nick, msg: dict):  # format and print a received message
    ts = msg.get("ts", "")  # timestamp field
    nick = msg.get("nick", "")  # sender nickname
    text = msg.get("text", "")  # message text
    mtype = msg.get("type", "msg")  # message type (join/leave/message)
    if mtype == "join":  # user joined
        print(f"[{ts}] -- {nick} joined --")
    elif mtype == "leave":  # user left
        print(f"[{ts}] -- {nick} left --")
    else:  # normal chat message
        print(f"[{ts}] {nick}: {text}")


# Summary: Parse CLI args, start tail thread, announce join, and run the interactive input loop
def main():  # entry point for the client
    parser = argparse.ArgumentParser(description="Local file-backed CLI chat client (prototype)")  # create CLI parser
    parser.add_argument("--nick", required=True, help="Your nickname")  # required nickname argument
    parser.add_argument("--history-file", default="history.jsonl", help="Path to history file")  # history file path
    parser.add_argument("--poll-interval", type=float, default=0.5, help="History poll interval (seconds)")  # polling interval
    args = parser.parse_args()  # parse CLI args

    nick = args.nick  # store nickname
    history_file = args.history_file  # store history path

    # Ensure history file exists
    open(history_file, "a", encoding="utf-8").close()  # create file if missing

    stop_event = threading.Event()  # event to tell tail thread to stop

    def on_message(msg):  # local callback for new messages
        try:
            print_message(nick, msg)  # print message to console
        except Exception:
            pass  # ignore errors in printing

    tail_thread = threading.Thread(target=tail_history, args=(history_file, stop_event, on_message, args.poll_interval), daemon=True)  # start background tail thread
    tail_thread.start()  # run the tail thread

    # Announce join
    join_msg = create_message("join", nick, "")  # make a join message
    write_message(history_file, join_msg)  # append join message to history

    try:
        while True:  # main input loop
            try:
                line = input(f"{nick}> ")  # prompt user for input
            except EOFError:
                break  # exit on EOF
            text = line.strip()  # trim whitespace
            if not text:
                continue  # ignore empty input
            if text.lower() in ("/quit", "/exit"):  # handle quit commands
                leave = create_message("leave", nick, "")  # make leave message
                write_message(history_file, leave)  # append leave message
                break  # exit loop
            msg = create_message("message", nick, text)  # create normal message
            write_message(history_file, msg)  # append message to history
    except KeyboardInterrupt:
        leave = create_message("leave", nick, "")  # on Ctrl+C, create leave message
        write_message(history_file, leave)  # write leave message
    finally:
        stop_event.set()  # signal tail thread to stop
        tail_thread.join(timeout=1)  # wait briefly for thread to exit


if __name__ == "__main__":  # run main when executed directly
    main()
