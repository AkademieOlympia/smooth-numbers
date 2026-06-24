"""
Detaillierte Gegenüberstellung: Herkömmliche Faktorisierung vs. EABC/Catalan-Parameter
für n = 1 bis 100.

Berechnet:
- Primfaktorzerlegung
- Ω(n) = Anzahl Primfaktoren mit Vielfachheit
- EABC-Klassifikation der Primfaktoren
- Schale S(n) = v₂(n) + v₃(n)
- EABC-Vektor v(n) = (n_E, n_A, n_B, n_C)
- Konzentration H(n) = ||v||²/Ω²
- Catalan-Zahl C_{Ω(n)-1}
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter
from typing import List, Tuple

from utils.eabc import (
    prime_factors_with_multiplicity,
    count_prime_factors,
    padicval,
    eabc_class,
    compute_eabc_vector,
    compute_H
)


def catalan_number(n: int) -> int:
    """
    Berechnet die n-te Catalan-Zahl C_n = (2n)! / ((n+1)! n!)
    
    Verwende dynamische Programmierung für Effizienz.
    C_n = Anzahl der Faktorisierungsbäume mit n+1 Blättern.
    """
    if n < 0:
        return 0
    if n <= 1:
        return 1
    
    # Binomialkoeffizient verwenden: C_n = C(2n, n) / (n+1)
    from math import comb
    return comb(2*n, n) // (n + 1)


def format_factorization(n: int) -> str:
    """
    Formatiert Faktorisierung als String, z.B. "2³·3·5"
    """
    if n == 1:
        return "1"
    
    factors = prime_factors_with_multiplicity(n)
    if not factors:
        return str(n)
    
    # Zähle Vielfachheiten
    factor_counts = Counter(factors)
    
    # Sortiere nach Primzahl
    sorted_primes = sorted(factor_counts.keys())
    
    # Formatiere
    parts = []
    for p in sorted_primes:
        count = factor_counts[p]
        if count == 1:
            parts.append(str(p))
        else:
            # Unicode-Exponenten
            exp_str = str(count).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))
            parts.append(f"{p}{exp_str}")
    
    return "·".join(parts)


def get_eabc_signature(n: int) -> str:
    """
    Erstellt EABC-Signatur als String, z.B. "EEAB" für die Klassen
    der Primfaktoren (mit Vielfachheit, inkl. 2 und 3).
    
    Für 2 und 3 verwenden wir 'E' (wie in der Aufgabenstellung).
    """
    if n == 1:
        return ""
    
    factors = prime_factors_with_multiplicity(n)
    signature = []
    
    for p in factors:
        if p == 2 or p == 3:
            signature.append('E')  # Laut Aufgabe: 2 und 3 sind Klasse E
        else:
            cls = eabc_class(p)
            if cls in ['E', 'A', 'B', 'C']:
                signature.append(cls)
            else:
                signature.append('?')
    
    return "".join(signature)


def compute_all_data(n_max: int = 100) -> pd.DataFrame:
    """
    Berechnet alle Daten für n = 1 bis n_max.
    """
    data = []
    
    for n in range(1, n_max + 1):
        # Basiswerte
        factorization = format_factorization(n)
        omega = count_prime_factors(n)
        
        # Shell-Werte
        v2 = padicval(n, 2)
        v3 = padicval(n, 3)
        shell = v2 + v3
        
        # EABC-Vektor
        v = compute_eabc_vector(n)
        eabc_sig = get_eabc_signature(n)
        
        # Konzentration
        H = compute_H(n)
        
        # Catalan-Zahl
        if omega > 0:
            catalan = catalan_number(omega - 1)
        else:
            catalan = 0
        
        data.append({
            'n': n,
            'factorization': factorization,
            'omega': omega,
            'eabc_signature': eabc_sig,
            'shell': shell,
            'v_E': int(v[0]),
            'v_A': int(v[1]),
            'v_B': int(v[2]),
            'v_C': int(v[3]),
            'H': H,
            'catalan': catalan
        })
    
    df = pd.DataFrame(data)
    return df


def create_visualizations(df: pd.DataFrame, output_file: str):
    """
    Erstellt Visualisierungen der Daten.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    fig.suptitle('EABC/Catalan-Parameter für n = 1..100', fontsize=16, fontweight='bold')
    
    # 1. Scatter: H(n) vs. n (farbcodiert nach Ω)
    ax1 = axes[0, 0]
    
    # Nur Werte mit gültigem H
    df_valid_H = df[df['H'].notna()].copy()
    
    # Farbkodierung nach Ω
    omega_values = sorted(df_valid_H['omega'].unique())
    colors = plt.cm.viridis(np.linspace(0, 1, len(omega_values)))
    omega_to_color = dict(zip(omega_values, colors))
    
    for omega in omega_values:
        subset = df_valid_H[df_valid_H['omega'] == omega]
        ax1.scatter(subset['n'], subset['H'], 
                   c=[omega_to_color[omega]], 
                   label=f'Ω={omega}',
                   alpha=0.7, s=50)
    
    ax1.set_xlabel('n', fontsize=12)
    ax1.set_ylabel('H(n) - Konzentration', fontsize=12)
    ax1.set_title('Konzentration H(n) vs. n', fontsize=13, fontweight='bold')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0.25, color='red', linestyle='--', alpha=0.5, label='Min (gleichverteilt)')
    ax1.axhline(y=1.0, color='green', linestyle='--', alpha=0.5, label='Max (konzentriert)')
    
    # 2. Histogram: Verteilung der EABC-Signaturen
    ax2 = axes[0, 1]
    
    # Zähle Signaturen (nur nicht-leere)
    sig_counts = df[df['eabc_signature'] != '']['eabc_signature'].value_counts()
    
    # Top 20 Signaturen
    top_sigs = sig_counts.head(20)
    
    ax2.barh(range(len(top_sigs)), top_sigs.values, color='steelblue')
    ax2.set_yticks(range(len(top_sigs)))
    ax2.set_yticklabels(top_sigs.index, fontsize=9)
    ax2.set_xlabel('Anzahl', fontsize=12)
    ax2.set_title('Top 20 EABC-Signaturen', fontsize=13, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    ax2.invert_yaxis()
    
    # 3. Scatter: S(n) vs. Ω(n)
    ax3 = axes[1, 0]
    
    # Gruppiere nach (shell, omega) und zähle
    shell_omega_counts = df.groupby(['shell', 'omega']).size().reset_index(name='count')
    
    scatter = ax3.scatter(shell_omega_counts['omega'], 
                         shell_omega_counts['shell'],
                         s=shell_omega_counts['count'] * 50,
                         c=shell_omega_counts['count'],
                         cmap='YlOrRd',
                         alpha=0.6,
                         edgecolors='black',
                         linewidth=0.5)
    
    ax3.set_xlabel('Ω(n) - Anzahl Primfaktoren', fontsize=12)
    ax3.set_ylabel('S(n) = v₂(n) + v₃(n) - Schale', fontsize=12)
    ax3.set_title('Schale vs. Primfaktoranzahl', fontsize=13, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Anzahl Zahlen', fontsize=10)
    
    # 4. Log-Plot: Catalan-Zahlen
    ax4 = axes[1, 1]
    
    # Gruppiere nach Ω und nimm ersten Wert der Catalan-Zahl
    omega_catalan = df[df['omega'] > 0].groupby('omega')['catalan'].first().reset_index()
    
    ax4.semilogy(omega_catalan['omega'], omega_catalan['catalan'], 
                'o-', color='darkgreen', linewidth=2, markersize=8)
    ax4.set_xlabel('Ω(n) - Anzahl Primfaktoren', fontsize=12)
    ax4.set_ylabel('C_{Ω-1} - Catalan-Zahl', fontsize=12)
    ax4.set_title('Zustandsraum: Catalan-Zahlen (log)', fontsize=13, fontweight='bold')
    ax4.grid(True, alpha=0.3, which='both')
    
    # Annotiere einige Werte
    for _, row in omega_catalan.iterrows():
        if row['omega'] <= 8:  # Nur bis Ω=8 annotieren
            ax4.annotate(f"{int(row['catalan'])}", 
                        xy=(row['omega'], row['catalan']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=8, alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Visualisierungen gespeichert: {output_file}")
    plt.close()


def find_interesting_examples(df: pd.DataFrame) -> dict:
    """
    Findet interessante Beispiele in den Daten.
    """
    examples = {}
    
    # Nur Zahlen mit gültigem H
    df_valid = df[df['H'].notna()].copy()
    
    # Hohe Konzentration (H ≈ 1)
    df_sorted_high_H = df_valid.sort_values('H', ascending=False)
    examples['high_concentration'] = df_sorted_high_H.head(10)
    
    # Niedrige Konzentration (H ≈ 0.25)
    df_sorted_low_H = df_valid.sort_values('H', ascending=True)
    examples['low_concentration'] = df_sorted_low_H.head(10)
    
    # Hohe Shell-Werte
    df_sorted_shell = df.sort_values('shell', ascending=False)
    examples['high_shell'] = df_sorted_shell.head(10)
    
    # Hohe Ω-Werte
    df_sorted_omega = df.sort_values('omega', ascending=False)
    examples['high_omega'] = df_sorted_omega.head(10)
    
    # Interessante EABC-Signaturen (lange, vielfältige)
    df['sig_length'] = df['eabc_signature'].str.len()
    df['sig_diversity'] = df['eabc_signature'].apply(lambda s: len(set(s)) if s else 0)
    df_sorted_sig = df.sort_values(['sig_diversity', 'sig_length'], ascending=False)
    examples['diverse_signatures'] = df_sorted_sig.head(10)
    
    return examples


def save_examples_markdown(examples: dict, output_file: str, df: pd.DataFrame):
    """
    Speichert interessante Beispiele als Markdown-Datei.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Interessante Beispiele: EABC/Catalan-Parameter (n = 1..100)\n\n")
        f.write("Automatisch generiert durch `comparison_n1_100.py`\n\n")
        f.write("---\n\n")
        
        # 1. Hohe Konzentration
        f.write("## 1. Hohe Konzentration H(n) ≈ 1\n\n")
        f.write("Zahlen, bei denen alle EABC-Faktoren (fast) zur selben Klasse gehören.\n\n")
        f.write("| n | Faktorisierung | Ω | EABC-Sig | v(n) | H(n) |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for _, row in examples['high_concentration'].iterrows():
            v_str = f"({row['v_E']},{row['v_A']},{row['v_B']},{row['v_C']})"
            f.write(f"| {row['n']} | {row['factorization']} | {row['omega']} | "
                   f"{row['eabc_signature']} | {v_str} | {row['H']:.4f} |\n")
        
        f.write("\n")
        
        # 2. Niedrige Konzentration
        f.write("## 2. Niedrige Konzentration H(n) ≈ 0.25\n\n")
        f.write("Zahlen mit gleichverteilten EABC-Faktoren über alle vier Klassen.\n\n")
        f.write("| n | Faktorisierung | Ω | EABC-Sig | v(n) | H(n) |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for _, row in examples['low_concentration'].iterrows():
            v_str = f"({row['v_E']},{row['v_A']},{row['v_B']},{row['v_C']})"
            f.write(f"| {row['n']} | {row['factorization']} | {row['omega']} | "
                   f"{row['eabc_signature']} | {v_str} | {row['H']:.4f} |\n")
        
        f.write("\n")
        
        # 3. Hohe Shell-Werte
        f.write("## 3. Hohe Shell-Werte S(n) = v₂(n) + v₃(n)\n\n")
        f.write("Zahlen mit vielen Faktoren 2 und 3 (smooth numbers).\n\n")
        f.write("| n | Faktorisierung | S(n) | v₂ | v₃ | Ω |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for _, row in examples['high_shell'].iterrows():
            v2 = padicval(row['n'], 2)
            v3 = padicval(row['n'], 3)
            f.write(f"| {row['n']} | {row['factorization']} | {row['shell']} | "
                   f"{v2} | {v3} | {row['omega']} |\n")
        
        f.write("\n")
        
        # 4. Hohe Ω-Werte
        f.write("## 4. Hohe Primfaktoranzahl Ω(n)\n\n")
        f.write("Zahlen mit vielen Primfaktoren (mit Vielfachheit).\n\n")
        f.write("| n | Faktorisierung | Ω(n) | C_{Ω-1} | EABC-Sig |\n")
        f.write("|---|---|---|---|---|\n")
        
        for _, row in examples['high_omega'].iterrows():
            f.write(f"| {row['n']} | {row['factorization']} | {row['omega']} | "
                   f"{row['catalan']:,} | {row['eabc_signature']} |\n")
        
        f.write("\n")
        
        # 5. Vielfältige EABC-Signaturen
        f.write("## 5. Vielfältige EABC-Signaturen\n\n")
        f.write("Zahlen mit langen, vielfältigen EABC-Signaturen (viele verschiedene Klassen).\n\n")
        f.write("| n | Faktorisierung | EABC-Sig | Vielfalt | v(n) | H(n) |\n")
        f.write("|---|---|---|---|---|---|\n")
        
        for _, row in examples['diverse_signatures'].iterrows():
            v_str = f"({row['v_E']},{row['v_A']},{row['v_B']},{row['v_C']})"
            diversity = len(set(row['eabc_signature']))
            h_val = row['H'] if not pd.isna(row['H']) else 'N/A'
            h_str = f"{h_val:.4f}" if isinstance(h_val, (int, float)) else h_val
            f.write(f"| {row['n']} | {row['factorization']} | {row['eabc_signature']} | "
                   f"{diversity}/4 | {v_str} | {h_str} |\n")
        
        f.write("\n---\n\n")
        
        # Statistiken
        f.write("## Statistiken\n\n")
        
        df_valid = df[df['H'].notna()]
        f.write(f"- **Anzahl Zahlen mit H definiert:** {len(df_valid)}/100\n")
        f.write(f"- **Durchschnitt H(n):** {df_valid['H'].mean():.4f}\n")
        f.write(f"- **Median H(n):** {df_valid['H'].median():.4f}\n")
        f.write(f"- **Min H(n):** {df_valid['H'].min():.4f} (n={df_valid.loc[df_valid['H'].idxmin(), 'n']})\n")
        f.write(f"- **Max H(n):** {df_valid['H'].max():.4f} (mehrere Zahlen)\n")
        f.write(f"- **Durchschnitt Ω(n):** {df['omega'].mean():.2f}\n")
        f.write(f"- **Max Ω(n):** {df['omega'].max()} (n={df.loc[df['omega'].idxmax(), 'n']})\n")
        f.write(f"- **Durchschnitt S(n):** {df['shell'].mean():.2f}\n")
        f.write(f"- **Max S(n):** {df['shell'].max()} (n={df.loc[df['shell'].idxmax(), 'n']})\n")
        
        # EABC-Signatur-Statistiken
        sig_counts = df[df['eabc_signature'] != '']['eabc_signature'].value_counts()
        f.write(f"- **Anzahl verschiedener EABC-Signaturen:** {len(sig_counts)}\n")
        f.write(f"- **Häufigste Signatur:** '{sig_counts.index[0]}' ({sig_counts.values[0]}×)\n")
        
    print(f"✓ Beispiele gespeichert: {output_file}")


def main():
    """
    Hauptfunktion: Berechnet Daten, erstellt Tabelle, Visualisierungen und Beispiele.
    """
    print("=" * 60)
    print("EABC/Catalan-Parameter: Gegenüberstellung n = 1..100")
    print("=" * 60)
    print()
    
    # Erstelle Output-Verzeichnis
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                              'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Berechne alle Daten
    print("Berechne Daten für n = 1..100...")
    df = compute_all_data(n_max=100)
    print(f"✓ {len(df)} Zahlen berechnet")
    print()
    
    # 2. Speichere Tabelle als CSV
    csv_file = os.path.join(output_dir, 'comparison_n1_100.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"✓ Tabelle gespeichert: {csv_file}")
    print()
    
    # 3. Erstelle Visualisierungen
    plot_file = os.path.join(output_dir, 'comparison_plots.png')
    print("Erstelle Visualisierungen...")
    create_visualizations(df, plot_file)
    print()
    
    # 4. Finde und speichere interessante Beispiele
    print("Analysiere interessante Beispiele...")
    examples = find_interesting_examples(df)
    examples_file = os.path.join(output_dir, 'COMPARISON_EXAMPLES.md')
    save_examples_markdown(examples, examples_file, df)
    print()
    
    # 5. Zeige Vorschau der ersten 20 Zeilen
    print("=" * 60)
    print("Vorschau: Erste 20 Zeilen")
    print("=" * 60)
    print()
    
    # Formatiere für bessere Lesbarkeit
    df_preview = df.head(20).copy()
    df_preview['v(n)'] = df_preview.apply(
        lambda row: f"({row['v_E']},{row['v_A']},{row['v_B']},{row['v_C']})", axis=1
    )
    
    cols_to_show = ['n', 'factorization', 'omega', 'eabc_signature', 'shell', 'v(n)', 'H', 'catalan']
    print(df_preview[cols_to_show].to_string(index=False))
    print()
    
    print("=" * 60)
    print("Fertig!")
    print("=" * 60)
    print()
    print(f"Dateien erstellt:")
    print(f"  - {csv_file}")
    print(f"  - {plot_file}")
    print(f"  - {examples_file}")
    print()


if __name__ == "__main__":
    main()
