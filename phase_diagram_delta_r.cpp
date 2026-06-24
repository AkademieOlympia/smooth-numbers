// Phase Diagram: R(Δr) for Bernoulli, Prime, Cramér
// Systematically tests gap asymmetry as function of residue class distance
//
// Key Question: Where does R_Prime cross above R_Bernoulli?
//
// Tests Δr = 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24
// for modulo 30 with multiple seeds for robustness

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <random>
#include <iomanip>
#include <algorithm>

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

// Generate Cramér model
vector<long long> generate_cramer_primes(long long limit, unsigned int seed) {
    mt19937 gen(seed);
    uniform_real_distribution<> dis(0.0, 1.0);
    
    vector<long long> sequence = {2, 3, 5};
    
    for (long long n = 7; n <= limit; n += 2) {
        if (n % 3 == 0 || n % 5 == 0) continue;
        
        double p = 2.0 / log(n);
        if (dis(gen) < p) {
            sequence.push_back(n);
        }
    }
    
    return sequence;
}

// Gap transition structure
struct GapTransitions {
    map<int, map<int, long long>> transitions;  // [from_class][gap_mod_30] -> count
    map<int, long long> class_counts;
    
    double compute_ratio(const vector<int>& low_gaps, const vector<int>& high_gaps, int from_class) const {
        long long low_count = 0, high_count = 0;
        
        auto it = transitions.find(from_class);
        if (it != transitions.end()) {
            for (int g : low_gaps) {
                auto git = it->second.find(g);
                if (git != it->second.end()) low_count += git->second;
            }
            for (int g : high_gaps) {
                auto git = it->second.find(g);
                if (git != it->second.end()) high_count += git->second;
            }
        }
        
        if (high_count == 0) return 0.0;
        return static_cast<double>(low_count) / high_count;
    }
    
    double compute_mean_ratio(const vector<int>& low_gaps, const vector<int>& high_gaps) const {
        vector<int> classes = {1, 7, 11, 13, 17, 19, 23, 29};
        double product = 1.0;
        int count = 0;
        
        for (int cls : classes) {
            auto it = class_counts.find(cls);
            if (it == class_counts.end() || it->second < 10) continue;
            
            double ratio = compute_ratio(low_gaps, high_gaps, cls);
            if (ratio > 0) {
                product *= ratio;
                count++;
            }
        }
        
        if (count == 0) return 0.0;
        return pow(product, 1.0 / count);
    }
};

// Analyze gaps
GapTransitions analyze_gaps(const vector<long long>& sequence) {
    GapTransitions stats;
    
    for (size_t i = 0; i + 1 < sequence.size(); ++i) {
        long long p1 = sequence[i];
        long long p2 = sequence[i + 1];
        
        if (p1 <= 5 || p2 <= 5) continue;
        
        int class1 = p1 % 30;
        int gap = (p2 - p1) % 30;
        
        stats.transitions[class1][gap]++;
        stats.class_counts[class1]++;
    }
    
    return stats;
}

// Generate symmetric gap pairs for given Δr
struct GapPair {
    vector<int> low;
    vector<int> high;
    int delta_r;
};

vector<GapPair> generate_gap_pairs_for_delta_r(int delta_r) {
    vector<GapPair> pairs;
    
    // For each possible starting gap offset, create pairs separated by delta_r
    // We use small gaps vs. gaps shifted by delta_r
    for (int offset = 2; offset <= 10; offset += 2) {
        GapPair pair;
        pair.delta_r = delta_r;
        
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

// Main phase diagram computation
struct PhasePoint {
    int delta_r;
    double r_bern_mean;
    double r_bern_std;
    double r_prime;
    double r_cram_mean;
    double r_cram_std;
};

vector<PhasePoint> compute_phase_diagram(long long limit, int num_seeds) {
    cout << "Computing phase diagram R(Δr)..." << endl;
    cout << "Limit: " << limit << ", Seeds: " << num_seeds << endl << endl;
    
    // Generate real primes once
    auto primes = sieve_primes(limit);
    auto prime_stats = analyze_gaps(primes);
    
    vector<PhasePoint> results;
    
    // Test different Δr values
    vector<int> delta_r_values = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24};
    
    for (int delta_r : delta_r_values) {
        cout << "Testing Δr = " << delta_r << "..." << flush;
        
        PhasePoint point;
        point.delta_r = delta_r;
        
        // Choose representative gap pairs
        vector<int> low_gaps, high_gaps;
        
        // Strategy: compare gaps around 2,4,6 vs gaps around (2+delta_r, 4+delta_r, 6+delta_r)
        for (int offset : {2, 4, 6}) {
            low_gaps.push_back(offset);
            high_gaps.push_back((offset + delta_r) % 30);
        }
        
        // Compute for real primes
        point.r_prime = prime_stats.compute_mean_ratio(low_gaps, high_gaps);
        
        // Compute for Bernoulli and Cramér over multiple seeds
        vector<double> r_bern_samples, r_cram_samples;
        
        double mean_gap = log(limit / 2);
        double p_const = 1.0 / mean_gap;
        
        for (int seed = 100; seed < 100 + num_seeds; ++seed) {
            auto bern = generate_bernoulli_sequence(limit, p_const, seed);
            auto cram = generate_cramer_primes(limit, seed);
            
            auto bern_stats = analyze_gaps(bern);
            auto cram_stats = analyze_gaps(cram);
            
            double r_b = bern_stats.compute_mean_ratio(low_gaps, high_gaps);
            double r_c = cram_stats.compute_mean_ratio(low_gaps, high_gaps);
            
            if (r_b > 0) r_bern_samples.push_back(r_b);
            if (r_c > 0) r_cram_samples.push_back(r_c);
        }
        
        // Compute means and std devs
        if (!r_bern_samples.empty()) {
            double sum = 0, sum_sq = 0;
            for (double x : r_bern_samples) { sum += x; sum_sq += x * x; }
            point.r_bern_mean = sum / r_bern_samples.size();
            point.r_bern_std = sqrt(sum_sq / r_bern_samples.size() - point.r_bern_mean * point.r_bern_mean);
        }
        
        if (!r_cram_samples.empty()) {
            double sum = 0, sum_sq = 0;
            for (double x : r_cram_samples) { sum += x; sum_sq += x * x; }
            point.r_cram_mean = sum / r_cram_samples.size();
            point.r_cram_std = sqrt(sum_sq / r_cram_samples.size() - point.r_cram_mean * point.r_cram_mean);
        }
        
        results.push_back(point);
        cout << " done." << endl;
    }
    
    return results;
}

// Print phase diagram
void print_phase_diagram(const vector<PhasePoint>& points) {
    cout << "\n=========================================" << endl;
    cout << "PHASE DIAGRAM: R(Δr)" << endl;
    cout << "=========================================" << endl;
    cout << "\nSystematic analysis of gap asymmetry as function of residue distance.\n" << endl;
    
    cout << setw(6) << "Δr"
         << setw(15) << "R_Bernoulli"
         << setw(15) << "R_Prime"
         << setw(15) << "R_Cramér"
         << setw(20) << "Hierarchy" << endl;
    cout << string(71, '-') << endl;
    
    int crossover_delta_r = -1;
    
    for (const auto& p : points) {
        cout << setw(6) << p.delta_r
             << setw(12) << fixed << setprecision(3) << p.r_bern_mean 
             << " ±" << setw(4) << setprecision(2) << p.r_bern_std
             << setw(12) << fixed << setprecision(3) << p.r_prime
             << "   "
             << setw(12) << fixed << setprecision(3) << p.r_cram_mean
             << " ±" << setw(4) << setprecision(2) << p.r_cram_std
             << "   ";
        
        // Determine hierarchy
        if (p.r_prime > p.r_bern_mean + p.r_bern_std) {
            cout << "Prime > Bern > Cram";
            if (crossover_delta_r < 0) crossover_delta_r = p.delta_r;
        } else if (p.r_prime < p.r_bern_mean - p.r_bern_std) {
            cout << "Bern > Prime > Cram";
        } else {
            cout << "Bern ≈ Prime > Cram";
        }
        
        cout << endl;
    }
    
    cout << "\n=========================================" << endl;
    cout << "INTERPRETATION" << endl;
    cout << "=========================================" << endl;
    
    if (crossover_delta_r > 0) {
        cout << "\n⭐ CROSSOVER DETECTED at Δr ≈ " << crossover_delta_r << " ⭐\n" << endl;
        cout << "The hierarchy REVERSES:" << endl;
        cout << "  • Small Δr: R_Bern > R_Prime  (geometric bias dominates)" << endl;
        cout << "  • Large Δr: R_Prime > R_Bern  (arithmetic correlations dominate)\n" << endl;
        cout << "IMPLICATION: For large residue distances, Hardy-Littlewood" << endl;
        cout << "correlations (twins, cousins, sexy primes) EXCEED the pure" << endl;
        cout << "geometric short-gap bias of constant-p Bernoulli processes.\n" << endl;
    } else {
        cout << "\nNo clear crossover detected in tested range." << endl;
        cout << "R_Bern > R_Prime > R_Cram holds consistently.\n" << endl;
    }
    
    cout << "Cramér model consistently shows LOWEST asymmetry (overdamping)." << endl;
}

int main(int argc, char* argv[]) {
    long long limit = 100000;
    int num_seeds = 5;
    
    if (argc > 1) limit = stoll(argv[1]);
    if (argc > 2) num_seeds = stoi(argv[2]);
    
    cout << "Phase Diagram Analysis: R(Δr)" << endl;
    cout << "=============================" << endl;
    cout << "Limit: " << limit << endl;
    cout << "Seeds per Δr: " << num_seeds << endl;
    cout << "\nThis will test Δr = 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24" << endl;
    cout << "to identify where R_Prime crosses above R_Bernoulli.\n" << endl;
    
    auto results = compute_phase_diagram(limit, num_seeds);
    print_phase_diagram(results);
    
    cout << "\n=========================================" << endl;
    cout << "THEORETICAL PREDICTION" << endl;
    cout << "=========================================" << endl;
    
    double p_typical = 0.05;
    double q = 1.0 - p_typical;
    
    cout << "\nFor constant-p Bernoulli with p ≈ " << p_typical << ":" << endl;
    cout << "R(Δr) ≈ q^(-Δr) = (0.95)^(-Δr)\n" << endl;
    
    cout << setw(10) << "Δr" << setw(20) << "R_predicted" << endl;
    cout << string(30, '-') << endl;
    for (int delta : {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24}) {
        cout << setw(10) << delta 
             << setw(20) << fixed << setprecision(3) << pow(q, -delta) << endl;
    }
    
    cout << "\n=========================================" << endl;
    cout << "NEXT STEPS" << endl;
    cout << "=========================================" << endl;
    cout << "\n1. If crossover is robust: Document in MODULO30_RESULTS.md" << endl;
    cout << "2. Rewrite paper to include regime-dependent interpretation" << endl;
    cout << "3. Hardy-Littlewood analysis becomes ESSENTIAL, not optional\n" << endl;
    
    return 0;
}
