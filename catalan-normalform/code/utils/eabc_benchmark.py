"""
Performance-Benchmark für EABC-Berechnung.

Testet die aktuelle Implementierung und schätzt den Aufwand für n=10^7.
"""

import time
import numpy as np
from typing import List, Tuple
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.eabc import compute_eabc_vector, compute_H, compute_svn_coordinates


def benchmark_single_computation(n: int) -> Tuple[float, dict]:
    """
    Benchmarkt einzelne EABC-Berechnung.
    
    Returns:
        (elapsed_time, result_dict)
    """
    start = time.perf_counter()
    result = compute_svn_coordinates(n)
    elapsed = time.perf_counter() - start
    return elapsed, result


def benchmark_range(n_start: int, n_end: int, sample_size: int = 1000) -> dict:
    """
    Benchmarkt EABC-Berechnung über einen Bereich.
    
    Args:
        n_start: Start-Wert
        n_end: End-Wert
        sample_size: Anzahl zu testender Werte
        
    Returns:
        Dictionary mit Statistiken
    """
    # Sample gleichmäßig verteilt
    if sample_size >= (n_end - n_start):
        n_values = list(range(n_start, n_end + 1))
    else:
        n_values = np.linspace(n_start, n_end, sample_size, dtype=int)
    
    times = []
    omega_values = []
    
    for n in n_values:
        elapsed, result = benchmark_single_computation(n)
        times.append(elapsed)
        omega_values.append(result['omega'])
    
    times = np.array(times)
    omega_values = np.array(omega_values)
    
    return {
        'n_start': n_start,
        'n_end': n_end,
        'sample_size': len(n_values),
        'mean_time': np.mean(times),
        'median_time': np.median(times),
        'std_time': np.std(times),
        'min_time': np.min(times),
        'max_time': np.max(times),
        'total_time': np.sum(times),
        'mean_omega': np.mean(omega_values),
        'max_omega': np.max(omega_values)
    }


def estimate_storage_requirements(n_max: int = 10**7) -> dict:
    """
    Schätzt Speicherbedarf für EABC-Cache bis n_max.
    
    Pro Eintrag speichern wir:
    - n: int64 (8 bytes)
    - omega: int32 (4 bytes)
    - sigma: int64 (8 bytes)
    - v2: int32 (4 bytes)
    - v3: int32 (4 bytes)
    - e, a, b, c: int32 × 4 (16 bytes)
    - H: float64 (8 bytes)
    - norm_sq: float64 (8 bytes)
    - omega_eabc: int32 (4 bytes)
    
    Total: ~64 bytes pro Eintrag (konservativ: 80 bytes mit Overhead)
    """
    bytes_per_entry = 80  # Konservative Schätzung
    total_bytes = n_max * bytes_per_entry
    
    # Verschiedene Einheiten
    mb = total_bytes / (1024**2)
    gb = total_bytes / (1024**3)
    
    return {
        'n_max': n_max,
        'bytes_per_entry': bytes_per_entry,
        'total_bytes': total_bytes,
        'total_mb': mb,
        'total_gb': gb
    }


def print_report(benchmarks: dict, storage: dict):
    """
    Druckt formatierten Report.
    """
    print("=" * 70)
    print("EABC-PERFORMANCE-ANALYSE")
    print("=" * 70)
    print()
    
    # Performance-Statistiken
    print("### PERFORMANCE-STATISTIKEN ###")
    print()
    for label, bench in benchmarks.items():
        print(f"Bereich: n = {bench['n_start']:,} bis {bench['n_end']:,}")
        print(f"  Sample-Größe: {bench['sample_size']:,}")
        print(f"  Durchschnitt: {bench['mean_time']*1000:.4f} ms/Berechnung")
        print(f"  Median:       {bench['median_time']*1000:.4f} ms/Berechnung")
        print(f"  Std-Abw:      {bench['std_time']*1000:.4f} ms")
        print(f"  Min/Max:      {bench['min_time']*1000:.4f} / {bench['max_time']*1000:.4f} ms")
        print(f"  Gesamt:       {bench['total_time']:.2f} s für {bench['sample_size']:,} Werte")
        print(f"  Ø Ω(n):       {bench['mean_omega']:.2f}")
        print(f"  Max Ω(n):     {bench['max_omega']}")
        print()
    
    # Hochrechnung für n=10^7
    print("### HOCHRECHNUNG FÜR n = 10^7 ###")
    print()
    
    # Verwende letzten Benchmark als Basis
    last_bench = list(benchmarks.values())[-1]
    avg_time_per_value = last_bench['mean_time']
    
    n_total = 10**7
    estimated_total_time = n_total * avg_time_per_value
    
    print(f"Geschätzte Gesamtzeit: {estimated_total_time/3600:.2f} Stunden")
    print(f"                        ({estimated_total_time/60:.2f} Minuten)")
    print()
    
    # Speicheranforderungen
    print("### SPEICHERANFORDERUNGEN ###")
    print()
    print(f"n_max = {storage['n_max']:,}")
    print(f"Bytes pro Eintrag: {storage['bytes_per_entry']}")
    print(f"Gesamt-Speicher:")
    print(f"  - {storage['total_mb']:.2f} MB")
    print(f"  - {storage['total_gb']:.2f} GB")
    print()
    
    # Empfehlungen
    print("### EMPFEHLUNGEN ###")
    print()
    if storage['total_gb'] < 1:
        print("✓ Speicherbedarf ist moderat (< 1 GB)")
        print("  → HDF5, NumPy .npz oder Pickle sind alle geeignet")
    else:
        print("! Speicherbedarf > 1 GB")
        print("  → HDF5 empfohlen (komprimiert, inkrementelles Laden)")
    
    print()
    
    if estimated_total_time > 3600:
        print("! Generierung dauert > 1 Stunde")
        print("  → Incremental generation mit Progress-Bar empfohlen")
        print("  → Chunk-weise Speicherung (z.B. alle 100k Werte)")
    else:
        print("✓ Generierung dauert < 1 Stunde")
        print("  → Direkte Generierung möglich")
    
    print()
    print("=" * 70)


def main():
    """
    Hauptfunktion: Führt Benchmarks durch und erstellt Report.
    """
    print("Starte EABC-Performance-Analyse...")
    print()
    
    # Benchmark verschiedene Bereiche
    benchmarks = {}
    
    print("Benchmark 1/4: n = 2..100 (kleine Zahlen)...")
    benchmarks['small'] = benchmark_range(2, 100, sample_size=99)
    
    print("Benchmark 2/4: n = 100..10,000 (mittlere Zahlen)...")
    benchmarks['medium'] = benchmark_range(100, 10_000, sample_size=1000)
    
    print("Benchmark 3/4: n = 10,000..100,000 (große Zahlen)...")
    benchmarks['large'] = benchmark_range(10_000, 100_000, sample_size=1000)
    
    print("Benchmark 4/4: n = 100,000..1,000,000 (sehr große Zahlen)...")
    benchmarks['very_large'] = benchmark_range(100_000, 1_000_000, sample_size=1000)
    
    print()
    
    # Speicheranforderungen
    storage = estimate_storage_requirements(n_max=10**7)
    
    # Report
    print_report(benchmarks, storage)
    
    # Zusätzliche Analyse: Korrelation Zeit vs. Ω(n)
    print("\n### KORRELATION: Rechenzeit vs. Ω(n) ###")
    print()
    print("Teste 100 Zufallswerte zwischen 10,000 und 100,000...")
    
    np.random.seed(42)
    test_values = np.random.randint(10_000, 100_000, size=100)
    
    times = []
    omegas = []
    
    for n in test_values:
        elapsed, result = benchmark_single_computation(n)
        times.append(elapsed)
        omegas.append(result['omega'])
    
    times = np.array(times)
    omegas = np.array(omegas)
    
    # Korrelation
    corr = np.corrcoef(times, omegas)[0, 1]
    
    print(f"Korrelation: r = {corr:.4f}")
    
    if corr > 0.7:
        print("→ Starke Korrelation: Rechenzeit steigt mit Ω(n)")
        print("  (Erwartetes Verhalten: Primfaktorzerlegung ist aufwändiger für Zahlen mit vielen Faktoren)")
    elif corr > 0.3:
        print("→ Moderate Korrelation")
    else:
        print("→ Schwache Korrelation")
    
    print()


if __name__ == "__main__":
    main()
