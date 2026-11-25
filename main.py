#!/usr/bin/env python3
"""Entry program: copy the invitation image to /output/entry.png.

Standard library only. Deterministic: the same bytes every run.
Verifies the copy is byte-identical to the shipped image (PNG magic,
size and sha256) before finishing.

Usage:
    python3 main.py [--self-test]
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
MAX_DIM = 1024


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def png_dimensions(data):
    """Read width/height from the PNG IHDR chunk (stdlib only)."""
    if len(data) < 33 or data[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def self_test():
    """Validate the shipped image against the full competition gate:
    whole PNG, at most 1 MiB, at most 1024x1024 pixels."""
    src = HERE / "entry.png"
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("self-test FAILED: entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit(
            f"self-test FAILED: entry.png is {len(data)} bytes (> 1 MiB)")
    try:
        width, height = png_dimensions(data)
    except ValueError as e:
        raise SystemExit(f"self-test FAILED: {e}")
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(
            f"self-test FAILED: {width}x{height} exceeds 1024x1024")
    print(f"self-test OK: PNG {width}x{height}, {len(data)} bytes, "
          f"sha256 {sha256(src)}")
    return 0


def main():
    src = HERE / "entry.png"
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG")
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png exceeds 1 MiB")
    width, height = png_dimensions(data)
    if width > MAX_DIM or height > MAX_DIM:
        raise SystemExit(f"entry.png is {width}x{height}, exceeds 1024x1024")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, OUT)
    if sha256(OUT) != sha256(src):
        raise SystemExit("copied image is not byte-identical")
    print(f"wrote {OUT} ({len(data)} bytes, sha256 {sha256(src)[:16]}...)")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        raise SystemExit(self_test())
    main()
