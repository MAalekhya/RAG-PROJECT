import json
import uuid
import datetime


def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"


def create_message(mtype: str, nick: str, text: str, source: str = "local") -> dict:
    return {
        "type": mtype,
        "nick": nick,
        "text": text,
        "ts": now_iso(),
        "id": str(uuid.uuid4()),
        "source": source,
    }


def dump_message(message: dict) -> str:
    return json.dumps(message, ensure_ascii=False)


def parse_message(line: str) -> dict:
    obj = json.loads(line)
    # Basic validation
    if not isinstance(obj, dict):
        raise ValueError("Invalid message")
    if "type" not in obj or "nick" not in obj:
        raise ValueError("Missing required fields")
    return obj
