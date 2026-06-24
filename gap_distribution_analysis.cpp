// Empirical Gap Distribution Analysis
// =====================================
//
// Rekonstruiert empirische Gap-Gewichte w_g^emp(Δr) direkt aus den Daten.
//
// Vorgehen:
// 1. Für jedes Prime-Pair (p_n, p_{n+1}):
//    - Gap g = p_{n+1} - p_n
//    - Residue-Klassen r_n, r_{n+1} mod 30
//    - Δr = |r_{n+1} - r_n| (modular)
// 2. Histogram: Welche Gaps g tragen zu welchem Δr bei?
// 3. Empirische Gewichte: w_g^emp(Δr) = count(g, Δr) / total(Δr)
// 4. Hardy-Littlewood-Singularserien S(g)
// 5. Konstruiere: H_HL,emp(Δr) = ∑_g w_g^emp(Δr) · S(g)
// 6. Vergleiche mit H_emp(Δr)

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <algorithm>
#include <iomanip>

using namespace std;

// Zulässige Residue-Klassen modulo 30 (coprime to 30 = 2·3·5)
const vector<int> RESIDUES_MOD30 = {1, 7, 11, 13, 17, 19, 23, 29};

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

// Residue-Class difference modulo 30
int compute_delta_r(int r1, int r2) {
    // Kleinster positiver Abstand zwischen Residue-Klassen
    int diff = abs(r2 - r1);
    if (diff > 15) diff = 30 - diff;  // Wrap around
    return diff;
}

// Hardy-Littlewood Singular Series S(g)
double hardy_littlewood_S(int g) {
    // Vereinfachte Berechnung für kleine Gaps
    // S(2) ≈ 0.6602 (Twin Prime Constant)
    // S(4) ≈ 1.3204
    // S(6) ≈ 1.3203
    
    // Approximation basierend auf bekannten Werten
    map<int, double> known_values = {
        {2, 0.6602},   // Twin Prime Constant
        {4, 1.3204},
        {6, 1.3203},   // Sexy Prime Constant
        {10, 2.8582},
        {12, 3.5777},
        {18, 5.9929},
        {30, 11.8508}
    };
    
    if (known_values.count(g)) {
        return known_values[g];
    }
    
    // Für unbekannte Gaps: Einfache Approximation
    // S(g) ≈ C · g / log(g) mit C ≈ 1.32
    if (g < 2) return 0.0;
    return 1.32 * g / log(g);
}

struct GapDistribution {
    map<int, map<int, long long>> gap_counts;  // gap_counts[delta_r][gap] = count
    map<int, long long> delta_r_totals;        // Total count for each delta_r
    
    void add_observation(int delta_r, int gap) {
        gap_counts[delta_r][gap]++;
        delta_r_totals[delta_r]++;
    }
    
    map<int, double> get_weights(int delta_r) const {
        map<int, double> weights;
        if (delta_r_totals.count(delta_r) == 0) return weights;
        
        long long total = delta_r_totals.at(delta_r);
        for (const auto& [gap, count] : gap_counts.at(delta_r)) {
            weights[gap] = static_cast<double>(count) / total;
        }
        return weights;
    }
    
    double compute_H_HL_emp(int delta_r) const {
        auto weights = get_weights(delta_r);
        double H_HL = 0.0;
        
        for (const auto& [gap, weight] : weights) {
            double S_g = hardy_littlewood_S(gap);
            H_HL += weight * S_g;
        }
        
        return H_HL;
    }
    
    void print_distribution(int delta_r) const {
        if (gap_counts.count(delta_r) == 0) {
            cout << "No data for Δr = " << delta_r << endl;
            return;
        }
        
        cout << "Δr = " << delta_r << ":" << endl;
        cout << "  Total observations: " << delta_r_totals.at(delta_r) << endl;
        cout << "  Gap distribution:" << endl;
        
        // Sort gaps by frequency
        vector<pair<int, long long>> sorted_gaps(gap_counts.at(delta_r).begin(), 
                                                   gap_counts.at(delta_r).end());
        sort(sorted_gaps.begin(), sorted_gaps.end(), 
             [](const auto& a, const auto& b) { return a.second > b.second; });
        
        cout << "    Gap    Count      Weight    S(g)     Contribution" << endl;
        cout << "    " << string(60, '-') << endl;
        
        double H_HL = 0.0;
        long long total = delta_r_totals.at(delta_r);
        
        int count_printed = 0;
        for (const auto& [gap, count] : sorted_gaps) {
            double weight = static_cast<double>(count) / total;
            double S_g = hardy_littlewood_S(gap);
            double contrib = weight * S_g;
            H_HL += contrib;
            
            if (count_printed < 10) {
                cout << "    " << setw(3) << gap 
                     << "    " << setw(8) << count
                     << "    " << fixed << setprecision(4) << weight
                     << "    " << setprecision(4) << S_g
                     << "    " << setprecision(4) << contrib << endl;
                count_printed++;
            }
        }
        
        if (sorted_gaps.size() > 10) {
            cout << "    ... (" << (sorted_gaps.size() - 10) << " more gaps)" << endl;
        }
        
        cout << "  H_HL,emp(Δr=" << delta_r << ") = " << setprecision(4) << H_HL << endl;
        cout << endl;
    }
};

int main(int argc, char* argv[]) {
    long long N = 1000000;  // Default
    if (argc > 1) {
        N = atoll(argv[1]);
    }
    
    cout << "================================" << endl;
    cout << "EMPIRICAL GAP DISTRIBUTION ANALYSIS" << endl;
    cout << "================================" << endl;
    cout << endl;
    cout << "Analyzing primes up to N = " << N << endl;
    cout << endl;
    
    // Generate primes
    cout << "Generating primes..." << flush;
    vector<long long> primes = sieve_primes(N);
    cout << " done. Found " << primes.size() << " primes." << endl;
    cout << endl;
    
    // Analyze gap distribution
    cout << "Analyzing gap distribution..." << flush;
    GapDistribution dist;
    
    for (size_t i = 1; i < primes.size(); ++i) {
        long long p_prev = primes[i-1];
        long long p_curr = primes[i];
        int gap = p_curr - p_prev;
        
        int r_prev = p_prev % 30;
        int r_curr = p_curr % 30;
        
        // Check if both are in valid residue classes
        if (find(RESIDUES_MOD30.begin(), RESIDUES_MOD30.end(), r_prev) == RESIDUES_MOD30.end()) continue;
        if (find(RESIDUES_MOD30.begin(), RESIDUES_MOD30.end(), r_curr) == RESIDUES_MOD30.end()) continue;
        
        int delta_r = compute_delta_r(r_prev, r_curr);
        
        dist.add_observation(delta_r, gap);
    }
    cout << " done." << endl;
    cout << endl;
    
    // Print distributions for Δr ≤ 18
    cout << string(80, '=') << endl;
    cout << "GAP DISTRIBUTIONS FOR EACH Δr" << endl;
    cout << string(80, '=') << endl;
    cout << endl;
    
    vector<int> delta_r_values = {2, 6, 10, 14, 18};
    
    for (int dr : delta_r_values) {
        dist.print_distribution(dr);
    }
    
    // Compute H_HL,emp for all Δr and compare with H_emp
    cout << string(80, '=') << endl;
    cout << "COMPARISON: H_emp vs H_HL,emp" << endl;
    cout << string(80, '=') << endl;
    cout << endl;
    
    // Empirical H(Δr) values from extraction
    map<int, double> H_emp = {
        {2, 0.834},
        {6, 0.540},
        {10, 0.422},
        {14, 0.329},
        {18, 0.241}
    };
    
    cout << "Δr    H_emp    H_HL,emp    Ratio    H_emp/H_HL,emp" << endl;
    cout << string(60, '-') << endl;
    
    vector<double> ratios;
    
    for (int dr : delta_r_values) {
        double h_emp = H_emp[dr];
        double h_hl_emp = dist.compute_H_HL_emp(dr);
        double ratio = h_emp / h_hl_emp;
        ratios.push_back(ratio);
        
        cout << setw(2) << dr << "    "
             << fixed << setprecision(3) << h_emp << "    "
             << setprecision(3) << h_hl_emp << "    "
             << setprecision(3) << ratio << endl;
    }
    
    cout << endl;
    
    // Compute optimal scaling factor
    double mean_ratio = 0.0;
    for (double r : ratios) mean_ratio += r;
    mean_ratio /= ratios.size();
    
    cout << "Mean ratio (scaling factor): c = " << setprecision(4) << mean_ratio << endl;
    cout << endl;
    
    // Compute correlation
    cout << "To compute full correlation, run Python analysis:" << endl;
    cout << "  python3 analyze_gap_distribution.py" << endl;
    cout << endl;
    
    return 0;
}
