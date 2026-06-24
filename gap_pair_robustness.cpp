// Gap-Pair Robustness Test: Stage 4 Test for A(Δr)
// ====================================================
// 
// CRITICAL TEST: Is A(Δr) projection-invariant?
//
// Tests whether the arithmetic amplification factor A(Δr) is independent
// of the specific gap-pair selection used to define it.
//
// Four base offsets tested:
//   Base 2: {2,4,6} vs {2+Δr, 4+Δr, 6+Δr}  (original)
//   Base 4: {4,6,8} vs {4+Δr, 6+Δr, 8+Δr}
//   Base 6: {6,8,10} vs {6+Δr, 8+Δr, 10+Δr}
//   Base 8: {8,10,12} vs {8+Δr, 10+Δr, 12+Δr}
//
// Expected outcomes:
//   - If qualitative structure preserved → A(Δr) is projection-invariant (Stage 4 passed)
//   - If structure changes → A(Δr) is projection-dependent (deeper object needed)
//
// This test determines whether A(Δr) is a genuine mathematical object
// or merely a projection-dependent statistic.

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <random>
#include <iomanip>
#include <algorithm>
#include <numeric>

using namespace std;

// Classify prime mod 30
int classify_prime_mod30(long long p) {
    if (p == 2 || p == 3 || p == 5) return -1;
    return p % 30;
}

// Sieve of Eratosthenes
vector<long long> sieve_primes(long long limit) {
    vector<bool> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;
    
    for (long long i = 2; i * i <= limit; ++i) {
        if (is_prime[i]) {
            for (long long j = i * i; j <= limit; j += i) {
                is_prime[j] = false;
            }
        }
    }
    
    vector<long long> primes;
    for (long long i = 2; i <= limit; ++i) {
        if (is_prime[i]) primes.push_back(i);
    }
    return primes;
}

// Generate Bernoulli point process
vector<long long> generate_bernoulli_sequence(long long limit, double p, unsigned int seed) {
    mt19937 gen(seed);
    geometric_distribution<int> gap_dist(p);
    
    vector<long long> sequence = {2, 3, 5};
    long long current = 7;
    
    while (current <= limit) {
        sequence.push_back(current);
        int gap = gap_dist(gen);
        current += (gap > 0 ? gap : 1);
        
        while (current % 2 == 0 || current % 3 == 0 || current % 5 == 0) {
            current++;
        }
    }
    
    return sequence;
}

// Gap transition structure
struct GapTransitions {
    map<int, map<int, long long>> transitions;
    map<int, long long> class_counts;
    
    double compute_ratio(const vector<int>& low_gaps, const vector<int>& high_gaps) const {
        double geometric_mean_log = 0;
        int num_classes = 0;
        
        for (const auto& [from_class, gap_map] : transitions) {
            long long low_count = 0, high_count = 0;
            
            for (int g : low_gaps) {
                auto it = gap_map.find(g);
                if (it != gap_map.end()) low_count += it->second;
            }
            for (int g : high_gaps) {
                auto it = gap_map.find(g);
                if (it != gap_map.end()) high_count += it->second;
            }
            
            if (low_count > 0 && high_count > 0) {
                double ratio = static_cast<double>(low_count) / high_count;
                geometric_mean_log += log(ratio);
                num_classes++;
            }
        }
        
        return (num_classes > 0) ? exp(geometric_mean_log / num_classes) : 1.0;
    }
};

// Analyze gaps for a sequence
GapTransitions analyze_gaps(const vector<long long>& sequence) {
    GapTransitions stats;
    
    for (size_t i = 0; i + 1 < sequence.size(); ++i) {
        int from_class = classify_prime_mod30(sequence[i]);
        int to_class = classify_prime_mod30(sequence[i+1]);
        
        if (from_class == -1 || to_class == -1) continue;
        
        long long gap = sequence[i+1] - sequence[i];
        int gap_mod = gap % 30;
        
        stats.transitions[from_class][gap_mod]++;
        stats.class_counts[from_class]++;
    }
    
    return stats;
}

// Generate gap pairs for given base offset and Δr
pair<vector<int>, vector<int>> generate_gap_pairs(int base_offset, int delta_r) {
    vector<int> low_gaps = {base_offset, base_offset + 2, base_offset + 4};
    vector<int> high_gaps;
    
    for (int g : low_gaps) {
        high_gaps.push_back((g + delta_r) % 30);
    }
    
    return {low_gaps, high_gaps};
}

// Structure to store results for one (base_offset, Δr) combination
struct RobustnessPoint {
    int base_offset;
    int delta_r;
    double r_bernoulli;
    double r_prime;
    double amplification;  // A(Δr) = R_Prime / R_Bernoulli
    
    double bernoulli_std;
    double amplification_std;
};

// Compute robustness data for one base offset
vector<RobustnessPoint> compute_robustness_for_base(
    int base_offset,
    const vector<long long>& primes,
    const GapTransitions& prime_stats,
    long long limit,
    int num_seeds
) {
    vector<RobustnessPoint> results;
    vector<int> delta_r_values = {2, 6, 10, 14, 18, 22, 24};
    
    double p = 2.0 / log(limit);
    
    cout << "\n=== Base Offset " << base_offset << " ===" << endl;
    cout << "Gap pairs: {" << base_offset << "," << base_offset+2 << "," << base_offset+4 << "} vs shifted\n";
    cout << string(70, '-') << endl;
    
    for (int delta_r : delta_r_values) {
        auto [low_gaps, high_gaps] = generate_gap_pairs(base_offset, delta_r);
        
        // Real primes
        double r_prime = prime_stats.compute_ratio(low_gaps, high_gaps);
        
        // Bernoulli samples
        vector<double> r_bernoulli_samples;
        for (int seed = 100; seed < 100 + num_seeds; ++seed) {
            auto bernoulli_seq = generate_bernoulli_sequence(limit, p, seed);
            auto bernoulli_stats = analyze_gaps(bernoulli_seq);
            double r_b = bernoulli_stats.compute_ratio(low_gaps, high_gaps);
            r_bernoulli_samples.push_back(r_b);
        }
        
        double r_bernoulli_mean = accumulate(r_bernoulli_samples.begin(), 
                                             r_bernoulli_samples.end(), 0.0) / r_bernoulli_samples.size();
        
        double r_bernoulli_var = 0;
        for (double r : r_bernoulli_samples) {
            r_bernoulli_var += (r - r_bernoulli_mean) * (r - r_bernoulli_mean);
        }
        double r_bernoulli_std = sqrt(r_bernoulli_var / r_bernoulli_samples.size());
        
        // Amplification factor A(Δr)
        double amplification = r_prime / r_bernoulli_mean;
        
        // Amplification std (propagated error)
        double amplification_std = amplification * (r_bernoulli_std / r_bernoulli_mean);
        
        RobustnessPoint point;
        point.base_offset = base_offset;
        point.delta_r = delta_r;
        point.r_bernoulli = r_bernoulli_mean;
        point.r_prime = r_prime;
        point.amplification = amplification;
        point.bernoulli_std = r_bernoulli_std;
        point.amplification_std = amplification_std;
        
        results.push_back(point);
        
        cout << "Δr=" << setw(2) << delta_r << ": "
             << "A(Δr)=" << fixed << setprecision(3) << amplification 
             << " ±" << amplification_std
             << "  [R_P=" << r_prime << ", R_B=" << r_bernoulli_mean << "]";
        
        // Regime classification
        if (amplification > 1.02) {
            cout << "  ← ENHANCEMENT";
        } else if (amplification < 0.98) {
            cout << "  ← SUPPRESSION";
        } else {
            cout << "  ← NEUTRAL";
        }
        cout << endl;
    }
    
    return results;
}

// Compare structures across base offsets
void compare_structures(const map<int, vector<RobustnessPoint>>& all_results) {
    cout << "\n" << string(80, '=') << endl;
    cout << "STRUCTURE COMPARISON ACROSS BASE OFFSETS" << endl;
    cout << string(80, '=') << endl;
    
    // Extract Δr values (should be same for all)
    vector<int> delta_r_values;
    if (!all_results.empty()) {
        for (const auto& point : all_results.begin()->second) {
            delta_r_values.push_back(point.delta_r);
        }
    }
    
    cout << "\nTable: A(Δr) for different base offsets\n";
    cout << string(80, '-') << endl;
    cout << "Δr  | Base 2  | Base 4  | Base 6  | Base 8  | Qualitative Structure" << endl;
    cout << string(80, '-') << endl;
    
    for (size_t i = 0; i < delta_r_values.size(); ++i) {
        int delta_r = delta_r_values[i];
        cout << setw(2) << delta_r << "  |";
        
        vector<double> amplifications;
        vector<int> base_offsets = {2, 4, 6, 8};
        
        for (int base : base_offsets) {
            auto it = all_results.find(base);
            if (it != all_results.end() && i < it->second.size()) {
                double amp = it->second[i].amplification;
                amplifications.push_back(amp);
                cout << " " << fixed << setprecision(3) << amp << " |";
            } else {
                cout << "   N/A  |";
            }
        }
        
        // Determine qualitative structure
        if (amplifications.size() >= 3) {
            double mean_amp = accumulate(amplifications.begin(), amplifications.end(), 0.0) / amplifications.size();
            double max_amp = *max_element(amplifications.begin(), amplifications.end());
            double min_amp = *min_element(amplifications.begin(), amplifications.end());
            double range = max_amp - min_amp;
            
            if (mean_amp > 1.05 && range < 0.15) {
                cout << " CONSISTENT ENHANCE";
            } else if (mean_amp < 0.95 && range < 0.15) {
                cout << " CONSISTENT SUPPRESS";
            } else if (range < 0.10) {
                cout << " CONSISTENT NEUTRAL";
            } else {
                cout << " VARIABLE (" << fixed << setprecision(2) << range << " range)";
            }
        }
        cout << endl;
    }
    
    cout << string(80, '-') << endl;
}

// Quantitative robustness assessment
void assess_robustness(const map<int, vector<RobustnessPoint>>& all_results) {
    cout << "\n" << string(80, '=') << endl;
    cout << "ROBUSTNESS ASSESSMENT" << endl;
    cout << string(80, '=') << endl;
    
    // For each Δr, compute coefficient of variation of A(Δr) across bases
    map<int, vector<double>> amplifications_by_delta_r;
    
    for (const auto& [base, results] : all_results) {
        for (const auto& point : results) {
            amplifications_by_delta_r[point.delta_r].push_back(point.amplification);
        }
    }
    
    cout << "\nΔr  | Mean A(Δr) | Std Dev | CV (%)  | Assessment" << endl;
    cout << string(70, '-') << endl;
    
    for (const auto& [delta_r, amps] : amplifications_by_delta_r) {
        double mean = accumulate(amps.begin(), amps.end(), 0.0) / amps.size();
        
        double variance = 0;
        for (double a : amps) {
            variance += (a - mean) * (a - mean);
        }
        double std_dev = sqrt(variance / amps.size());
        double cv = (std_dev / mean) * 100.0;
        
        cout << setw(2) << delta_r << "  | "
             << fixed << setprecision(3) << mean << "      | "
             << setprecision(3) << std_dev << "   | "
             << setprecision(1) << cv << "%   | ";
        
        if (cv < 5.0) {
            cout << "HIGHLY ROBUST (projection-invariant)";
        } else if (cv < 10.0) {
            cout << "MODERATELY ROBUST";
        } else if (cv < 20.0) {
            cout << "WEAKLY ROBUST (partial dependence)";
        } else {
            cout << "NOT ROBUST (projection-dependent)";
        }
        cout << endl;
    }
    
    cout << string(70, '-') << endl;
    
    // Overall assessment
    vector<double> all_cvs;
    for (const auto& [delta_r, amps] : amplifications_by_delta_r) {
        double mean = accumulate(amps.begin(), amps.end(), 0.0) / amps.size();
        double variance = 0;
        for (double a : amps) variance += (a - mean) * (a - mean);
        double std_dev = sqrt(variance / amps.size());
        all_cvs.push_back((std_dev / mean) * 100.0);
    }
    
    double mean_cv = accumulate(all_cvs.begin(), all_cvs.end(), 0.0) / all_cvs.size();
    
    cout << "\n*** OVERALL STAGE 4 ASSESSMENT ***\n";
    cout << "Mean Coefficient of Variation: " << fixed << setprecision(1) << mean_cv << "%\n";
    cout << "\n";
    
    if (mean_cv < 8.0) {
        cout << "VERDICT: A(Δr) is PROJECTION-INVARIANT\n";
        cout << "         Stage 4 PASSED ✓\n";
        cout << "         A(Δr) qualifies as object candidate\n";
        cout << "         Next: Proceed to Stage 5 (theoretical connectability)\n";
    } else if (mean_cv < 15.0) {
        cout << "VERDICT: A(Δr) shows PARTIAL PROJECTION INVARIANCE\n";
        cout << "         Stage 4 PARTIALLY PASSED (~)\n";
        cout << "         A deeper projection-invariant object likely exists\n";
        cout << "         Next: Search for H such that A_i(Δr) = P_i(H)\n";
    } else {
        cout << "VERDICT: A(Δr) is PROJECTION-DEPENDENT\n";
        cout << "         Stage 4 NOT PASSED ✗\n";
        cout << "         A(Δr) is a statistic, not yet an object\n";
        cout << "         Next: Seek alternative decomposition\n";
    }
}

int main(int argc, char* argv[]) {
    long long limit = (argc > 1) ? atoll(argv[1]) : 1000000;
    int num_seeds = (argc > 2) ? atoi(argv[2]) : 10;
    
    cout << "╔════════════════════════════════════════════════════════════╗" << endl;
    cout << "║  GAP-PAIR ROBUSTNESS TEST: STAGE 4 FOR A(Δr)             ║" << endl;
    cout << "╚════════════════════════════════════════════════════════════╝" << endl;
    cout << "\nTesting projection invariance of A(Δr)\n";
    cout << "N = " << limit << ", Seeds = " << num_seeds << "\n";
    cout << "\nCRITICAL QUESTION:\n";
    cout << "Is A(Δr) independent of gap-pair selection?\n";
    cout << string(70, '=') << endl;
    
    // Generate real primes
    cout << "\nGenerating primes up to " << limit << "..." << endl;
    auto primes = sieve_primes(limit);
    auto prime_stats = analyze_gaps(primes);
    cout << "Found " << primes.size() << " primes.\n";
    
    // Test four base offsets
    vector<int> base_offsets = {2, 4, 6, 8};
    map<int, vector<RobustnessPoint>> all_results;
    
    for (int base : base_offsets) {
        all_results[base] = compute_robustness_for_base(base, primes, prime_stats, limit, num_seeds);
    }
    
    // Compare structures
    compare_structures(all_results);
    
    // Assess robustness
    assess_robustness(all_results);
    
    cout << "\n" << string(80, '=') << endl;
    cout << "Test complete. See assessment above." << endl;
    cout << string(80, '=') << endl;
    
    return 0;
}
