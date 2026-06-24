#!/usr/bin/env python3
"""Zeigt inhaltliche Tagesziele fuer Tag 1-7 an."""

from __future__ import annotations

import argparse
import sys

DAY_GOALS = {
    1: {
        "titel": "Fundament (Plotkern + Expose)",
        "ziele": [
            "Expose in `roman/00_expose.md` ausfuellen.",
            "Konfliktformel in 2 Saetzen festlegen.",
            "Kapitel 1 als Stichpunkte vorbereiten.",
        ],
    },
    2: {
        "titel": "Figuren und Motivlagen",
        "ziele": [
            "Hauptfiguren in `roman/01_figuren.md` scharfstellen.",
            "Ziele, Angst und Fehler pro Hauptfigur definieren.",
            "Konflikte auf Plot ausrichten.",
        ],
    },
    3: {
        "titel": "Kapitelplan + Schreibstart",
        "ziele": [
            "`roman/02_kapitelplan.md` fertigstellen.",
            "Kapitel 1 und 2 als Rohfassung schreiben.",
            "Ersten Spannungscheck auf Kapitel 1 anwenden.",
        ],
    },
    4: {
        "titel": "Rohfassung vertiefen",
        "ziele": [
            "Kapitel 3 und 4 schreiben.",
            "Technische Wendung plausibel herleiten.",
            "Tempo und Konfliktdichte pruefen.",
        ],
    },
    5: {
        "titel": "Rohfassung abschliessen",
        "ziele": [
            "Kapitel 5 bis 7 als Rohfassung fertigstellen.",
            "Finalkonflikt und Aufloesung inhaltlich schliessen.",
            "Gesamtdramaturgie auf Luecken pruefen.",
        ],
    },
    6: {
        "titel": "Ueberarbeitung Runde 1",
        "ziele": [
            "Spannungspruefung fuer alle Kapitel durchfuehren.",
            "Stilkonsistenz und Szenenuebergaenge glatten.",
            "Plausibilitaetscheck auf rote Punkte fokussieren.",
        ],
    },
    7: {
        "titel": "Finalisierung",
        "ziele": [
            "Sprachliche Straffung und letzte Kuerzungen.",
            "`make build` ausfuehren und Ergebnis lesen.",
            "Abgabefassung als `manuskript_final.md` finalisieren.",
        ],
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Zeigt Tagesziele fuer den 7-Tage-Romanplan.")
    parser.add_argument("day", type=int, choices=range(1, 8), help="Tag 1-7")
    args = parser.parse_args()

    data = DAY_GOALS.get(args.day)
    if not data:
        print("Ungueltiger Tag.", file=sys.stderr)
        return 1

    print(f"Tag {args.day}: {data['titel']}")
    print("-" * 60)
    for idx, goal in enumerate(data["ziele"], start=1):
        print(f"{idx}. {goal}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
