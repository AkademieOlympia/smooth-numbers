#!/usr/bin/env python3
"""Zaehlt Woerter in allen Kapiteldateien."""

from __future__ import annotations

import re
import sys
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z0-9ÄÖÜäöüß]+")


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    chapter_dir = project_root / "roman" / "kapitel"

    if not chapter_dir.exists():
        print(f"Fehler: Kapitelordner nicht gefunden: {chapter_dir}", file=sys.stderr)
        return 1

    chapter_files = sorted(chapter_dir.glob("kapitel_*.md"))
    if not chapter_files:
        print("Keine Kapiteldateien gefunden.")
        return 0

    total = 0
    print("Wortzaehlung pro Kapitel")
    print("-" * 40)
    for path in chapter_files:
        content = path.read_text(encoding="utf-8")
        words = count_words(content)
        total += words
        print(f"{path.name:<18} {words:>7} Woerter")

    print("-" * 40)
    print(f"{'GESAMT':<18} {total:>7} Woerter")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
