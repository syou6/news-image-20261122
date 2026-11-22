#!/usr/bin/env python3
"""make.fun news-image entry for Sunday 22 November 2026.

The repository holds entry.png, a one-page collage of the day's world
news (drawn by build_image.py). This program copies it to the output
directory as entry.png, byte for byte, and verifies the copy.

It runs with the Python 3.13 standard library only, with no network.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576  # the gate's 1 MiB cap
MAX_DIM = 1024         # the gate's pixel cap

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def png_dimensions(data):
    """(width, height) from a PNG's IHDR chunk, else None."""
    if len(data) < 24 or not data.startswith(PNG_MAGIC):
        return None
    return struct.unpack(">II", data[16:24])


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(SOURCE):
        return fail(f"entry image missing: {SOURCE}")

    with open(SOURCE, "rb") as fh:
        data = fh.read()
    if not (data.startswith(PNG_MAGIC) or data.startswith(JPEG_MAGIC)):
        return fail("entry image is neither PNG nor JPEG")

    size = len(data)
    if size > MAX_BYTES:
        return fail(f"entry image too large: {size} bytes > {MAX_BYTES}")

    dims = png_dimensions(data)
    if dims and (dims[0] > MAX_DIM or dims[1] > MAX_DIM):
        return fail(f"entry image too big: {dims[0]}x{dims[1]} over {MAX_DIM}px")

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, dest)

    if digest(dest) != digest(SOURCE):
        return fail("copy verification failed: bytes differ")
    print(f"wrote {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
