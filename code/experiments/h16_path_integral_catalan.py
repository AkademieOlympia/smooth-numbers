#!/usr/bin/env python3
"""
H16 starter: diskrete Pfadsumme ueber Catalan-Baeume (defensives Skelett).

Dieses Skript ist absichtlich minimal:
- klarer CLI-Rahmen,
- reproduzierbare Parameter,
- TODO-Hooks fuer konkrete Aktionen/Enumeration/Reporting.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class ExperimentConfig:
    n_list: List[int]
    beta_values: List[float]
    action: str
    mode: str
    sample_budget: int
    seed: int
    outdir: Path


def parse_csv_ints(raw: str) -> List[int]:
    values = sorted({int(x.strip()) for x in raw.split(",") if x.strip()})
    if not values:
        raise ValueError("n-list darf nicht leer sein.")
    if min(values) < 2:
        raise ValueError("Alle n muessen >= 2 sein.")
    return values


def parse_csv_floats(raw: str) -> List[float]:
    values = [float(x.strip()) for x in raw.split(",") if x.strip()]
    if not values:
        raise ValueError("beta-list darf nicht leer sein.")
    if any(beta < 0 for beta in values):
        raise ValueError("beta-Werte muessen >= 0 sein.")
    return values


def parse_args() -> ExperimentConfig:
    parser = argparse.ArgumentParser(description="H16 diskrete Catalan-Pfadsumme (starter).")
    parser.add_argument("--n-list", type=str, default="60,72,84")
    parser.add_argument("--beta-list", type=str, default="0.0,0.2,0.5,1.0")
    parser.add_argument("--action", type=str, choices=["S1", "S2", "S3"], default="S1")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["exhaustive", "sampled"],
        default="exhaustive",
        help="Enumerationsmodus fuer Catalan-Baeume.",
    )
    parser.add_argument(
        "--sample-budget",
        type=int,
        default=1000,
        help="Nur relevant in mode=sampled.",
    )
    parser.add_argument("--seed", type=int, default=20260625)
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("experiments/results/h16_path_integral"),
    )
    args = parser.parse_args()
    if args.sample_budget < 1:
        raise ValueError("sample-budget muss >= 1 sein.")

    return ExperimentConfig(
        n_list=parse_csv_ints(args.n_list),
        beta_values=parse_csv_floats(args.beta_list),
        action=args.action,
        mode=args.mode,
        sample_budget=args.sample_budget,
        seed=args.seed,
        outdir=args.outdir,
    )


def run_h16_probe(config: ExperimentConfig) -> Dict[str, object]:
    # TODO(H16-1): Faktorenlisten je n erzeugen und Omega_tot bestimmen.
    # TODO(H16-2): Catalan-Baeume je n exhaustiv oder sampled enumerieren.
    # TODO(H16-3): Aktionen S1/S2/S3 entlang Zwischenprodukten q^(k) auswerten.
    # TODO(H16-4): Pfadgewichte, N_eff, Entropie, Top-k-Gewicht berechnen.
    # TODO(H16-5): Nullchecks (beta=0, Permutationscheck) integrieren.
    return {
        "status": "todo",
        "message": "Starter-Skelett ausgefuehrt; numerische H16-Auswertung ist noch TODO.",
        "n_count": len(config.n_list),
        "beta_count": len(config.beta_values),
        "action": config.action,
        "mode": config.mode,
    }


def write_stub_outputs(config: ExperimentConfig, payload: Dict[str, object]) -> None:
    config.outdir.mkdir(parents=True, exist_ok=True)
    run_cfg_path = config.outdir / "h16_run_config.json"
    run_out_path = config.outdir / "h16_stub_output.json"
    run_cfg_path.write_text(json.dumps(asdict(config), indent=2, default=str) + "\n", encoding="utf-8")
    run_out_path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")


def main() -> None:
    config = parse_args()
    payload = run_h16_probe(config)
    write_stub_outputs(config, payload)
    print("H16 starter completed.")
    print(f"outdir={config.outdir}")
    print(f"status={payload.get('status')}")


if __name__ == "__main__":
    main()
