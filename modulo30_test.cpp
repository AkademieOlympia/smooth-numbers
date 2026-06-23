// Modulo-30 Generalization Test
// Tests whether the geometric gap asymmetry generalizes to m=30
//
// Prime residue classes modulo 30: {1, 7, 11, 13, 17, 19, 23, 29}
// (8 classes, excluding multiples of 2, 3, 5)
//
// Gap residue classes: We test whether geometric bias depends on
// residue class distance Δr.

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
    if (p == 2 || p == 3 || p == 5) return -1;  // Special cases
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

// Generate Bernoulli point process with constant p
vector<long long> generate_bernoulli_sequence(long long limit, double p, unsigned int seed) {
    mt19937 gen(seed);
    geometric_distribution<int> gap_dist(p);
    
    vector<long long> sequence = {2, 3, 5};  // Start with small primes
    long long current = 7;  // First candidate coprime to 2,3,5
    
    while (current <= limit) {
        sequence.push_back(current);
        int gap = gap_dist(gen);
        current += (gap > 0 ? gap : 1);
        
        // Ensure we only hit numbers coprime to 30
        while (current % 2 == 0 || current % 3 == 0 || current % 5 == 0) {
            current++;
        }
    }
    
    return sequence;
}

// Generate Cramér model (variable p(n))
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

// Gap analysis structure
struct GapStats30 {
    map<int, map<int, long long>> transitions;  // [from_class][gap_mod_30] -> count
    map<int, long long> class_counts;            // [class] -> total count
    string label;
    
    // Compute gap asymmetry for specific residue class pairs
    double compute_asymmetry(const vector<int>& low_gaps, const vector<int>& high_gaps, int from_class) const {
        long long low_count = 0, high_count = 0;
        
        for (int g : low_gaps) {
            auto it = transitions.find(from_class);
            if (it != transitions.end()) {
                auto git = it->second.find(g);
                if (git != it->second.end()) {
                    low_count += git->second;
                }
            }
        }
        for (int g : high_gaps) {
            auto it = transitions.find(from_class);
            if (it != transitions.end()) {
                auto git = it->second.find(g);
                if (git != it->second.end()) {
                    high_count += git->second;
                }
            }
        }
        
        if (high_count == 0) return 0.0;
        return static_cast<double>(low_count) / high_count;
    }
    
    // Compute mean asymmetry over all starting classes
    double compute_mean_asymmetry(const vector<int>& low_gaps, const vector<int>& high_gaps) const {
        vector<int> classes = {1, 7, 11, 13, 17, 19, 23, 29};
        double product = 1.0;
        int count = 0;
        
        for (int cls : classes) {
            auto it = class_counts.find(cls);
            if (it == class_counts.end() || it->second < 10) continue;  // Skip low-count classes
            
            double ratio = compute_asymmetry(low_gaps, high_gaps, cls);
            if (ratio > 0) {
                product *= ratio;
                count++;
            }
        }
        
        if (count == 0) return 0.0;
        return pow(product, 1.0 / count);  // Geometric mean
    }
};

// Analyze gaps for a sequence
GapStats30 analyze_gaps_mod30(const vector<long long>& sequence, const string& label) {
    GapStats30 stats;
    stats.label = label;
    
    // Count transitions
    for (size_t i = 0; i + 1 < sequence.size(); ++i) {
        long long p1 = sequence[i];
        long long p2 = sequence[i + 1];
        
        if (p1 <= 5 || p2 <= 5) continue;  // Skip small primes
        
        int class1 = p1 % 30;
        int gap = (p2 - p1) % 30;
        
        stats.transitions[class1][gap]++;
        stats.class_counts[class1]++;
    }
    
    return stats;
}

// Print comprehensive statistics
void print_stats(const GapStats30& stats) {
    cout << "\n=== " << stats.label << " ===" << endl;
    cout << "Sample size: " << stats.class_counts.size() << " classes" << endl;
    
    // Print class distribution
    cout << "\nClass counts:" << endl;
    vector<int> classes = {1, 7, 11, 13, 17, 19, 23, 29};
    for (int cls : classes) {
        auto it = stats.class_counts.find(cls);
        if (it != stats.class_counts.end()) {
            cout << "  " << setw(2) << cls << ": " << setw(6) << it->second << endl;
        }
    }
}

// Test specific gap pairs with varying Delta r
void test_gap_pairs(const GapStats30& bernoulli, const GapStats30& cramer, const GapStats30& primes) {
    cout << "\n===========================================" << endl;
    cout << "MODULO-30 GAP ASYMMETRY TEST" << endl;
    cout << "===========================================" << endl;
    
    // Test pairs with different Delta r values
    struct TestCase {
        vector<int> low_gaps;
        vector<int> high_gaps;
        int delta_r;
        string description;
    };
    
    vector<TestCase> tests = {
        {{2, 4}, {12, 14}, 10, "Δr ≈ 10"},
        {{2, 4, 6}, {14, 16, 18}, 12, "Δr ≈ 12"},
        {{2, 6}, {18, 22}, 16, "Δr ≈ 16"},
        {{4, 6}, {16, 18}, 12, "Δr ≈ 12 (shifted)"},
    };
    
    cout << "\nTesting gap asymmetry R = P(low gaps) / P(high gaps):\n" << endl;
    cout << setw(20) << "Test Case" 
         << setw(15) << "R_Bernoulli" 
         << setw(15) << "R_Prime" 
         << setw(15) << "R_Cramér" << endl;
    cout << string(65, '-') << endl;
    
    for (const auto& test : tests) {
        double r_bern = bernoulli.compute_mean_asymmetry(test.low_gaps, test.high_gaps);
        double r_prime = primes.compute_mean_asymmetry(test.low_gaps, test.high_gaps);
        double r_cram = cramer.compute_mean_asymmetry(test.low_gaps, test.high_gaps);
        
        cout << setw(20) << test.description
             << setw(15) << fixed << setprecision(3) << r_bern
             << setw(15) << fixed << setprecision(3) << r_prime
             << setw(15) << fixed << setprecision(3) << r_cram << endl;
    }
    
    cout << "\n===========================================" << endl;
    cout << "THEORETICAL PREDICTION" << endl;
    cout << "===========================================" << endl;
    
    // Theoretical prediction: R ≈ q^(-Δr)
    double p_typical = 0.05;  // Typical acceptance probability
    double q = 1.0 - p_typical;
    
    cout << "\nFor constant-p Bernoulli process with p ≈ " << p_typical << ":" << endl;
    cout << "Predicted R(Δr) ≈ (1-p)^(-Δr) = q^(-Δr)\n" << endl;
    
    cout << setw(10) << "Δr" << setw(20) << "R_predicted" << endl;
    cout << string(30, '-') << endl;
    for (int delta : {6, 10, 12, 16, 20}) {
        double r_pred = pow(q, -delta);
        cout << setw(10) << delta << setw(20) << fixed << setprecision(3) << r_pred << endl;
    }
}

int main(int argc, char* argv[]) {
    long long limit = 100000;
    unsigned int seed = 42;
    
    if (argc > 1) limit = stoll(argv[1]);
    if (argc > 2) seed = stoi(argv[2]);
    
    cout << "Modulo-30 Generalization Test" << endl;
    cout << "=============================" << endl;
    cout << "Limit: " << limit << endl;
    cout << "Seed: " << seed << endl;
    
    // Generate sequences
    cout << "\nGenerating sequences..." << endl;
    auto primes = sieve_primes(limit);
    
    double mean_gap = log(limit / 2);
    double p_const = 1.0 / mean_gap;
    auto bernoulli = generate_bernoulli_sequence(limit, p_const, seed);
    auto cramer = generate_cramer_primes(limit, seed);
    
    cout << "Prime count: " << primes.size() << endl;
    cout << "Bernoulli count: " << bernoulli.size() << endl;
    cout << "Cramér count: " << cramer.size() << endl;
    
    // Analyze
    cout << "\nAnalyzing gaps modulo 30..." << endl;
    auto stats_bern = analyze_gaps_mod30(bernoulli, "Bernoulli Process");
    auto stats_cram = analyze_gaps_mod30(cramer, "Cramér Model");
    auto stats_prime = analyze_gaps_mod30(primes, "Real Primes");
    
    print_stats(stats_bern);
    print_stats(stats_cram);
    print_stats(stats_prime);
    
    // Test gap asymmetries
    test_gap_pairs(stats_bern, stats_cram, stats_prime);
    
    cout << "\n===========================================" << endl;
    cout << "INTERPRETATION" << endl;
    cout << "===========================================" << endl;
    cout << "\nIf the hierarchy R_Bernoulli > R_Prime > R_Cramér persists" << endl;
    cout << "for ALL tested Δr values, then the geometric origin of gap" << endl;
    cout << "asymmetry is UNIVERSAL and not specific to modulo 12.\n" << endl;
    
    return 0;
}
