#!/usr/bin/env python3
"""
Stage 5.5: Wheel-30 Null Hypothesis Test

Tests whether H(Δr) is prime-specific or merely a property of Wheel-30 arithmetic
by comparing:
  - H_Prime:        Real primes
  - H_WheelRandom:  Random thinning of Wheel-30 numbers
  - H_WheelCramér:  Cramér density restricted to Wheel-30

Uses the exact same pipeline: R → A_i(Δr) → H(Δr)
"""

import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict

# Configuration
N = 1_000_000  # Range to test
WHEEL_30 = {1, 7, 11, 13, 17, 19, 23, 29}  # Residues mod 30
DELTA_R_VALUES = [2, 6, 10, 14, 18]  # Focus on Regime I
PROJECTIONS = [2, 4, 6, 8]  # Base offsets for gap-pair projections
NUM_SEEDS = 10  # Number of random realizations

print("=" * 80)
print("STAGE 5.5: WHEEL-30 NULL HYPOTHESIS TEST")
print("=" * 80)
print(f"N = {N:,}")
print(f"Δr values: {DELTA_R_VALUES}")
print(f"Projections (base): {PROJECTIONS}")
print(f"Random seeds: {NUM_SEEDS}")
print()

# ============================================================================
# 1. SEQUENCE GENERATION
# ============================================================================

def sieve_primes(n: int) -> List[int]:
    """Generate primes up to n using Sieve of Eratosthenes."""
    if n < 2:
        return []
    
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
    
    return [i for i in range(2, n + 1) if is_prime[i]]


def generate_wheel30_numbers(n: int) -> List[int]:
    """Generate all Wheel-30 numbers up to n."""
    wheel = []
    for num in range(1, n + 1):
        if num % 30 in WHEEL_30:
            wheel.append(num)
    return wheel


def generate_wheel_random(n: int, target_density: float, seed: int = None) -> List[int]:
    """
    Generate random thinning of Wheel-30 numbers.
    
    Args:
        n: Upper bound
        target_density: Probability of inclusion (e.g., matching prime density)
        seed: Random seed for reproducibility
    """
    if seed is not None:
        np.random.seed(seed)
    
    wheel = generate_wheel30_numbers(n)
    # Random thinning
    selected = []
    for num in wheel:
        if np.random.random() < target_density:
            selected.append(num)
    
    return sorted(selected)


def generate_wheel_cramer(n: int, seed: int = None) -> List[int]:
    """
    Generate Cramér density restricted to Wheel-30.
    
    Uses Cramér probability p(n) = 2/ln(n) for each Wheel-30 number.
    """
    if seed is not None:
        np.random.seed(seed)
    
    wheel = generate_wheel30_numbers(n)
    selected = []
    
    for num in wheel:
        if num < 3:
            continue
        # Cramér probability
        p = 2.0 / np.log(num)
        if np.random.random() < p:
            selected.append(num)
    
    return sorted(selected)


# ============================================================================
# 2. GAP-PAIR ANALYSIS (EXACT PIPELINE FROM C++ CODE)
# ============================================================================

def compute_gaps(sequence: List[int]) -> List[int]:
    """Compute gaps between consecutive numbers."""
    return [sequence[i+1] - sequence[i] for i in range(len(sequence) - 1)]


def compute_gap_transition_counts(gaps: List[int], delta_r: int, 
                                  base_offsets: List[int]) -> Tuple[int, int]:
    """
    Count gap transitions matching/not matching the delta_r criterion.
    
    For each consecutive gap pair (g1, g2):
      - Match:     |g1 % 30 - g2 % 30| == delta_r
      - No-match:  |g1 % 30 - g2 % 30| != delta_r
    
    Only consider gap pairs where both gaps are in base_offsets or base_offsets + delta_r.
    
    Returns:
        (match_count, nomatch_count)
    """
    target_gaps_set = set(base_offsets + [g + delta_r for g in base_offsets])
    
    match_count = 0
    nomatch_count = 0
    
    for i in range(len(gaps) - 1):
        g1, g2 = gaps[i], gaps[i+1]
        
        # Only consider pairs where both gaps are in target set
        if g1 not in target_gaps_set or g2 not in target_gaps_set:
            continue
        
        # Check residue distance
        r1 = g1 % 30
        r2 = g2 % 30
        
        residue_dist = abs(r1 - r2)
        # Handle wrap-around
        residue_dist = min(residue_dist, 30 - residue_dist)
        
        if residue_dist == delta_r:
            match_count += 1
        else:
            nomatch_count += 1
    
    return match_count, nomatch_count


def compute_R_gap(gaps: List[int], delta_r: int, 
                  base_offsets: List[int]) -> float:
    """
    Compute R_gap asymmetry ratio.
    
    R = (match_count) / (nomatch_count)
    """
    match, nomatch = compute_gap_transition_counts(gaps, delta_r, base_offsets)
    
    if nomatch == 0:
        return np.nan
    
    return match / nomatch


def compute_A_for_projection(sequence: List[int], delta_r: int, 
                             base_offsets: List[int],
                             bernoulli_R: float) -> float:
    """
    Compute A(Δr) = R_sequence / R_Bernoulli for a single projection.
    
    Args:
        sequence: The number sequence
        delta_r: Residue distance
        base_offsets: Base gap offsets for this projection
        bernoulli_R: Pre-computed Bernoulli baseline
    
    Returns:
        A(Δr) amplification factor
    """
    gaps = compute_gaps(sequence)
    R_seq = compute_R_gap(gaps, delta_r, base_offsets)
    
    if np.isnan(R_seq) or bernoulli_R == 0:
        return np.nan
    
    return R_seq / bernoulli_R


def compute_H(sequence: List[int], delta_r_values: List[int],
             projections: List[int],
             bernoulli_baselines: Dict[Tuple[int, int], float]) -> Dict[int, float]:
    """
    Compute H(Δr) = mean(A_i(Δr)) across projections.
    
    Args:
        sequence: The number sequence
        delta_r_values: List of Δr values to test
        projections: List of base offsets
        bernoulli_baselines: Pre-computed Bernoulli R values
    
    Returns:
        Dictionary mapping Δr → H(Δr)
    """
    H_values = {}
    
    for delta_r in delta_r_values:
        A_values = []
        
        for base in projections:
            base_offsets = [base, base + 2, base + 4]
            key = (delta_r, base)
            
            if key not in bernoulli_baselines:
                continue
            
            A = compute_A_for_projection(sequence, delta_r, base_offsets, 
                                        bernoulli_baselines[key])
            
            if not np.isnan(A):
                A_values.append(A)
        
        if A_values:
            H_values[delta_r] = np.mean(A_values)
        else:
            H_values[delta_r] = np.nan
    
    return H_values


# ============================================================================
# 3. BERNOULLI BASELINE COMPUTATION
# ============================================================================

def compute_bernoulli_baselines(delta_r_values: List[int], 
                               projections: List[int],
                               num_trials: int = 100,
                               seq_length: int = 100000) -> Dict[Tuple[int, int], float]:
    """
    Compute Bernoulli baseline R values for all (Δr, base) combinations.
    
    Generates random gap sequences with uniform residues mod 30.
    """
    print("Computing Bernoulli baselines...")
    baselines = {}
    
    # Typical gaps in Wheel-30 sequences
    typical_gaps = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
    
    for delta_r in delta_r_values:
        for base in projections:
            base_offsets = [base, base + 2, base + 4]
            
            R_values = []
            for trial in range(num_trials):
                # Generate random gaps
                random_gaps = np.random.choice(typical_gaps, size=seq_length)
                R = compute_R_gap(random_gaps, delta_r, base_offsets)
                
                if not np.isnan(R):
                    R_values.append(R)
            
            if R_values:
                baselines[(delta_r, base)] = np.mean(R_values)
            else:
                baselines[(delta_r, base)] = 1.0  # Fallback
    
    print(f"  Computed {len(baselines)} baseline values")
    return baselines


# ============================================================================
# 4. MAIN EXECUTION
# ============================================================================

print("Step 1: Generating sequences...")
print("-" * 80)

# 1a. Generate primes
print("  Generating primes...")
primes = sieve_primes(N)
print(f"  Found {len(primes):,} primes up to {N:,}")

# 1b. Compute prime density for matching
prime_density = len(primes) / N
print(f"  Prime density: {prime_density:.6f}")

# 1c. Generate Wheel-30 sequences (averaged over multiple seeds)
print(f"  Generating {NUM_SEEDS} Wheel-Random sequences...")
wheel_random_sequences = [
    generate_wheel_random(N, prime_density, seed=i) 
    for i in range(NUM_SEEDS)
]
avg_wheel_random_size = np.mean([len(seq) for seq in wheel_random_sequences])
print(f"  Average Wheel-Random size: {avg_wheel_random_size:,.0f}")

print(f"  Generating {NUM_SEEDS} Wheel-Cramér sequences...")
wheel_cramer_sequences = [
    generate_wheel_cramer(N, seed=i) 
    for i in range(NUM_SEEDS)
]
avg_wheel_cramer_size = np.mean([len(seq) for seq in wheel_cramer_sequences])
print(f"  Average Wheel-Cramér size: {avg_wheel_cramer_size:,.0f}")

print()
print("Step 2: Computing Bernoulli baselines...")
print("-" * 80)
bernoulli_baselines = compute_bernoulli_baselines(DELTA_R_VALUES, PROJECTIONS)
print()

# ============================================================================
# 5. COMPUTE H FOR ALL THREE MODELS
# ============================================================================

print("Step 3: Computing H(Δr) for all models...")
print("-" * 80)

# 3a. H_Prime
print("  Computing H_Prime...")
H_prime = compute_H(primes, DELTA_R_VALUES, PROJECTIONS, bernoulli_baselines)

# 3b. H_WheelRandom (averaged)
print(f"  Computing H_WheelRandom (averaging over {NUM_SEEDS} seeds)...")
H_wheel_random_all = []
for i, seq in enumerate(wheel_random_sequences):
    H = compute_H(seq, DELTA_R_VALUES, PROJECTIONS, bernoulli_baselines)
    H_wheel_random_all.append(H)

# Average across seeds
H_wheel_random = {}
for delta_r in DELTA_R_VALUES:
    values = [H[delta_r] for H in H_wheel_random_all if delta_r in H and not np.isnan(H[delta_r])]
    if values:
        H_wheel_random[delta_r] = np.mean(values)
    else:
        H_wheel_random[delta_r] = np.nan

# 3c. H_WheelCramér (averaged)
print(f"  Computing H_WheelCramér (averaging over {NUM_SEEDS} seeds)...")
H_wheel_cramer_all = []
for i, seq in enumerate(wheel_cramer_sequences):
    H = compute_H(seq, DELTA_R_VALUES, PROJECTIONS, bernoulli_baselines)
    H_wheel_cramer_all.append(H)

# Average across seeds
H_wheel_cramer = {}
for delta_r in DELTA_R_VALUES:
    values = [H[delta_r] for H in H_wheel_cramer_all if delta_r in H and not np.isnan(H[delta_r])]
    if values:
        H_wheel_cramer[delta_r] = np.mean(values)
    else:
        H_wheel_cramer[delta_r] = np.nan

print()

# ============================================================================
# 6. RESULTS & COMPARISON
# ============================================================================

print("=" * 80)
print("RESULTS: H(Δr) COMPARISON")
print("=" * 80)
print()
print(f"{'Δr':<8} {'H_Prime':<12} {'H_WheelRand':<12} {'H_WheelCramér':<12}")
print("-" * 48)

for delta_r in DELTA_R_VALUES:
    hp = H_prime.get(delta_r, np.nan)
    hwr = H_wheel_random.get(delta_r, np.nan)
    hwc = H_wheel_cramer.get(delta_r, np.nan)
    
    print(f"{delta_r:<8} {hp:<12.4f} {hwr:<12.4f} {hwc:<12.4f}")

print()
print("=" * 80)
print("STATISTICAL COMPARISON")
print("=" * 80)

# Compute correlations
H_prime_vals = [H_prime.get(dr, np.nan) for dr in DELTA_R_VALUES]
H_wr_vals = [H_wheel_random.get(dr, np.nan) for dr in DELTA_R_VALUES]
H_wc_vals = [H_wheel_cramer.get(dr, np.nan) for dr in DELTA_R_VALUES]

# Remove NaN values for correlation
valid_indices = [i for i in range(len(DELTA_R_VALUES)) 
                if not np.isnan(H_prime_vals[i]) 
                and not np.isnan(H_wr_vals[i]) 
                and not np.isnan(H_wc_vals[i])]

if valid_indices:
    hp_clean = [H_prime_vals[i] for i in valid_indices]
    hwr_clean = [H_wr_vals[i] for i in valid_indices]
    hwc_clean = [H_wc_vals[i] for i in valid_indices]
    
    corr_prime_wr = np.corrcoef(hp_clean, hwr_clean)[0, 1]
    corr_prime_wc = np.corrcoef(hp_clean, hwc_clean)[0, 1]
    
    print(f"Correlation H_Prime vs H_WheelRandom:  ρ = {corr_prime_wr:.4f}")
    print(f"Correlation H_Prime vs H_WheelCramér:  ρ = {corr_prime_wc:.4f}")
    print()
    
    # Mean absolute differences
    mad_wr = np.mean(np.abs(np.array(hp_clean) - np.array(hwr_clean)))
    mad_wc = np.mean(np.abs(np.array(hp_clean) - np.array(hwc_clean)))
    
    print(f"Mean absolute difference (Prime vs WheelRandom): {mad_wr:.4f}")
    print(f"Mean absolute difference (Prime vs WheelCramér): {mad_wc:.4f}")
    print()

# ============================================================================
# 7. INTERPRETATION
# ============================================================================

print("=" * 80)
print("INTERPRETATION")
print("=" * 80)
print()

if valid_indices:
    threshold_high = 0.9
    threshold_low = 0.3
    
    if corr_prime_wr > threshold_high or corr_prime_wc > threshold_high:
        print("⚠️  HIGH CORRELATION DETECTED")
        print()
        print("Result: H_Prime ≈ H_Wheel")
        print()
        print("Interpretation:")
        print("  H(Δr) appears to be primarily a property of Wheel-30 arithmetic")
        print("  rather than a prime-specific phenomenon.")
        print()
        print("Implication:")
        print("  The observable characterizes Wheel-30 residue-class structure.")
        print("  Not prime-number-theoretic in the narrow sense.")
        print()
    elif corr_prime_wr < threshold_low and corr_prime_wc < threshold_low:
        print("✓  LOW CORRELATION DETECTED")
        print()
        print("Result: H_Prime ≠ H_Wheel")
        print()
        print("Interpretation:")
        print("  H(Δr) contains information beyond Wheel-30 structure.")
        print("  Prime-specific signal remains after Wheel elimination.")
        print()
        print("Implication:")
        print("  After elimination of Bernoulli, Cramér, projection-dependence,")
        print("  HL k=2, and Wheel-30, a prime-specific residual remains.")
        print()
        print("Next steps:")
        print("  - Test Hardy-Littlewood k-tuple models (k≥3)")
        print("  - Investigate residue-class-specific HL theory")
        print()
    else:
        print("⚡ INTERMEDIATE CORRELATION")
        print()
        print("Result: Ambiguous")
        print()
        print("Interpretation:")
        print("  H(Δr) shows partial similarity to Wheel-30 structure.")
        print("  May contain both Wheel and prime-specific components.")
        print()
        print("Recommendation:")
        print("  - Increase N for better statistics")
        print("  - Analyze per-Δr differences more carefully")
        print("  - Consider mixed models")
        print()

print("=" * 80)
print("STAGE 5.5 COMPLETE")
print("=" * 80)

# ============================================================================
# 8. VISUALIZATION
# ============================================================================

print()
print("Generating visualization...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: H(Δr) comparison
ax1.plot(DELTA_R_VALUES, [H_prime.get(dr, np.nan) for dr in DELTA_R_VALUES], 
         'o-', label='H_Prime', linewidth=2, markersize=8)
ax1.plot(DELTA_R_VALUES, [H_wheel_random.get(dr, np.nan) for dr in DELTA_R_VALUES], 
         's-', label='H_WheelRandom', linewidth=2, markersize=8, alpha=0.7)
ax1.plot(DELTA_R_VALUES, [H_wheel_cramer.get(dr, np.nan) for dr in DELTA_R_VALUES], 
         '^-', label='H_WheelCramér', linewidth=2, markersize=8, alpha=0.7)

ax1.set_xlabel('Δr', fontsize=12)
ax1.set_ylabel('H(Δr)', fontsize=12)
ax1.set_title('Stage 5.5: H(Δr) Comparison', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Plot 2: Scatter comparison
if valid_indices:
    ax2.scatter(hp_clean, hwr_clean, s=100, alpha=0.6, label='WheelRandom')
    ax2.scatter(hp_clean, hwc_clean, s=100, alpha=0.6, label='WheelCramér', marker='s')
    
    # Diagonal line
    min_val = min(min(hp_clean), min(hwr_clean + hwc_clean))
    max_val = max(max(hp_clean), max(hwr_clean + hwc_clean))
    ax2.plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, label='y=x')
    
    ax2.set_xlabel('H_Prime(Δr)', fontsize=12)
    ax2.set_ylabel('H_Wheel(Δr)', fontsize=12)
    ax2.set_title('Scatter: Prime vs. Wheel', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('stage5_5_wheel30_comparison.png', dpi=150, bbox_inches='tight')
print(f"Saved: stage5_5_wheel30_comparison.png")

print()
print("Stage 5.5 analysis complete!")
print()
