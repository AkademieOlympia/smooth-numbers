#!/usr/bin/env python3
"""
Schnelltest für Collatz-Integration

Minimales Testskript, um zu verifizieren, dass die Collatz-Erweiterung korrekt funktioniert.
"""

import numpy as np
from src import CollatzEABCHamiltonian, EABCHamiltonian
from src.level_spacing import compute_level_spacing

print("="*70)
print("COLLATZ-EABC-QUBIT SCHNELLTEST")
print("="*70)

# Parameter
N = 500
gamma = 1.5
k = 200

print(f"\nParameter: N = {N}, γ = {gamma}, k = {k} Eigenwerte\n")

# Test 1: Standard-EABC
print("[1/3] Standard-EABC Hamiltonian (uniform)")
print("-"*70)
H_uniform = EABCHamiltonian(N=N, gamma=gamma)
E_uniform = H_uniform.compute_spectrum(k=k, which='SM')
s_uniform = compute_level_spacing(E_uniform)

print(f"Spektrum: E ∈ [{E_uniform.min():.4f}, {E_uniform.max():.4f}]")
print(f"Level Spacing: ⟨s⟩ = {np.mean(s_uniform):.4f}, σ = {np.std(s_uniform):.4f}")

# Test 2: Collatz-gewichtet
print("\n[2/3] Collatz-gewichteter Hamiltonian")
print("-"*70)
H_collatz = CollatzEABCHamiltonian(N=N, gamma=gamma, use_random_soup=False)
E_collatz = H_collatz.compute_spectrum(k=k, which='SM')
s_collatz = compute_level_spacing(E_collatz)

print(f"Spektrum: E ∈ [{E_collatz.min():.4f}, {E_collatz.max():.4f}]")
print(f"Level Spacing: ⟨s⟩ = {np.mean(s_collatz):.4f}, σ = {np.std(s_collatz):.4f}")

# Test 3: Random Soup
print("\n[3/3] Random Soup Kontrolle")
print("-"*70)
H_soup = CollatzEABCHamiltonian(N=N, gamma=gamma, use_random_soup=True, random_seed=42)
E_soup = H_soup.compute_spectrum(k=k, which='SM')
s_soup = compute_level_spacing(E_soup)

print(f"Spektrum: E ∈ [{E_soup.min():.4f}, {E_soup.max():.4f}]")
print(f"Level Spacing: ⟨s⟩ = {np.mean(s_soup):.4f}, σ = {np.std(s_soup):.4f}")

# Vergleich
print("\n" + "="*70)
print("VERGLEICH")
print("="*70)
delta_uniform_collatz = np.abs(E_uniform - E_collatz)
delta_uniform_soup = np.abs(E_uniform - E_soup)

print(f"Δ(Uniform, Collatz): Max = {delta_uniform_collatz.max():.6f}, Mean = {delta_uniform_collatz.mean():.6f}")
print(f"Δ(Uniform, Soup):    Max = {delta_uniform_soup.max():.6f}, Mean = {delta_uniform_soup.mean():.6f}")

print("\nCollatz-Gewichte Statistik:")
print(f"  Mittelwert: {np.mean(H_collatz.collatz_weights):+.6f}")
print(f"  Std.-Abw.:  {np.std(H_collatz.collatz_weights):.6f}")
print(f"  Min/Max:    [{np.min(H_collatz.collatz_weights):+.4f}, {np.max(H_collatz.collatz_weights):+.4f}]")

print("\n" + "="*70)
print("✓ Schnelltest erfolgreich abgeschlossen!")
print("="*70)
print("\nFür umfassende Tests und Visualisierung:")
print("  → python demo_collatz.py")
print("  → python -m pytest tests/test_collatz_weights.py -v")
print("="*70)
