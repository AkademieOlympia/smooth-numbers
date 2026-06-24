#!/usr/bin/env python3
"""
Minimal Ratio-Statistik Test
"""

import numpy as np
import sys
from pathlib import Path

print("START: Minimal Ratio Test", flush=True)

# Füge src zum Path hinzu
sys.path.insert(0, str(Path(__file__).parent))

print("Importiere Module...", flush=True)

try:
    from src.hamiltonian import CollatzEABCHamiltonian
    print("✓ hamiltonian importiert", flush=True)
except Exception as e:
    print(f"✗ Fehler beim Import hamiltonian: {e}", flush=True)
    sys.exit(1)

try:
    from src.level_spacing import compute_level_spacing
    print("✓ level_spacing importiert", flush=True)
except Exception as e:
    print(f"✗ Fehler beim Import level_spacing: {e}", flush=True)
    sys.exit(1)

try:
    from src.spectral import spectral_unfolding
    print("✓ spectral importiert", flush=True)
except Exception as e:
    print(f"✗ Fehler beim Import spectral: {e}", flush=True)
    sys.exit(1)

print("\n" + "="*60, flush=True)
print("MINIMAL RATIO-STATISTIK TEST", flush=True)
print("="*60 + "\n", flush=True)

# Kleine Parameter für schnellen Test
N = 300
K = 100

print(f"System: N = {N}, k = {K}", flush=True)
print("Konstruiere Collatz-Hamiltonian...", flush=True)

try:
    H = CollatzEABCHamiltonian(N=N, gamma=1.5, beta=0.5, alpha=1.0)
    print("✓ Hamiltonian konstruiert", flush=True)
except Exception as e:
    print(f"✗ Fehler: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Berechne Spektrum...", flush=True)

try:
    # Verwende 'SA' (smallest algebraic) statt 'SM' mit sigma - stabiler!
    eigenvalues = H.compute_spectrum(k=K, which='SA')
    print(f"✓ Spektrum berechnet: {len(eigenvalues)} Eigenwerte", flush=True)
    print(f"  E_min = {eigenvalues[0]:.4f}, E_max = {eigenvalues[-1]:.4f}", flush=True)
except Exception as e:
    print(f"✗ Fehler: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Unfolding...", flush=True)

try:
    unfolded = spectral_unfolding(eigenvalues)
    print(f"✓ Unfolding abgeschlossen", flush=True)
except Exception as e:
    print(f"✗ Fehler: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Berechne Level Spacings...", flush=True)

try:
    spacings = compute_level_spacing(unfolded)
    print(f"✓ Level Spacings berechnet: {len(spacings)} Spacings", flush=True)
    print(f"  ⟨s⟩ = {np.mean(spacings):.4f}, σ(s) = {np.std(spacings):.4f}", flush=True)
except Exception as e:
    print(f"✗ Fehler: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("Berechne Ratio-Statistik...", flush=True)

try:
    r_values = []
    for i in range(len(spacings) - 1):
        s_min = min(spacings[i], spacings[i + 1])
        s_max = max(spacings[i], spacings[i + 1])
        
        if s_max > 0:
            r = s_min / s_max
            r_values.append(r)
    
    r_values = np.array(r_values)
    mean_r = np.mean(r_values)
    std_r = np.std(r_values)
    
    print(f"✓ Ratio-Statistik berechnet", flush=True)
    print(f"\n  ⟨r⟩ = {mean_r:.4f} ± {std_r:.4f}", flush=True)
    print(f"\n  Referenzwerte:", flush=True)
    print(f"    Poisson: ⟨r⟩ ≈ 0.386", flush=True)
    print(f"    GOE:     ⟨r⟩ ≈ 0.530", flush=True)
    print(f"    GUE:     ⟨r⟩ ≈ 0.603", flush=True)
    
    # Bewertung
    if 0.52 <= mean_r <= 0.68:
        print(f"\n  ✓✓✓ ⟨r⟩ IM BEREICH [0.52, 0.68]!", flush=True)
        print(f"      → Hinweise auf arithmetische Universalitätsklasse", flush=True)
    elif mean_r < 0.52:
        print(f"\n  → ⟨r⟩ nahe GOE", flush=True)
    elif mean_r > 0.68:
        print(f"\n  → ⟨r⟩ nahe Poisson", flush=True)

except Exception as e:
    print(f"✗ Fehler: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60, flush=True)
print("MINIMAL TEST ABGESCHLOSSEN!", flush=True)
print("="*60, flush=True)
