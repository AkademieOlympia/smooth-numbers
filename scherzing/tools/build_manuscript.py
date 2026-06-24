#!/usr/bin/env python3
"""Fuegt alle Kapitel in eine finale Manuskriptdatei zusammen."""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    chapter_dir = project_root / "roman" / "kapitel"
    output_path = project_root / "manuskript_final.md"

    chapter_files = sorted(chapter_dir.glob("kapitel_*.md"))
    if not chapter_files:
        print("Fehler: Keine Kapiteldateien gefunden.", file=sys.stderr)
        return 1

    sections = []
    sections.append("# Manuskript (Final-Build)")
    sections.append("")
    sections.append(f"Build-Zeit: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    sections.append("")
    sections.append("> Automatisch erzeugt aus `roman/kapitel/`.")
    sections.append("")

    for path in chapter_files:
        content = path.read_text(encoding="utf-8").strip()
        sections.append(f"---\n\n<!-- Quelle: {path.name} -->\n")
        sections.append(content)
        sections.append("")

    output_path.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    print(f"Manuskript gebaut: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
