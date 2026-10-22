#!/bin/bash
# Check the sprite maker: the examples convert, PNGs are valid, and mistakes give friendly errors.
set -euo pipefail
cd "$(dirname "$0")"
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
cp examples/*.txt "$tmp/"
for f in "$tmp"/*.txt; do python3 make_sprite.py "$f" >/dev/null; done
python3 - "$tmp" <<'PY'
import pathlib, struct, sys, zlib
for png in sorted(pathlib.Path(sys.argv[1]).glob("*.png")):
    data = png.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", png
    w, h = struct.unpack(">II", data[16:24])
    assert (w, h) == (40, 40) or (w, h) == (40, 35), (png, w, h)
    # walk the chunks and check every CRC
    i = 8
    while i < len(data):
        n = struct.unpack(">I", data[i:i+4])[0]
        body = data[i+4:i+8+n]
        assert struct.unpack(">I", data[i+8+n:i+12+n])[0] == zlib.crc32(body), png
        i += 12 + n
    print("ok", png.name, w, "x", h)
PY
printf 'gg\nggg\n' > "$tmp/bad1.txt"; printf 'gq\n' > "$tmp/bad2.txt"; printf 'q = #00FF00\nqq\n' > "$tmp/custom.txt"
expect_error() {  # FILE MESSAGE: the maker must refuse FILE and say MESSAGE
  local out
  if out=$(python3 make_sprite.py "$1" 2>&1); then echo "FAIL $1 was accepted"; exit 1; fi
  grep -qF "$2" <<<"$out" || { echo "FAIL $1 said: $out"; exit 1; }
  echo "ok $(basename "$1") rejected: $2"
}
expect_error "$tmp/bad1.txt" "same width"
expect_error "$tmp/bad2.txt" "don't know the colour 'q'"
python3 make_sprite.py "$tmp/custom.txt" >/dev/null && echo "ok custom colour"
