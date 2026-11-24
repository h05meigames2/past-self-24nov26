#!/usr/bin/env python3
"""Two Lines to Your Past Self — make.fun entry.

Writes exactly two lines to /output/entry.txt. Line one warns my past self
about one specific moment — a text typed at 2am from the kitchen table on
the night she said she was leaving — in a single sentence; line two says in
one sentence why that moment mattered and what changed because of it: the
words could never be taken back, and the apology rehearsed for three years
only ever made sense in the silence that followed.
"""

import os
import re
import sys

LINE1 = "Don't send that text at 2am from the kitchen table the night she says she's leaving \u2014 put the phone down and let her finish."
LINE2 = "You never got those words back, and the apology you rehearsed for three years only ever made sense in the silence that followed."

MAX_CHARS = 280


def _sentence_count(line: str) -> int:
    """Count sentence-ending marks (. ! ?) in a line."""
    return len(re.findall(r"[.!?]", line))


def validate(line1: str, line2: str) -> str:
    """Validate the two lines and return the exact entry text."""
    lines = [line1, line2]
    for i, line in enumerate(lines, start=1):
        if not line or not line.strip():
            raise ValueError(f"line {i} is empty")
        if line != line.strip():
            raise ValueError(f"line {i} has leading/trailing whitespace")
        if _sentence_count(line) != 1:
            raise ValueError(
                f"line {i} must be exactly one sentence "
                f"(found {_sentence_count(line)} sentence marks)"
            )
    text = line1 + "\n" + line2 + "\n"
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if len(text.strip().splitlines()) != 2:
        raise ValueError("entry must be exactly two lines")
    return text


def main() -> int:
    text = validate(LINE1, LINE2)
    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.txt")
    except OSError:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(out_path, "r", encoding="utf-8") as f:
        round_trip = f.read()
    if round_trip != text:
        raise ValueError("round-trip verification failed")
    print(text, end="")
    print(f"---\nWrote {out_path} ({len(text)} chars, 2 lines, valid)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
