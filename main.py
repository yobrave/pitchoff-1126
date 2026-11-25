#!/usr/bin/env python3
"""ams entry pump: one line in, one artifact out."""

import json
import os
from pathlib import Path

BOUNTY_CAP = 200
OUT_NAME = "entry.txt"


def flatten(multiline_blob):
    """Return the first non-empty line so gates always see single-line text."""
    for segment in multiline_blob.splitlines():
        cleaned = segment.strip()
        if cleaned:
            return segment.rstrip()
    return ""


def pump():
    here = Path(__file__).resolve().parent
    entry_src = here / OUT_NAME
    if not entry_src.is_file():
        print(json.dumps({"ok": False, "reason": "no entry.txt beside main.py"}))
        return 4
    raw = entry_src.read_text(encoding="utf-8")
    line = flatten(raw.replace("\r", ""))
    width = len(line)
    passes = 1 <= width <= BOUNTY_CAP and bool(line.strip())
    if not passes:
        print(json.dumps({"ok": False, "width": width, "cap": BOUNTY_CAP}))
        return 1
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    Path(base).mkdir(parents=True, exist_ok=True)
    Path(base, OUT_NAME).write_bytes(line.encode("utf-8"))
    print(json.dumps({"ok": True, "width": width, "cap": BOUNTY_CAP}))
    return 0


if __name__ == "__main__":
    raise SystemExit(pump())
