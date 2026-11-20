#!/usr/bin/env python3
"""Place the finished front page where the grader reads it.

The picture itself is rendered ahead of time by draw.py and kept in this
repository as entry.png. This program only drops a copy of that file at
the grader's output path, using the standard library and no network.
Two runs produce the same bytes both times.
"""

from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"


def run():
    import os
    if SRC.is_file():
        dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
        dest.mkdir(parents=True, exist_ok=True)
        out = dest / "entry.png"
        out.write_bytes(SRC.read_bytes())
        print("wrote", out)
        return 0
    print("entry.png is missing; generate it with draw.py first")
    return 1


if __name__ == "__main__": raise SystemExit(run())
