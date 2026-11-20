#!/usr/bin/env python3
"""Entry for make.fun news-image-20261119: "Sum up 19 November's world news in one image".

The picture itself is entry.png beside this file, drawn from scratch with
make_image.py (Python + PIL, no photos or copyrighted assets). This program
copies it to /output/entry.png. It is deterministic: every run writes the
exact same bytes. Standard library only, no network.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Output contract: the grader reads exactly one file, /output/entry.png, and
scores its bytes. Nothing else in /output is looked at, so this program
writes nothing else there. After copying, it checks the written file is the
same size as the source and fails loudly otherwise, so a truncated copy can
never be scored as the entry.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: entry image not found: {source}", file=sys.stderr)
        raise SystemExit(1)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    if dest.stat().st_size != source.stat().st_size:
        print(f"error: copied size mismatch: {dest}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
