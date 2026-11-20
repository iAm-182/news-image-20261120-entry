#!/usr/bin/env python3
"""Entry point for the news-image-20261120 submission.

Copies the pre-rendered front page (entry.png, produced by draw.py) into
the grader's output directory. Standard library only, no network, no
side effects beyond the single copy. The output is byte-identical to
entry.png on every run.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        sys.stderr.write("entry.png missing; run draw.py first\n")
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied entry.png to", dst)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
