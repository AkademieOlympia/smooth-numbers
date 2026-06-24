#!/usr/bin/env python3
"""Erstellt einen Soll/Ist-Fortschrittsreport fuer 7 Schreibtage."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z0-9ÄÖÜäöüß]+")

DAY_TARGETS = {
    1: 1200,
    2: 2600,
    3: 6000,
    4: 10000,
    5: 16000,
    6: 20000,
    7: 22000,
}


def count_words_in_chapters(project_root: Path) -> int:
    chapter_dir = project_root / "roman" / "kapitel"
    chapter_files = sorted(chapter_dir.glob("kapitel_*.md"))
    total = 0
    for path in chapter_files:
        total += len(WORD_RE.findall(path.read_text(encoding="utf-8")))
    return total


def infer_day(total_words: int) -> int:
    day = 1
    for d, target in DAY_TARGETS.items():
        if total_words >= target:
            day = d
    return min(day + 1, 7) if day < 7 else 7


def render_status(total_words: int, day_focus: int) -> str:
    lines = []
    lines.append("Fortschrittsreport (Soll/Ist)")
    lines.append("-" * 64)
    lines.append(f"Aktueller Stand: {total_words} Woerter")
    lines.append(f"Heutiger Fokus (Tag): {day_focus}")
    lines.append("")
    lines.append(f"{'Tag':<5}{'Soll kumuliert':>16}{'Ist':>10}{'Status':>14}")
    lines.append("-" * 64)

    for day in range(1, 8):
        target = DAY_TARGETS[day]
        ok = total_words >= target
        if ok:
            status = "erreicht"
        elif day == day_focus:
            status = "heute aktiv"
        else:
            status = "offen"
        lines.append(f"{day:<5}{target:>16}{total_words:>10}{status:>14}")

    lines.append("-" * 64)
    next_target = DAY_TARGETS[day_focus]
    delta = max(next_target - total_words, 0)
    lines.append(f"Delta bis Tagesziel: {delta} Woerter")
    lines.append("Tipp: Nutze `make dayX`, um den inhaltlichen Fokus je Tag zu sehen.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Soll/Ist-Fortschritt fuer das Romanprojekt.")
    parser.add_argument(
        "--day",
        type=int,
        choices=range(1, 8),
        metavar="{1..7}",
        help="Tag fuer den Fokusbericht (1-7). Wenn leer, wird ein Tag vorgeschlagen.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    total_words = count_words_in_chapters(project_root)
    day_focus = args.day or infer_day(total_words)

    print(render_status(total_words, day_focus))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
