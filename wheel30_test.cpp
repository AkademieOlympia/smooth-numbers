// Stage 5.5: Wheel-30 Null Hypothesis Test
// ==========================================
//
// CRITICAL TEST: Is H(Δr) prime-specific or just Wheel-30 structure?
//
// Test question:
//   H_Prime(Δr) ≈? H_Wheel-30(Δr) for Δr ≤ 18
//
// Three models compared:
//   1. H_Prime        : Real primes
//   2. H_WheelRandom  : Random thinning of Wheel-30 numbers
//   3. H_WheelCramér  : Cramér with density 2/ln(n), restricted to Wheel-30
//
// Same pipeline applied to all:
//   Sequence → Gap-Transitions → A_i(Δr) → H(Δr)
//
// Decision matrix:
//   H_Prime ≈ H_WheelRandom      → Wheel structure explains core
//   H_Prime ≈ H_WheelCramér ≠ H_WheelRandom → log-density + Wheel explains core
//   H_Prime ≠ both               → Prime-specific correlation remains

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <random>
#include <algorithm>
#include <iomanip>

using namespace std;

// Wheel-30 residues (coprime to 30 = 2·3·5)
const vector<int> WHEEL_RESIDUES = {1, 7, 11, 13, 17, 19, 23, 29};

// Sieve of Eratosthenes
vector<long long> sieve_primes(long long N) {
    vector<bool> is_prime(N + 1, true);
    is_prime[0] = is_prime[1] = false;
    
    for (long long i = 2; i * i <= N; ++i) {
        if (is_prime[i]) {
            for (long long j = i * i; j <= N; j += i) {
                is_prime[j] = false;
            }
        }
    }
    
    vector<long long> primes;
    for (long long i = 2; i <= N; ++i) {
        if (is_prime[i]) primes.push_back(i);
    }
    return primes;
}

// Generate Wheel-30 numbers (all n ≡ wheel residues mod 30)
vector<long long> generate_wheel30_numbers(long long N) {
    vector<long long> wheel_nums;
    for (long long n = 1; n <= N; ++n) {
        int res = n % 30;
        if (find(WHEEL_RESIDUES.begin(), WHEEL_RESIDUES.end(), res) != WHEEL_RESIDUES.end()) {
            wheel_nums.push_back(n);
        }
    }
    return wheel_nums;
}

// Thin Wheel-30 numbers randomly with density matching primes
vector<long long> generate_wheel_random(long long N, double target_density, mt19937& rng) {
    vector<long long> wheel_nums = generate_wheel30_numbers(N);
    vector<long long> result;
    
    uniform_real_distribution<double> dist(0.0, 1.0);
    
    for (long long n : wheel_nums) {
        double p = target_density; // Simplified: constant density
        if (dist(rng) < p) {
            result.push_back(n);
        }
    }
    
    return result;
}

// Cramér model: random with density 2/ln(n), restricted to Wheel-30
vector<long long> generate_wheel_cramer(long long N, int seed) {
    mt19937 rng(seed);
    uniform_real_distribution<double> dist(0.0, 1.0);
    
    vector<long long> wheel_nums = generate_wheel30_numbers(N);
    vector<long long> result;
    
    for (long long n : wheel_nums) {
        if (n < 2) continue;
        double p = 2.0 / log(n);
        if (dist(rng) < p) {
            result.push_back(n);
        }
    }
    
    return result;
}

// Gap transition analysis (GAP-BASED, not residue-to-residue)
struct GapTransitions {
    map<int, map<int, long long>> transitions;  // [from_class][gap_mod_30] -> count
    map<int, long long> class_counts;
    
    double compute_ratio(const vector<int>& low_gaps, const vector<int>& high_gaps) const {
        long long low_count = 0, high_count = 0;
        
        // Sum over all from_classes
        for (auto& [from_class, gap_map] : transitions) {
            for (int g : low_gaps) {
                auto it = gap_map.find(g);
                if (it != gap_map.end()) low_count += it->second;
            }
            for (int g : high_gaps) {
                auto it = gap_map.find(g);
                if (it != gap_map.end()) high_count += it->second;
            }
        }
        
        if (high_count == 0) return 1.0;
        return static_cast<double>(low_count) / high_count;
    }
    
    double compute_geometric_mean_ratio(const vector<int>& low_gaps, const vector<int>& high_gaps) const {
        vector<int> classes = {1, 7, 11, 13, 17, 19, 23, 29};
        double product = 1.0;
        int count = 0;
        
        for (int cls : classes) {
            auto it = class_counts.find(cls);
            if (it == class_counts.end() || it->second < 10) continue;
            
            long long low_count = 0, high_count = 0;
            
            auto trans_it = transitions.find(cls);
            if (trans_it != transitions.end()) {
                for (int g : low_gaps) {
                    auto git = trans_it->second.find(g);
                    if (git != trans_it->second.end()) low_count += git->second;
                }
                for (int g : high_gaps) {
                    auto git = trans_it->second.find(g);
                    if (git != trans_it->second.end()) high_count += git->second;
                }
            }
            
            if (high_count > 0) {
                double ratio = static_cast<double>(low_count) / high_count;
                if (ratio > 0) {
                    product *= ratio;
                    count++;
                }
            }
        }
        
        if (count == 0) return 1.0;
        return pow(product, 1.0 / count);
    }
};

// Analyze gap transitions for a sequence
GapTransitions analyze_transitions(const vector<long long>& sequence) {
    GapTransitions trans;
    
    for (size_t i = 1; i < sequence.size(); ++i) {
        long long p1 = sequence[i-1];
        long long p2 = sequence[i];
        
        if (p1 <= 5 || p2 <= 5) continue;
        
        int from_class = p1 % 30;
        int gap = (p2 - p1) % 30;
        
        trans.transitions[from_class][gap]++;
        trans.class_counts[from_class]++;
    }
    
    return trans;
}

// Generate gap-pairs for given Δr (EXACT COPY from phase_diagram_delta_r.cpp)
struct GapPair {
    vector<int> low;
    vector<int> high;
};

vector<GapPair> generate_gap_pairs_for_delta_r(int delta_r) {
    vector<GapPair> pairs;
    
    // For each possible starting gap offset, create pairs separated by delta_r
    for (int offset = 2; offset <= 10; offset += 2) {
        GapPair pair;
        
        // Low gaps: around offset
        pair.low.push_back(offset % 30);
        if (offset + 2 <= 30) pair.low.push_back((offset + 2) % 30);
        
        // High gaps: offset + delta_r
        int high_base = (offset + delta_r) % 30;
        pair.high.push_back(high_base);
        if (high_base + 2 <= 30) pair.high.push_back((high_base + 2) % 30);
        
        // Only add if we have valid gaps
        if (!pair.low.empty() && !pair.high.empty()) {
            pairs.push_back(pair);
        }
    }
    
    return pairs;
}

// Extract H(Δr) - geometric mean ratio (EXACT COPY from phase_diagram_delta_r.cpp)
double extract_H(const vector<long long>& sequence, int delta_r) {
    auto gap_pairs = generate_gap_pairs_for_delta_r(delta_r);
    GapTransitions trans = analyze_transitions(sequence);
    
    // Average over all gap pairs
    vector<double> ratios;
    for (const auto& pair : gap_pairs) {
        double r = trans.compute_geometric_mean_ratio(pair.low, pair.high);
        if (r > 0) ratios.push_back(r);
    }
    
    if (ratios.empty()) return 1.0;
    
    // Geometric mean of ratios
    double product = 1.0;
    for (double r : ratios) product *= r;
    return pow(product, 1.0 / ratios.size());
}

// Main comparison
int main(int argc, char* argv[]) {
    long long N = 1000000;  // Default
    int num_seeds = 5;      // For averaging random models
    
    if (argc > 1) N = atoll(argv[1]);
    if (argc > 2) num_seeds = atoi(argv[2]);
    
    cout << "========================================" << endl;
    cout << "STAGE 5.5: WHEEL-30 NULL HYPOTHESIS TEST" << endl;
    cout << "========================================" << endl;
    cout << endl;
    cout << "N = " << N << endl;
    cout << "Seeds for random models: " << num_seeds << endl;
    cout << endl;
    
    // Test parameters
    vector<int> delta_r_values = {2, 6, 10, 14, 18};
    
    // Generate real primes
    cout << "Generating real primes..." << flush;
    vector<long long> primes = sieve_primes(N);
    cout << " done. Found " << primes.size() << " primes." << endl;
    cout << endl;
    
    // Compute H_Prime
    map<int, double> H_prime;
    cout << "Computing H_Prime(Δr)..." << endl;
    for (int dr : delta_r_values) {
        H_prime[dr] = extract_H(primes, dr);
        cout << "  Δr=" << dr << ": H_Prime = " << fixed << setprecision(4) << H_prime[dr] << endl;
    }
    cout << endl;
    
    // Compute H_WheelRandom (averaged over seeds)
    map<int, double> H_wheel_random;
    map<int, double> H_wheel_random_std;
    
    cout << "Computing H_WheelRandom(Δr)..." << endl;
    double prime_density = static_cast<double>(primes.size()) / N;
    
    for (int dr : delta_r_values) {
        vector<double> values;
        for (int seed = 0; seed < num_seeds; ++seed) {
            mt19937 rng(seed);
            vector<long long> wheel_rand = generate_wheel_random(N, prime_density, rng);
            double h = extract_H(wheel_rand, dr);
            values.push_back(h);
        }
        
        double mean = 0.0;
        for (double v : values) mean += v;
        mean /= values.size();
        
        double std = 0.0;
        for (double v : values) std += (v - mean) * (v - mean);
        std = sqrt(std / values.size());
        
        H_wheel_random[dr] = mean;
        H_wheel_random_std[dr] = std;
        
        cout << "  Δr=" << dr << ": H_WheelRandom = " << fixed << setprecision(4) 
             << mean << " ± " << std << endl;
    }
    cout << endl;
    
    // Compute H_WheelCramér (averaged over seeds)
    map<int, double> H_wheel_cramer;
    map<int, double> H_wheel_cramer_std;
    
    cout << "Computing H_WheelCramér(Δr)..." << endl;
    for (int dr : delta_r_values) {
        vector<double> values;
        for (int seed = 0; seed < num_seeds; ++seed) {
            vector<long long> wheel_cram = generate_wheel_cramer(N, seed);
            double h = extract_H(wheel_cram, dr);
            values.push_back(h);
        }
        
        double mean = 0.0;
        for (double v : values) mean += v;
        mean /= values.size();
        
        double std = 0.0;
        for (double v : values) std += (v - mean) * (v - mean);
        std = sqrt(std / values.size());
        
        H_wheel_cramer[dr] = mean;
        H_wheel_cramer_std[dr] = std;
        
        cout << "  Δr=" << dr << ": H_WheelCramér = " << fixed << setprecision(4) 
             << mean << " ± " << std << endl;
    }
    cout << endl;
    
    // Comparison table
    cout << "========================================" << endl;
    cout << "COMPARISON: H_Prime vs Wheel Models" << endl;
    cout << "========================================" << endl;
    cout << endl;
    
    cout << "Δr   H_Prime   H_WheelRandom   H_WheelCramér   Diff_Rand   Diff_Cram" << endl;
    cout << string(75, '-') << endl;
    
    for (int dr : delta_r_values) {
        double diff_rand = abs(H_prime[dr] - H_wheel_random[dr]);
        double diff_cram = abs(H_prime[dr] - H_wheel_cramer[dr]);
        
        cout << setw(2) << dr << "   "
             << fixed << setprecision(4) << H_prime[dr] << "    "
             << setprecision(4) << H_wheel_random[dr] << "        "
             << setprecision(4) << H_wheel_cramer[dr] << "        "
             << setprecision(4) << diff_rand << "      "
             << setprecision(4) << diff_cram << endl;
    }
    cout << endl;
    
    // Statistical test: Are means significantly different?
    cout << "========================================" << endl;
    cout << "STATISTICAL ASSESSMENT" << endl;
    cout << "========================================" << endl;
    cout << endl;
    
    for (int dr : delta_r_values) {
        double h_p = H_prime[dr];
        double h_wr = H_wheel_random[dr];
        double h_wc = H_wheel_cramer[dr];
        double std_wr = H_wheel_random_std[dr];
        double std_wc = H_wheel_cramer_std[dr];
        
        // Z-score (simplified, assumes normal distribution)
        double z_rand = abs(h_p - h_wr) / (std_wr + 1e-10);
        double z_cram = abs(h_p - h_wc) / (std_wc + 1e-10);
        
        cout << "Δr=" << dr << ":" << endl;
        cout << "  H_Prime vs H_WheelRandom: |diff| = " << fixed << setprecision(4) 
             << abs(h_p - h_wr) << ", z ≈ " << setprecision(2) << z_rand;
        if (z_rand > 2.0) cout << " (SIGNIFICANT)";
        cout << endl;
        
        cout << "  H_Prime vs H_WheelCramér: |diff| = " << fixed << setprecision(4) 
             << abs(h_p - h_wc) << ", z ≈ " << setprecision(2) << z_cram;
        if (z_cram > 2.0) cout << " (SIGNIFICANT)";
        cout << endl;
        cout << endl;
    }
    
    // Overall verdict
    cout << "========================================" << endl;
    cout << "STAGE 5.5 VERDICT" << endl;
    cout << "========================================" << endl;
    cout << endl;
    
    // Count significant differences
    int sig_rand = 0, sig_cram = 0;
    for (int dr : delta_r_values) {
        double z_rand = abs(H_prime[dr] - H_wheel_random[dr]) / (H_wheel_random_std[dr] + 1e-10);
        double z_cram = abs(H_prime[dr] - H_wheel_cramer[dr]) / (H_wheel_cramer_std[dr] + 1e-10);
        if (z_rand > 2.0) sig_rand++;
        if (z_cram > 2.0) sig_cram++;
    }
    
    if (sig_rand >= 3 && sig_cram >= 3) {
        cout << "VERDICT: H_Prime DIFFERS from both Wheel models" << endl;
        cout << "  → H(Δr) contains PRIME-SPECIFIC information" << endl;
        cout << "  → Wheel-30 structure alone insufficient" << endl;
        cout << "  → Higher-order correlations (k ≥ 3) remain plausible" << endl;
    } else if (sig_cram >= 3) {
        cout << "VERDICT: H_Prime DIFFERS from WheelCramér, similar to WheelRandom" << endl;
        cout << "  → log-density effect matters" << endl;
        cout << "  → But Wheel structure explains core" << endl;
    } else if (sig_rand >= 3) {
        cout << "VERDICT: H_Prime DIFFERS from WheelRandom, similar to WheelCramér" << endl;
        cout << "  → log-density + Wheel explains core" << endl;
        cout << "  → Prime-specific correlation minimal" << endl;
    } else {
        cout << "VERDICT: H_Prime SIMILAR to Wheel models" << endl;
        cout << "  → H(Δr) primarily Wheel-30 structure" << endl;
        cout << "  → Not prime-specific" << endl;
    }
    
    cout << endl;
    cout << "To proceed to Stage 6 (HL k-tuples):" << endl;
    cout << "  Require: H_Prime significantly differs from both Wheel models" << endl;
    cout << endl;
    
    return 0;
}
