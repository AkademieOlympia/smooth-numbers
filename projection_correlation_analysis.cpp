// Correlation Analysis of Gap-Pair Projections
// ==============================================
//
// QUESTION: Are the four projections A_2, A_4, A_6, A_8 structurally similar?
//
// Even if CV = 37.5% (too high for invariance), the curves might still be
// correlated, suggesting a deeper object H where A_i(Δr) = P_i(H).
//
// This analysis computes:
// 1. Pearson correlation ρ(A_i, A_j) for all pairs
// 2. Spearman rank correlation
// 3. Structural similarity metrics
//
// Interpretation:
//   ρ ≈ 0.8-1.0 → Same structure, different scaling (H exists!)
//   ρ ≈ 0.3-0.6 → Partial common core (complex H)
//   ρ ≈ 0       → Projectional construction (no common H)

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <random>
#include <iomanip>
#include <algorithm>
#include <numeric>
#include <fstream>

using namespace std;

// [Previous helper functions: classify_prime_mod30, sieve_primes, 
//  generate_bernoulli_sequence, GapTransitions, analyze_gaps, 
//  generate_gap_pairs - identical to gap_pair_robustness.cpp]

// ... [Include all the same helper code as before] ...

struct ProjectionData {
    int base_offset;
    vector<int> delta_r_values;
    vector<double> amplifications;
    
    map<int, double> get_map() const {
        map<int, double> result;
        for (size_t i = 0; i < delta_r_values.size(); ++i) {
            result[delta_r_values[i]] = amplifications[i];
        }
        return result;
    }
};

// Pearson correlation
double pearson_correlation(const vector<double>& x, const vector<double>& y) {
    if (x.size() != y.size() || x.empty()) return 0.0;
    
    double mean_x = accumulate(x.begin(), x.end(), 0.0) / x.size();
    double mean_y = accumulate(y.begin(), y.end(), 0.0) / y.size();
    
    double numerator = 0, sum_x_sq = 0, sum_y_sq = 0;
    for (size_t i = 0; i < x.size(); ++i) {
        double dx = x[i] - mean_x;
        double dy = y[i] - mean_y;
        numerator += dx * dy;
        sum_x_sq += dx * dx;
        sum_y_sq += dy * dy;
    }
    
    double denominator = sqrt(sum_x_sq * sum_y_sq);
    return (denominator > 0) ? (numerator / denominator) : 0.0;
}

// Spearman rank correlation
double spearman_correlation(vector<double> x, vector<double> y) {
    if (x.size() != y.size() || x.empty()) return 0.0;
    
    // Convert to ranks
    vector<pair<double, size_t>> x_indexed, y_indexed;
    for (size_t i = 0; i < x.size(); ++i) {
        x_indexed.push_back({x[i], i});
        y_indexed.push_back({y[i], i});
    }
    
    sort(x_indexed.begin(), x_indexed.end());
    sort(y_indexed.begin(), y_indexed.end());
    
    vector<double> x_ranks(x.size()), y_ranks(y.size());
    for (size_t i = 0; i < x.size(); ++i) {
        x_ranks[x_indexed[i].second] = i + 1;
        y_ranks[y_indexed[i].second] = i + 1;
    }
    
    return pearson_correlation(x_ranks, y_ranks);
}

// Analyze correlation between two projections
void analyze_pair_correlation(const ProjectionData& proj_i, const ProjectionData& proj_j) {
    // Find common Δr values
    auto map_i = proj_i.get_map();
    auto map_j = proj_j.get_map();
    
    vector<double> values_i, values_j;
    for (const auto& [dr, amp_i] : map_i) {
        auto it = map_j.find(dr);
        if (it != map_j.end()) {
            values_i.push_back(amp_i);
            values_j.push_back(it->second);
        }
    }
    
    if (values_i.size() < 3) {
        cout << "  Insufficient overlap" << endl;
        return;
    }
    
    double pearson = pearson_correlation(values_i, values_j);
    double spearman = spearman_correlation(values_i, values_j);
    
    cout << "  Base " << proj_i.base_offset << " vs Base " << proj_j.base_offset << ": "
         << "ρ(Pearson)=" << fixed << setprecision(3) << pearson
         << ", ρ(Spearman)=" << spearman;
    
    if (pearson > 0.8) {
        cout << "  ← STRONG correlation (same structure!)";
    } else if (pearson > 0.5) {
        cout << "  ← MODERATE correlation (partial core)";
    } else if (pearson > 0.2) {
        cout << "  ← WEAK correlation";
    } else {
        cout << "  ← NO correlation";
    }
    cout << endl;
}

// Full correlation matrix
void correlation_matrix(const vector<ProjectionData>& projections) {
    cout << "\n" << string(80, '=') << endl;
    cout << "CORRELATION MATRIX" << endl;
    cout << string(80, '=') << endl;
    
    cout << "\nPearson Correlations:" << endl;
    cout << string(50, '-') << endl;
    
    for (size_t i = 0; i < projections.size(); ++i) {
        for (size_t j = i + 1; j < projections.size(); ++j) {
            analyze_pair_correlation(projections[i], projections[j]);
        }
    }
    
    // Compute mean correlation
    vector<double> all_correlations;
    for (size_t i = 0; i < projections.size(); ++i) {
        for (size_t j = i + 1; j < projections.size(); ++j) {
            auto map_i = projections[i].get_map();
            auto map_j = projections[j].get_map();
            
            vector<double> values_i, values_j;
            for (const auto& [dr, amp_i] : map_i) {
                auto it = map_j.find(dr);
                if (it != map_j.end()) {
                    values_i.push_back(amp_i);
                    values_j.push_back(it->second);
                }
            }
            
            if (values_i.size() >= 3) {
                all_correlations.push_back(pearson_correlation(values_i, values_j));
            }
        }
    }
    
    double mean_corr = accumulate(all_correlations.begin(), all_correlations.end(), 0.0) / all_correlations.size();
    
    cout << string(50, '-') << endl;
    cout << "Mean pairwise correlation: " << fixed << setprecision(3) << mean_corr << endl;
    
    // Interpretation
    cout << "\n*** INTERPRETATION ***\n";
    if (mean_corr > 0.75) {
        cout << "STRONG structural similarity detected!\n";
        cout << "→ Projections likely arise from common H(Δr)\n";
        cout << "→ Model: A_i(Δr) = c_i · H(Δr) + ε_i(Δr)\n";
        cout << "→ Next: Extract projection-invariant H\n";
    } else if (mean_corr > 0.4) {
        cout << "MODERATE structural similarity\n";
        cout << "→ Partial common core exists\n";
        cout << "→ Model: Complex H with projection-dependent components\n";
        cout << "→ Next: Identify common vs. projection-specific parts\n";
    } else {
        cout << "WEAK or NO structural similarity\n";
        cout << "→ No simple common object H\n";
        cout << "→ A(Δr) is truly projection-dependent\n";
        cout << "→ Next: Reformulate or abandon A(Δr) approach\n";
    }
}

// [Main function would be similar to gap_pair_robustness.cpp 
//  but focused on correlation analysis]

int main(int argc, char* argv[]) {
    cout << "=== CORRELATION ANALYSIS OF PROJECTIONS ===" << endl;
    cout << "This implementation requires gap_pair_robustness output data" << endl;
    cout << "Please run gap_pair_robustness first and pipe results here" << endl;
    
    // In practice, this would read the output from gap_pair_robustness
    // and perform correlation analysis
    
    return 0;
}
