import json
import sys
import os
# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from core.message_handler import create_message, dump_message, parse_message


def test_create_and_parse_message_roundtrip():
    msg = create_message("message", "alice", "hello")
    s = dump_message(msg)
    parsed = parse_message(s)
    assert parsed["type"] == "message"
    assert parsed["nick"] == "alice"
    assert parsed["text"] == "hello"
    assert "ts" in parsed
    assert "id" in parsed
