import json
import os
import shutil
import time

STATE = os.environ.get("XDG_STATE_HOME") or os.path.join(os.path.expanduser("~"), ".local", "state")
PATH = os.environ.get("ANTIALGORITHM_HISTORY") or os.path.join(STATE, "antialgorithm", "history.jsonl")
OLD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "history.jsonl")
LIMITS = {"seed": 60, "move": 300}
DEFAULT_LIMIT = 300
LOCK_STALE = 10.0


def migrate():
    if not os.path.exists(PATH) and os.path.exists(OLD_PATH):
        os.makedirs(os.path.dirname(PATH), exist_ok=True)
        shutil.copyfile(OLD_PATH, PATH)


def load(kind=None):
    migrate()
    try:
        with open(PATH, encoding="utf-8") as f:
            lines = f.read().splitlines()
    except FileNotFoundError:
        return []
    out = []
    for line in lines:
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        if kind is None or entry.get("type") == kind:
            out.append(entry)
    return out


def acquire(lock_path):
    while True:
        try:
            os.close(os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            return
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(lock_path) > LOCK_STALE:
                    os.remove(lock_path)
                    continue
            except OSError:
                pass
            time.sleep(0.02)


def trim(rows):
    counts = {}
    kept = []
    for row in reversed(rows):
        kind = row.get("type")
        counts[kind] = counts.get(kind, 0) + 1
        if counts[kind] <= LIMITS.get(kind, DEFAULT_LIMIT):
            kept.append(row)
    kept.reverse()
    return kept


def add(entry):
    entry = {"date": time.strftime("%Y-%m-%d"), **entry}
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    lock_path = PATH + ".lock"
    acquire(lock_path)
    try:
        rows = trim(load() + [entry])
        tmp = PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
        os.replace(tmp, PATH)
    finally:
        os.remove(lock_path)
