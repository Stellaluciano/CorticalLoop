"""Render a lightweight architecture diagram PNG without external deps."""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

W, H = 1200, 700


def _png_chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def _set_px(buf: bytearray, x: int, y: int, color: tuple[int, int, int]) -> None:
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i : i + 3] = bytes(color)


def _rect(buf: bytearray, x: int, y: int, w: int, h: int, fill=(226, 232, 240), stroke=(51, 65, 85)) -> None:
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            _set_px(buf, xx, yy, fill)
    for xx in range(x, x + w):
        _set_px(buf, xx, y, stroke)
        _set_px(buf, xx, y + h - 1, stroke)
    for yy in range(y, y + h):
        _set_px(buf, x, yy, stroke)
        _set_px(buf, x + w - 1, yy, stroke)


def _line(buf: bytearray, x1: int, y1: int, x2: int, y2: int, color=(15, 23, 42)) -> None:
    dx = abs(x2 - x1)
    sx = 1 if x1 < x2 else -1
    dy = -abs(y2 - y1)
    sy = 1 if y1 < y2 else -1
    err = dx + dy
    while True:
        _set_px(buf, x1, y1, color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x1 += sx
        if e2 <= dx:
            err += dx
            y1 += sy


def _arrow(buf: bytearray, x1: int, y1: int, x2: int, y2: int) -> None:
    _line(buf, x1, y1, x2, y2)
    _line(buf, x2, y2, x2 - 8, y2 - 4)
    _line(buf, x2, y2, x2 - 8, y2 + 4)


def main() -> None:
    pixels = bytearray([255, 255, 255] * W * H)

    boxes = [
        (40, 300, 180, 70),
        (300, 120, 230, 90),
        (580, 120, 230, 90),
        (860, 120, 230, 90),
        (860, 300, 230, 90),
        (580, 300, 230, 90),
        (300, 300, 230, 90),
        (580, 500, 230, 90),
        (860, 500, 280, 90),
    ]
    for box in boxes:
        _rect(pixels, *box)

    arrows = [
        (220, 335, 300, 165),
        (530, 165, 580, 165),
        (810, 165, 860, 165),
        (975, 210, 975, 300),
        (860, 345, 810, 345),
        (580, 345, 530, 165),
        (695, 390, 695, 500),
        (810, 545, 860, 545),
    ]
    for a in arrows:
        _arrow(pixels, *a)

    raw = bytearray()
    row_bytes = W * 3
    for y in range(H):
        raw.append(0)
        start = y * row_bytes
        raw.extend(pixels[start : start + row_bytes])

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + _png_chunk(b"IHDR", ihdr) + _png_chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + _png_chunk(b"IEND", b"")

    out = Path("assets/corticalloop_architecture.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(png)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
