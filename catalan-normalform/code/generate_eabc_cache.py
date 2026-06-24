#!/usr/bin/env python3
"""
CLI-Tool zur Generierung von EABC-Cache-Dateien.

Usage:
    python generate_eabc_cache.py --max-n 100000 --output cache.h5
    python generate_eabc_cache.py --max-n 10000000 --output eabc_10M.h5 --compression gzip
"""

import argparse
import sys
import os
from pathlib import Path
import time

sys.path.append(os.path.dirname(__file__))
from utils.eabc_test_data import create_cache


def parse_scientific_notation(s: str) -> int:
    """
    Parse wissenschaftliche Notation (z.B. '10^7', '1e7').
    """
    if '^' in s:
        base, exp = s.split('^')
        return int(base) ** int(exp)
    else:
        return int(float(s))


def main():
    parser = argparse.ArgumentParser(
        description='Generiere EABC-Cache-Datei für effiziente Tests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Kleiner Test-Cache (10k Werte)
  %(prog)s --max-n 10000 --output test_cache.h5
  
  # Mittlerer Cache (100k Werte, ~6 MB)
  %(prog)s --max-n 100000 --output eabc_100k.h5
  
  # Großer Cache (10M Werte, ~760 MB, ~24 min)
  %(prog)s --max-n 10^7 --output eabc_10M.h5 --chunk-size 200000
  
  # Mit Kompression
  %(prog)s --max-n 10^6 --output eabc_1M.h5 --compression gzip
        """
    )
    
    parser.add_argument(
        '--max-n',
        type=str,
        required=True,
        help='Maximale Zahl (inklusiv). Unterstützt: 10^7, 1e7, 10000000'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=Path,
        required=True,
        help='Pfad zur Ausgabe-HDF5-Datei'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=100_000,
        help='Chunk-Größe für inkrementelles Speichern (default: 100,000)'
    )
    
    parser.add_argument(
        '--compression',
        type=str,
        choices=['gzip', 'lzf', 'none'],
        default='gzip',
        help='HDF5-Kompression (default: gzip)'
    )
    
    parser.add_argument(
        '--no-progress',
        action='store_true',
        help='Deaktiviere Progress-Bar'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Überschreibe existierende Datei'
    )
    
    args = parser.parse_args()
    
    # Parse max_n
    try:
        max_n = parse_scientific_notation(args.max_n)
    except Exception as e:
        print(f"Fehler beim Parsen von --max-n: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validierung
    if max_n < 2:
        print(f"Fehler: max_n muss ≥ 2 sein, erhalten: {max_n}", file=sys.stderr)
        sys.exit(1)
    
    if max_n > 10**8:
        print(f"Warnung: max_n = {max_n:,} ist sehr groß (> 10^8).")
        print(f"         Dies kann sehr lange dauern und viel Speicher benötigen.")
        confirm = input("Fortfahren? [y/N]: ")
        if confirm.lower() != 'y':
            print("Abgebrochen.")
            sys.exit(0)
    
    # Prüfe, ob Ausgabe-Datei existiert
    if args.output.exists() and not args.force:
        print(f"Fehler: Ausgabe-Datei existiert bereits: {args.output}", file=sys.stderr)
        print(f"        Verwende --force zum Überschreiben.", file=sys.stderr)
        sys.exit(1)
    
    # Schätze Dauer und Speicher
    if max_n >= 10**6:
        # Basierend auf Benchmark: 0.144 ms/Wert für n~1M
        estimated_time_min = (max_n * 0.000144) / 60
        estimated_size_mb = (max_n * 80) / (1024**2)
        
        print()
        print("=" * 70)
        print("SCHÄTZUNGEN")
        print("=" * 70)
        print(f"max_n:              {max_n:,}")
        print(f"Geschätzte Dauer:   ~{estimated_time_min:.1f} Minuten")
        print(f"Geschätzte Größe:   ~{estimated_size_mb:.1f} MB (unkomprimiert)")
        if args.compression != 'none':
            print(f"                    ~{estimated_size_mb * 0.5:.1f} MB (komprimiert, Schätzung)")
        print("=" * 70)
        print()
    
    # Kompression
    compression = None if args.compression == 'none' else args.compression
    
    # Generiere Cache
    print()
    print("Starte Cache-Generierung...")
    print()
    
    start_time = time.time()
    
    try:
        create_cache(
            max_n=max_n,
            output_file=args.output,
            chunk_size=args.chunk_size,
            show_progress=not args.no_progress,
            compression=compression
        )
    except Exception as e:
        print(f"\nFehler bei Cache-Generierung: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    elapsed_time = time.time() - start_time
    
    # Zusammenfassung
    print()
    print("=" * 70)
    print("FERTIG!")
    print("=" * 70)
    print(f"Datei:       {args.output}")
    print(f"Größe:       {args.output.stat().st_size / (1024**2):.2f} MB")
    print(f"max_n:       {max_n:,}")
    print(f"Einträge:    {max_n - 1:,}")
    print(f"Dauer:       {elapsed_time:.1f} Sekunden ({elapsed_time/60:.1f} Minuten)")
    print(f"Durchsatz:   {(max_n - 1) / elapsed_time:.0f} Werte/Sekunde")
    print("=" * 70)
    print()
    print("Verwende:")
    print(f"  from utils.eabc_test_data import EABCTestData")
    print(f"  data = EABCTestData(cache_file='{args.output}')")
    print(f"  coords = data.get_coordinates(12345)")
    print()


if __name__ == '__main__':
    main()
