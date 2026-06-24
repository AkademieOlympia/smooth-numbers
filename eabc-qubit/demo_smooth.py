#!/usr/bin/env python3
"""
Quick Demo: Smooth Numbers Integration

Zeigt die wichtigsten Features der Smooth-Integration:
1. Glattheitsdichten einzelner Zahlen
2. Potentiallandschaft visualisieren
3. MultiLayerHamiltonian mit Smooth
4. Vergleich mit/ohne Smooth
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.smooth_integration import (
    smooth_density_fast,
    largest_prime_factor,
    smooth_potential_landscape,
    analyze_smooth_statistics,
    print_smooth_statistics
)
from src.hamiltonian import MultiLayerHamiltonian
from src.level_spacing import compute_level_spacings, estimate_brody_q


def demo_1_smooth_density():
    """Demo 1: Glattheitsdichte einzelner Zahlen."""
    print("\n" + "="*70)
    print("DEMO 1: Glattheitsdichte einzelner Zahlen")
    print("="*70)
    
    test_numbers = [1, 2, 12, 30, 97, 128, 210, 997]
    max_k = 20
    
    print(f"\nGlattheitsdichte für max_k={max_k}:\n")
    print(f"{'n':>6s} │ {'p_max':>6s} │ {'Dichte':>8s} │ Interpretation")
    print("─" * 6 + "┼" + "─" * 8 + "┼" + "─" * 10 + "┼" + "─" * 30)
    
    for n in test_numbers:
        density = smooth_density_fast(n, max_k)
        p_max = largest_prime_factor(n)
        
        if density > 0.8:
            interp = "sehr glatt"
        elif density > 0.5:
            interp = "glatt"
        elif density > 0.2:
            interp = "mittel"
        else:
            interp = "rau (Primzahl-artig)"
        
        print(f"{n:6d} │ {p_max:6d} │ {density:8.3f} │ {interp}")
    
    print("\n→ Glatte Zahlen (kleine Primfaktoren) haben hohe Dichte")
    print("→ Primzahlen haben niedrige Dichte (nur für k ≥ p glatt)")


def demo_2_landscape():
    """Demo 2: Potentiallandschaft."""
    print("\n" + "="*70)
    print("DEMO 2: Potentiallandschaft visualisieren")
    print("="*70)
    
    N = 200
    max_k = 20
    
    print(f"\nGeneriere Potentiallandschaft für N={N}, max_k={max_k}...")
    landscape = smooth_potential_landscape(N, max_k)
    
    # Statistiken
    stats = analyze_smooth_statistics(N, max_k)
    print_smooth_statistics(stats)
    
    # Visualisierung
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Plot 1: Potentiallandschaft
    ax = axes[0]
    ax.plot(range(1, N+1), landscape, 'o-', markersize=3, alpha=0.7, color='steelblue')
    ax.set_xlabel('n', fontsize=12)
    ax.set_ylabel('Glattheitsdichte', fontsize=12)
    ax.set_title(f'Smooth Potential Landscape (N={N}, max_k={max_k})', 
                 fontsize=14, fontweight='bold')
    ax.grid(alpha=0.3)
    ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Mittelwert-Referenz')
    ax.legend()
    
    # Plot 2: Histogramm
    ax = axes[1]
    ax.hist(landscape, bins=30, color='coral', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Glattheitsdichte', fontsize=12)
    ax.set_ylabel('Häufigkeit', fontsize=12)
    ax.set_title('Verteilung der Glattheitsdichten', fontsize=14, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.axvline(x=np.mean(landscape), color='red', linestyle='--', 
               linewidth=2, label=f'Mittelwert: {np.mean(landscape):.3f}')
    ax.legend()
    
    plt.tight_layout()
    
    # Speichere Plot
    output_dir = Path("figures")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "smooth_landscape_demo.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot gespeichert: {output_path}")
    
    plt.show()


def demo_3_multilayer_hamiltonian():
    """Demo 3: MultiLayerHamiltonian mit Smooth."""
    print("\n" + "="*70)
    print("DEMO 3: MultiLayerHamiltonian mit Smooth-Potential")
    print("="*70)
    
    N = 100
    
    # Szenario 1: Nur Basis (TB + χ)
    print("\n--- Szenario 1: Nur Tight-Binding + Chiralität ---")
    H1 = MultiLayerHamiltonian(
        N=N,
        alpha=1.0,
        beta=0.5,
        use_primes=False,
        use_smooth=False
    )
    H1.info()
    E1 = H1.compute_spectrum(k=50, which='SM')
    
    # Szenario 2: Mit Primzahlen
    print("\n--- Szenario 2: + Primzahl-Defekte ---")
    H2 = MultiLayerHamiltonian(
        N=N,
        alpha=1.0,
        beta=0.5,
        gamma=1.5,
        use_primes=True,
        use_smooth=False
    )
    H2.info()
    E2 = H2.compute_spectrum(k=50, which='SM')
    
    # Szenario 3: Mit Smooth
    print("\n--- Szenario 3: + Glattheitspotential ---")
    H3 = MultiLayerHamiltonian(
        N=N,
        alpha=1.0,
        beta=0.5,
        gamma=1.5,
        eta=0.5,
        use_primes=True,
        use_smooth=True,
        smooth_max_k=20
    )
    H3.info()
    E3 = H3.compute_spectrum(k=50, which='SM')
    
    # Vergleiche Spektren
    print("\n" + "="*70)
    print("Spektralvergleich (erste 10 Eigenwerte)")
    print("="*70)
    print(f"{'i':>3s} │ {'Basis':>10s} │ {'+ Primes':>10s} │ {'+ Smooth':>10s}")
    print("─" * 4 + "┼" + "─" * 12 + "┼" + "─" * 12 + "┼" + "─" * 12)
    
    for i in range(10):
        print(f"{i+1:3d} │ {E1[i]:10.5f} │ {E2[i]:10.5f} │ {E3[i]:10.5f}")


def demo_4_comparison():
    """Demo 4: Vergleich mit/ohne Smooth (Hauptfrage)."""
    print("\n" + "="*70)
    print("DEMO 4: Effekt von Glattheit auf Chaos")
    print("="*70)
    print("\nFrage: Wirkt Glattheit verstärkend oder dämpfend auf Chaos?\n")
    
    N = 500
    k = 300
    
    # Ohne Smooth
    print("Berechne Spektrum OHNE Smooth...")
    H_without = MultiLayerHamiltonian(
        N=N,
        gamma=1.5,
        eta=0.0,
        use_primes=True,
        use_collatz=True,
        use_smooth=False
    )
    E_without = H_without.compute_spectrum(k=k, which='SM')
    spacings_without = compute_level_spacings(E_without)
    q_without = estimate_brody_q(spacings_without)
    
    # Mit Smooth
    print("\nBerechne Spektrum MIT Smooth...")
    H_with = MultiLayerHamiltonian(
        N=N,
        gamma=1.5,
        eta=0.5,
        use_primes=True,
        use_collatz=True,
        use_smooth=True,
        smooth_max_k=20
    )
    E_with = H_with.compute_spectrum(k=k, which='SM')
    spacings_with = compute_level_spacings(E_with)
    q_with = estimate_brody_q(spacings_with)
    
    # Ergebnisse
    delta_q = q_with - q_without
    
    print("\n" + "="*70)
    print("ERGEBNISSE")
    print("="*70)
    print(f"\nOhne Smooth: q = {q_without:.4f}")
    print(f"Mit Smooth:  q = {q_with:.4f}")
    print(f"Δq = {delta_q:+.4f}")
    
    print("\n" + "─" * 70)
    print("INTERPRETATION:")
    print("─" * 70)
    
    if delta_q < -0.01:
        print("✓ Hypothese A: Glattheit GLÄTTET das Spektrum (q sinkt)")
        print("  → Smooth-Potential wirkt regularisierend")
        print("  → Glattheit unterdrückt Chaos")
    elif delta_q > 0.01:
        print("✓ Hypothese B: Glattheit VERSTÄRKT Chaos (q steigt)")
        print("  → Interferenz zwischen Primzahl- und Smooth-Potential")
        print("  → Zusätzliche Struktur erhöht Komplexität")
    else:
        print("✓ Hypothese C: Glattheit ist ORTHOGONAL (kein Effekt)")
        print("  → Smooth und Primes sind spektral entkoppelt")
        print("  → Nur Energieskala beeinflusst, nicht Statistik")
    
    # Visualisierung
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Level Spacings
    ax = axes[0]
    ax.hist(spacings_without, bins=30, alpha=0.6, label='Ohne Smooth', 
            color='blue', density=True, edgecolor='black')
    ax.hist(spacings_with, bins=30, alpha=0.6, label='Mit Smooth', 
            color='orange', density=True, edgecolor='black')
    ax.set_xlabel('Level Spacing s', fontsize=12)
    ax.set_ylabel('Dichte P(s)', fontsize=12)
    ax.set_title('Level Spacing Verteilung', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Plot 2: Brody-Parameter
    ax = axes[1]
    scenarios = ['Ohne Smooth', 'Mit Smooth']
    q_values = [q_without, q_with]
    colors = ['blue', 'orange']
    
    bars = ax.bar(scenarios, q_values, color=colors, alpha=0.7, edgecolor='black')
    ax.axhline(y=0.0, color='red', linestyle='--', label='Poisson (q=0)')
    ax.axhline(y=1.0, color='green', linestyle='--', label='GUE (q=1)')
    ax.set_ylabel('Brody-Parameter q', fontsize=12)
    ax.set_title('Spektrale Statistik', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Annotiere Werte
    for bar, q in zip(bars, q_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'q = {q:.3f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    # Speichere Plot
    output_dir = Path("figures")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "smooth_effect_demo.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot gespeichert: {output_path}")
    
    plt.show()


def main():
    """Führe alle Demos aus."""
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║        SMOOTH NUMBERS INTEGRATION - Quick Demo                   ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    # Demo 1: Glattheitsdichte
    demo_1_smooth_density()
    
    # Demo 2: Potentiallandschaft
    demo_2_landscape()
    
    # Demo 3: MultiLayerHamiltonian
    demo_3_multilayer_hamiltonian()
    
    # Demo 4: Hauptfrage (mit/ohne Smooth)
    demo_4_comparison()
    
    print("\n" + "="*70)
    print("ALLE DEMOS ABGESCHLOSSEN!")
    print("="*70)
    print("\nGenerierte Dateien:")
    print("  - figures/smooth_landscape_demo.png")
    print("  - figures/smooth_effect_demo.png")
    print("\nNächste Schritte:")
    print("  - Vollständiger Vergleich: python compare_layers.py")
    print("  - Tests ausführen: pytest tests/test_smooth_integration.py -v")
    print("  - Dokumentation: docs/smooth_integration.md")


if __name__ == "__main__":
    main()
