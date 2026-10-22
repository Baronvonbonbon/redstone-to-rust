#!/usr/bin/env python3
"""Turn text pixel art into a PNG picture, for Pygame Zero games.

Write a picture as a text file, one letter per pixel:

    # diamond.txt
    ...cc...
    ..cwcc..
    .cccccc.
    ..cccc..
    ...cc...

Then run:

    python3 make_sprite.py diamond.txt            # makes diamond.png
    python3 make_sprite.py diamond.txt --size 4   # each pixel 4x4 (default 5)

Letters:  . see-through   k black   w white   s stone gray   r red
          o orange   y yellow   g green   d dark green   c cyan   b blue
          p purple   m pink   n brown   t tan

Make your own colours with a line like this before the picture:

    x = #FF8800

Lines starting with # are notes and are skipped. Blank lines are skipped too.
"""
import argparse
import pathlib
import re
import struct
import sys
import zlib

PALETTE = {
    ".": None,
    "k": "#000000",
    "w": "#FFFFFF",
    "s": "#8B8B8B",
    "r": "#E53935",
    "o": "#FB8C00",
    "y": "#FDD835",
    "g": "#43A047",
    "d": "#1B5E20",
    "c": "#4DD0E1",
    "b": "#1E88E5",
    "p": "#8E24AA",
    "m": "#F48FB1",
    "n": "#6D4C41",
    "t": "#D7B98E",
}

COLOUR_LINE = re.compile(r"^(\S)\s*=\s*#([0-9A-Fa-f]{6})\s*$")


def fail(message):
    sys.exit(f"make_sprite: {message}")


def read_picture(path):
    palette = dict(PALETTE)
    rows = []
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        match = COLOUR_LINE.match(line)
        if match:
            palette[match.group(1)] = "#" + match.group(2)
            continue
        for letter in line:
            if letter not in palette:
                fail(f"line {number}: I don't know the colour '{letter}'. "
                     f"Add a line like '{letter} = #FF8800' above the picture.")
        rows.append((number, line))
    if not rows:
        fail(f"{path} has no picture in it.")
    width = len(rows[0][1])
    for number, line in rows:
        if len(line) != width:
            fail(f"line {number} is {len(line)} letters wide, but the first "
                 f"line is {width}. Every line must be the same width.")
    return [line for _, line in rows], palette


def rgba(colour):
    if colour is None:
        return bytes([0, 0, 0, 0])
    return bytes.fromhex(colour[1:]) + b"\xff"


def png_bytes(rows, palette, size):
    raw = bytearray()
    for line in rows:
        pixels = b"".join(rgba(palette[letter]) * size for letter in line)
        for _ in range(size):
            raw += b"\x00" + pixels  # filter type 0, then the row

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    width, height = len(rows[0]) * size, len(rows) * size
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)  # 8-bit RGBA
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def main():
    parser = argparse.ArgumentParser(description="Turn text pixel art into a PNG.")
    parser.add_argument("picture", type=pathlib.Path, help="the .txt picture file")
    parser.add_argument("--size", type=int, default=5,
                        help="how many screen pixels each letter becomes (default 5)")
    args = parser.parse_args()
    if not args.picture.is_file():
        fail(f"can't find the file {args.picture}")
    if not 1 <= args.size <= 50:
        fail("--size must be between 1 and 50")
    rows, palette = read_picture(args.picture)
    out = args.picture.with_suffix(".png")
    out.write_bytes(png_bytes(rows, palette, args.size))
    print(f"Made {out} ({len(rows[0]) * args.size} x {len(rows) * args.size} pixels)")


if __name__ == "__main__":
    main()
