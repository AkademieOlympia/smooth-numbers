"""
Demo: EABC-Test-Daten-Cache verwenden.

Zeigt die Verwendung der EABCTestData-Klasse für effiziente EABC-Berechnungen.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import time
from utils.eabc_test_data import EABCTestData
from utils.eabc import compute_svn_coordinates


def demo_single_lookups(data: EABCTestData):
    """Demonstriert einzelne Lookups."""
    print("=" * 70)
    print("DEMO 1: EINZELNE LOOKUPS")
    print("=" * 70)
    print()
    
    test_numbers = [60, 210, 2310, 30030]
    
    for n in test_numbers:
        coords = data.get_coordinates(n)
        eabc = data.get_eabc(n)
        
        print(f"n = {n}")
        print(f"  Ω(n) = {coords['omega']}")
        print(f"  EABC-Vektor = {eabc}")
        print(f"  H(n) = {coords['H']:.4f}")
        print(f"  Shell S(n) = {coords['shell']}")
        print()


def demo_batch_operations(data: EABCTestData):
    """Demonstriert Batch-Operationen."""
    print("=" * 70)
    print("DEMO 2: BATCH-OPERATIONEN")
    print("=" * 70)
    print()
    
    n_values = np.arange(100, 200)
    
    # Batch-Lookup
    start = time.perf_counter()
    eabc_batch = data.get_eabc_batch(n_values)
    omega_batch = data.get_omega_batch(n_values)
    H_batch = data.get_concentration_batch(n_values)
    elapsed = time.perf_counter() - start
    
    print(f"Batch-Lookup für {len(n_values)} Werte:")
    print(f"  Dauer: {elapsed*1000:.2f} ms")
    print(f"  Durchsatz: {len(n_values)/elapsed:.0f} Werte/s")
    print()
    
    # Statistiken
    print(f"Statistiken für n = {n_values[0]}..{n_values[-1]}:")
    print(f"  Durchschnitt Ω(n): {np.mean(omega_batch):.2f}")
    print(f"  Durchschnitt H(n): {np.nanmean(H_batch):.4f}")
    print(f"  Max Ω(n): {np.max(omega_batch)}")
    print()


def demo_performance_comparison(data: EABCTestData):
    """Vergleicht cached vs. uncached Performance."""
    print("=" * 70)
    print("DEMO 3: PERFORMANCE-VERGLEICH (Cached vs. Uncached)")
    print("=" * 70)
    print()
    
    n_values = np.random.randint(2, 10_000, size=1000)
    
    # Cached
    start = time.perf_counter()
    for n in n_values:
        _ = data.get_coordinates(n)
    time_cached = time.perf_counter() - start
    
    # Uncached (direkte Berechnung)
    start = time.perf_counter()
    for n in n_values:
        _ = compute_svn_coordinates(n)
    time_uncached = time.perf_counter() - start
    
    speedup = time_uncached / time_cached
    
    print(f"1000 zufällige Lookups:")
    print(f"  Cached:   {time_cached*1000:.2f} ms ({time_cached*1000/1000:.4f} ms/Lookup)")
    print(f"  Uncached: {time_uncached*1000:.2f} ms ({time_uncached*1000/1000:.4f} ms/Lookup)")
    print(f"  Speedup:  {speedup:.1f}×")
    print()


def demo_statistical_analysis(data: EABCTestData):
    """Zeigt statistische Analyse."""
    print("=" * 70)
    print("DEMO 4: STATISTISCHE ANALYSE")
    print("=" * 70)
    print()
    
    # Alle Werte bis 10,000
    n_values = np.arange(2, 10_001)
    
    # Batch-Lookup
    omega_values = data.get_omega_batch(n_values)
    H_values = data.get_concentration_batch(n_values)
    
    # Filter gültige H-Werte (nicht NaN)
    valid_H = H_values[~np.isnan(H_values)]
    
    print(f"Analyse für n = 2..10,000:")
    print()
    
    print(f"Ω(n) - Primfaktoranzahl:")
    print(f"  Mittelwert: {np.mean(omega_values):.2f}")
    print(f"  Median:     {np.median(omega_values):.0f}")
    print(f"  Maximum:    {np.max(omega_values)}")
    print(f"  Standardabweichung: {np.std(omega_values):.2f}")
    print()
    
    print(f"H(n) - Konzentration:")
    print(f"  Gültige Werte: {len(valid_H):,} / {len(n_values):,}")
    print(f"  Mittelwert: {np.mean(valid_H):.4f}")
    print(f"  Median:     {np.median(valid_H):.4f}")
    print(f"  Minimum:    {np.min(valid_H):.4f}")
    print(f"  Maximum:    {np.max(valid_H):.4f}")
    print()
    
    # Histogramm-Bins
    H_hist, H_bins = np.histogram(valid_H, bins=10)
    
    print("H(n) Verteilung (10 Bins):")
    for i in range(len(H_hist)):
        bar = "█" * int(H_hist[i] / max(H_hist) * 40)
        print(f"  [{H_bins[i]:.2f}, {H_bins[i+1]:.2f}]: {bar} ({H_hist[i]})")
    print()


def demo_interesting_examples(data: EABCTestData):
    """Findet interessante Beispiele."""
    print("=" * 70)
    print("DEMO 5: INTERESSANTE BEISPIELE")
    print("=" * 70)
    print()
    
    # Finde Zahlen mit maximaler Konzentration H=1
    print("Zahlen mit maximaler Konzentration (H = 1.0):")
    count = 0
    for n in range(2, 1000):
        coords = data.get_coordinates(n)
        if coords['H'] == 1.0 and coords['omega_eabc'] > 0:
            eabc = data.get_eabc(n)
            print(f"  n = {n:4d}: EABC = {eabc}, Ω_EABC = {coords['omega_eabc']}")
            count += 1
            if count >= 10:
                break
    print()
    
    # Finde Zahlen mit minimaler Konzentration H=0.25
    print("Zahlen mit minimaler Konzentration (H ≈ 0.25):")
    count = 0
    for n in range(2, 10_000):
        coords = data.get_coordinates(n)
        if abs(coords['H'] - 0.25) < 0.001 and coords['omega_eabc'] >= 4:
            eabc = data.get_eabc(n)
            print(f"  n = {n:5d}: EABC = {eabc}, H = {coords['H']:.4f}")
            count += 1
            if count >= 10:
                break
    print()
    
    # Finde Zahlen mit hoher Shell-Koordinate
    print("Zahlen mit hoher Shell-Koordinate (S ≥ 10):")
    count = 0
    for n in range(2, 10_000):
        coords = data.get_coordinates(n)
        if coords['shell'] >= 10:
            print(f"  n = {n:5d}: S = {coords['shell']}, v₂ = {coords['v2']}, v₃ = {coords['v3']}")
            count += 1
            if count >= 10:
                break
    print()


def main():
    """Hauptfunktion."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "EABC-CACHE DEMONSTRATION" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Lade Cache
    cache_file = "test_eabc_cache.h5"
    
    if not os.path.exists(cache_file):
        print(f"Fehler: Cache-Datei nicht gefunden: {cache_file}")
        print()
        print("Bitte zuerst Cache generieren mit:")
        print(f"  python code/generate_eabc_cache.py --max-n 10000 --output {cache_file}")
        return
    
    print(f"Lade Cache: {cache_file}")
    data = EABCTestData(cache_file=cache_file)
    print(f"✓ Cache geladen: max_n = {data.max_n:,}")
    print()
    
    # Demos
    demo_single_lookups(data)
    demo_batch_operations(data)
    demo_performance_comparison(data)
    demo_statistical_analysis(data)
    demo_interesting_examples(data)
    
    # Schließe Cache
    data.close()
    
    print("=" * 70)
    print("DEMO ABGESCHLOSSEN")
    print("=" * 70)
    print()


if __name__ == '__main__':
    main()
