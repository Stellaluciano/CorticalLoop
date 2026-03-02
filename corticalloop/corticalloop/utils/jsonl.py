"""JSONL helper utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def write_jsonl(path: str | Path, rows: Iterable[dict]) -> None:
    with Path(path).open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
