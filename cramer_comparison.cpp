/*
 * Cramér Comparison Analysis
 * 
 * Vergleicht echte Primzahlen mit synthetischen Cramér-Primzahlen bezüglich
 * der Gap-Asymmetrie modulo 12.
 * 
 * Cramér-Modell:
 * - Jede ungerade Zahl n erhält Wahrscheinlichkeit ~2/ln(n), Primzahl zu sein
 * - Erzeugt "Primzahlen" mit korrekter Dichte
 * - Aber OHNE Siebstruktur von Eratosthenes
 * 
 * KRITISCHE FRAGE:
 * Falls R_Cramér ≈ 1, R_prime > 1: Gap-Asymmetrie ist primzahl-spezifisch
 * Falls R_Cramér ≈ R_prime: Gap-Asymmetrie ist allgemeines Phänomen dünner Mengen
 * 
 * Dies trennt:
 * "Sieb-Effekte" vs. "Dünne-Menge-Effekte"
 * 
 * Autor: Thomas Hoffbauer
 * Datum: Juni 2026
 */

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <random>
#include <iomanip>
#include <algorithm>

using namespace std;

// Sieb von Eratosthenes (echte Primzahlen)
vector<long long> sieve(long long limit) {
    if (limit < 2) return {};
    
    vector<bool> is_prime(limit + 1, true);
    is_prime[0] = is_prime[1] = false;
    
    for (long long p = 2; p * p <= limit; p++) {
        if (is_prime[p]) {
            for (long long i = p * p; i <= limit; i += p) {
                is_prime[i] = false;
            }
        }
    }
    
    vector<long long> primes;
    for (long long i = 2; i <= limit; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
        }
    }
    
    return primes;
}

// Cramér-Primzahlen generieren
// Jede ungerade Zahl n hat Wahrscheinlichkeit p(n) ≈ 2/ln(n), eine "Primzahl" zu sein
vector<long long> generate_cramer_primes(long long limit, unsigned int seed = 12345) {
    mt19937_64 gen(seed);
    uniform_real_distribution<double> dis(0.0, 1.0);
    
    vector<long long> cramer_primes;
    cramer_primes.push_back(2);  // 2 ist immer dabei
    cramer_primes.push_back(3);  // 3 ist immer dabei
    
    // Für ungerade Zahlen ab 5
    for (long long n = 5; n <= limit; n += 2) {
        double prob = 2.0 / log(n);  // Cramér-Wahrscheinlichkeit
        
        if (dis(gen) < prob) {
            cramer_primes.push_back(n);
        }
    }
    
    return cramer_primes;
}

// EABC-Klassifikation
string classify(long long p) {
    if (p == 2) return "2";
    if (p == 3) return "3";
    
    int r = p % 12;
    switch(r) {
        case 1: return "E";
        case 5: return "A";
        case 7: return "B";
        case 11: return "C";
        default: return "X";
    }
}

// Gap-Statistiken berechnen
struct GapStats {
    string label;
    long long num_primes;
    
    // gap_counts[start_class][gap_mod_12] = count
    map<string, map<int, int>> gap_counts;
    
    // Ratios P(g≡2,4) / P(g≡8,10) für jede Klasse
    map<string, double> ratios;
    
    double geometric_mean_ratio() const {
        double product = 1.0;
        int count = 0;
        
        for (const auto& [cls, ratio] : ratios) {
            if (ratio > 0) {
                product *= ratio;
                count++;
            }
        }
        
        return (count > 0) ? pow(product, 1.0 / count) : 0.0;
    }
    
    void compute_ratios() {
        vector<string> classes = {"E", "A", "B", "C"};
        
        for (const auto& cls : classes) {
            if (gap_counts[cls].empty()) continue;
            
            int sum_2_4 = (gap_counts[cls].count(2) ? gap_counts[cls][2] : 0) +
                          (gap_counts[cls].count(4) ? gap_counts[cls][4] : 0);
            int sum_8_10 = (gap_counts[cls].count(8) ? gap_counts[cls][8] : 0) +
                           (gap_counts[cls].count(10) ? gap_counts[cls][10] : 0);
            
            if (sum_8_10 > 0) {
                ratios[cls] = static_cast<double>(sum_2_4) / sum_8_10;
            } else {
                ratios[cls] = 0.0;
            }
        }
    }
};

GapStats analyze_gaps(const vector<long long>& primes, const string& label) {
    GapStats stats;
    stats.label = label;
    stats.num_primes = primes.size();
    
    for (size_t i = 0; i < primes.size() - 1; i++) {
        long long p = primes[i];
        long long q = primes[i + 1];
        long long gap = q - p;
        
        string cls = classify(p);
        if (cls == "2" || cls == "3" || cls == "X") continue;
        
        int gap_mod = gap % 12;
        stats.gap_counts[cls][gap_mod]++;
    }
    
    stats.compute_ratios();
    
    return stats;
}

void print_gap_stats(const GapStats& stats) {
    cout << "\n=== " << stats.label << " ===" << endl;
    cout << "Anzahl: " << stats.num_primes << endl;
    cout << "\nRatios P(g≡2,4) / P(g≡8,10):" << endl;
    cout << string(60, '-') << endl;
    
    vector<string> classes = {"E", "A", "B", "C"};
    
    for (const auto& cls : classes) {
        if (stats.gap_counts.find(cls) != stats.gap_counts.end()) {
            const auto& counts = stats.gap_counts.at(cls);
            
            int sum_2_4 = (counts.count(2) ? counts.at(2) : 0) + 
                          (counts.count(4) ? counts.at(4) : 0);
            int sum_8_10 = (counts.count(8) ? counts.at(8) : 0) + 
                           (counts.count(10) ? counts.at(10) : 0);
            
            double ratio = stats.ratios.count(cls) ? stats.ratios.at(cls) : 0.0;
            
            cout << cls << " (≡";
            if (cls == "E") cout << "1";
            else if (cls == "A") cout << "5";
            else if (cls == "B") cout << "7";
            else if (cls == "C") cout << "11";
            cout << "): ";
            
            cout << fixed << setprecision(3) << ratio;
            cout << "  [" << sum_2_4 << " vs " << sum_8_10 << "]" << endl;
        }
    }
    
    cout << "\nGeometrisches Mittel: " << fixed << setprecision(3) 
         << stats.geometric_mean_ratio() << endl;
}

void print_comparison(const GapStats& real_stats, const GapStats& cramer_stats) {
    cout << "\n" << string(80, '=') << endl;
    cout << "CRAMÉR-VERGLEICH" << endl;
    cout << string(80, '=') << endl;
    
    // Tabelle
    cout << "\n" << setw(20) << "Klasse";
    cout << setw(15) << "Real";
    cout << setw(15) << "Cramér";
    cout << setw(15) << "Differenz" << endl;
    cout << string(65, '-') << endl;
    
    vector<string> classes = {"E", "A", "B", "C"};
    
    for (const auto& cls : classes) {
        double real_ratio = real_stats.ratios.count(cls) ? real_stats.ratios.at(cls) : 0.0;
        double cramer_ratio = cramer_stats.ratios.count(cls) ? cramer_stats.ratios.at(cls) : 0.0;
        double diff = real_ratio - cramer_ratio;
        
        cout << setw(20) << (cls + " (≡" + 
                             (cls == "E" ? "1" : cls == "A" ? "5" : cls == "B" ? "7" : "11") + ")");
        cout << fixed << setprecision(3);
        cout << setw(15) << real_ratio;
        cout << setw(15) << cramer_ratio;
        cout << setw(15) << showpos << diff << noshowpos << endl;
    }
    
    cout << string(65, '-') << endl;
    cout << setw(20) << "GEOMETRISCHES MITTEL";
    double real_mean = real_stats.geometric_mean_ratio();
    double cramer_mean = cramer_stats.geometric_mean_ratio();
    double mean_diff = real_mean - cramer_mean;
    
    cout << fixed << setprecision(3);
    cout << setw(15) << real_mean;
    cout << setw(15) << cramer_mean;
    cout << setw(15) << showpos << mean_diff << noshowpos << endl;
    
    cout << "\n" << string(80, '=') << endl;
    cout << "INTERPRETATION" << endl;
    cout << string(80, '=') << endl;
    
    double excess_percent = (real_mean - cramer_mean) / cramer_mean * 100;
    
    cout << "\nR_gap(Real):   " << fixed << setprecision(3) << real_mean << endl;
    cout << "R_gap(Cramér): " << fixed << setprecision(3) << cramer_mean << endl;
    cout << "Differenz:     " << showpos << fixed << setprecision(3) << mean_diff << noshowpos << endl;
    cout << "Excess:        " << showpos << fixed << setprecision(1) << excess_percent << "%" << noshowpos << endl;
    
    cout << "\n";
    
    if (abs(excess_percent) < 5) {
        cout << "≈ CRAMÉR-MODELL KONSISTENT" << endl;
        cout << "  Real ≈ Cramér (Differenz < 5%)" << endl;
        cout << "\n  INTERPRETATION:" << endl;
        cout << "  → Die Gap-Asymmetrie ist ein ALLGEMEINES Phänomen dünner Mengen" << endl;
        cout << "  → NICHT primzahl-spezifisch" << endl;
        cout << "  → Siebstruktur spielt KEINE wesentliche Rolle" << endl;
        cout << "  → Das Cramér-Modell erklärt den Effekt bereits" << endl;
        cout << "\n  KONSEQUENZ:" << endl;
        cout << "  Die EABC-Asymmetrie ist kein spezifisches Primzahl-Phänomen," << endl;
        cout << "  sondern eine Eigenschaft dünner Mengen mit modularer Struktur." << endl;
    } else if (excess_percent > 5 && excess_percent < 20) {
        cout << "↗ REAL > CRAMÉR (MODERAT)" << endl;
        cout << "  Real übertrifft Cramér um " << excess_percent << "%" << endl;
        cout << "\n  INTERPRETATION:" << endl;
        cout << "  → Primzahlen zeigen STÄRKERE Asymmetrie als Cramér-Modell" << endl;
        cout << "  → Siebstruktur trägt messbar bei" << endl;
        cout << "  → Aber Cramér erklärt Haupteffekt" << endl;
        cout << "\n  KONSEQUENZ:" << endl;
        cout << "  Die Gap-Asymmetrie ist TEILWEISE primzahl-spezifisch." << endl;
        cout << "  Cramér-Effekt + Sieb-Korrekturen." << endl;
    } else if (excess_percent > 20) {
        cout << "↑↑ REAL >> CRAMÉR (STARK)" << endl;
        cout << "  Real übertrifft Cramér um " << excess_percent << "%" << endl;
        cout << "\n  INTERPRETATION:" << endl;
        cout << "  → Die Asymmetrie ist STARK primzahl-spezifisch" << endl;
        cout << "  → Siebstruktur ist ENTSCHEIDEND" << endl;
        cout << "  → Cramér-Modell ist UNZUREICHEND" << endl;
        cout << "\n  KONSEQUENZ:" << endl;
        cout << "  Die EABC-Gap-Asymmetrie ist ein genuines Primzahl-Phänomen," << endl;
        cout << "  das aus der Siebstruktur von Eratosthenes entsteht." << endl;
    } else if (excess_percent < -5) {
        cout << "⚠ REAL < CRAMÉR (UNERWARTET)" << endl;
        cout << "  Primzahlen zeigen SCHWÄCHERE Asymmetrie als Cramér" << endl;
        cout << "\n  INTERPRETATION:" << endl;
        cout << "  → Unerwartetes Ergebnis" << endl;
        cout << "  → Möglicherweise Artefakt der Stichprobe" << endl;
        cout << "  → Wiederholen mit anderem Seed" << endl;
    }
}

int main(int argc, char* argv[]) {
    cout << "=== CRAMÉR COMPARISON ANALYSIS ===" << endl;
    cout << "Vergleich: Echte Primzahlen vs. Cramér-Modell" << endl;
    cout << endl;
    
    // Parameter
    long long limit = 100000;
    unsigned int seed = 12345;
    int num_trials = 1;
    
    if (argc >= 2) {
        limit = stoll(argv[1]);
    }
    
    if (argc >= 3) {
        num_trials = stoi(argv[2]);
    }
    
    cout << "Parameter:" << endl;
    cout << "  Limit: " << limit << endl;
    cout << "  Cramér-Trials: " << num_trials << endl;
    cout << endl;
    
    // Echte Primzahlen
    cout << "Generiere echte Primzahlen bis " << limit << "..." << endl;
    vector<long long> real_primes = sieve(limit);
    cout << "  → " << real_primes.size() << " Primzahlen gefunden" << endl;
    
    GapStats real_stats = analyze_gaps(real_primes, "ECHTE PRIMZAHLEN");
    print_gap_stats(real_stats);
    
    // Cramér-Primzahlen (mehrere Trials für Stabilität)
    cout << "\n" << string(80, '-') << endl;
    cout << "Generiere Cramér-Primzahlen..." << endl;
    
    vector<GapStats> cramer_trials;
    
    for (int trial = 0; trial < num_trials; trial++) {
        unsigned int trial_seed = seed + trial * 1000;
        
        vector<long long> cramer_primes = generate_cramer_primes(limit, trial_seed);
        
        if (trial == 0 || num_trials <= 3) {
            cout << "  Trial " << (trial + 1) << ": " << cramer_primes.size() 
                 << " Cramér-Primzahlen (Seed=" << trial_seed << ")" << endl;
        }
        
        GapStats cramer_stats = analyze_gaps(
            cramer_primes, 
            "CRAMÉR-PRIMZAHLEN (Trial " + to_string(trial + 1) + ")"
        );
        
        cramer_trials.push_back(cramer_stats);
    }
    
    // Durchschnitt über alle Trials
    GapStats avg_cramer_stats;
    avg_cramer_stats.label = "CRAMÉR-PRIMZAHLEN (Durchschnitt)";
    avg_cramer_stats.num_primes = 0;
    
    for (const auto& trial : cramer_trials) {
        avg_cramer_stats.num_primes += trial.num_primes;
    }
    avg_cramer_stats.num_primes /= num_trials;
    
    // Durchschnittliche Ratios
    vector<string> classes = {"E", "A", "B", "C"};
    for (const auto& cls : classes) {
        double sum = 0.0;
        int count = 0;
        
        for (const auto& trial : cramer_trials) {
            if (trial.ratios.count(cls)) {
                sum += trial.ratios.at(cls);
                count++;
            }
        }
        
        if (count > 0) {
            avg_cramer_stats.ratios[cls] = sum / count;
        }
    }
    
    if (num_trials == 1) {
        print_gap_stats(cramer_trials[0]);
        print_comparison(real_stats, cramer_trials[0]);
    } else {
        cout << "\n  → Durchschnitt über " << num_trials << " Trials berechnet" << endl;
        print_gap_stats(avg_cramer_stats);
        
        // Variabilität anzeigen
        cout << "\nVariabilität über Trials:" << endl;
        for (const auto& cls : classes) {
            vector<double> trial_ratios;
            for (const auto& trial : cramer_trials) {
                if (trial.ratios.count(cls)) {
                    trial_ratios.push_back(trial.ratios.at(cls));
                }
            }
            
            if (!trial_ratios.empty()) {
                double mean = 0.0;
                for (double r : trial_ratios) mean += r;
                mean /= trial_ratios.size();
                
                double std_dev = 0.0;
                for (double r : trial_ratios) {
                    std_dev += (r - mean) * (r - mean);
                }
                std_dev = sqrt(std_dev / trial_ratios.size());
                
                cout << "  " << cls << ": " << fixed << setprecision(3) 
                     << mean << " ± " << std_dev << endl;
            }
        }
        
        print_comparison(real_stats, avg_cramer_stats);
    }
    
    // Zusätzliche Statistiken
    cout << "\n" << string(80, '=') << endl;
    cout << "ZUSÄTZLICHE BEOBACHTUNGEN" << endl;
    cout << string(80, '=') << endl;
    
    cout << "\nDichte-Vergleich:" << endl;
    double real_density = static_cast<double>(real_primes.size()) / limit;
    double expected_density = 1.0 / log(limit);
    cout << "  Echte Primzahldichte:     " << fixed << setprecision(6) << real_density << endl;
    cout << "  Erwartete Dichte (π(x)/x ≈ 1/ln(x)): " << expected_density << endl;
    cout << "  Cramér-Dichte (Durchschnitt): " << static_cast<double>(avg_cramer_stats.num_primes) / limit << endl;
    
    cout << "\nKLASSEN-SPEZIFISCHE ANALYSE:" << endl;
    for (const auto& cls : classes) {
        double real_ratio = real_stats.ratios.count(cls) ? real_stats.ratios.at(cls) : 0.0;
        double cramer_ratio = avg_cramer_stats.ratios.count(cls) ? avg_cramer_stats.ratios.at(cls) : 0.0;
        double diff_percent = (cramer_ratio > 0) ? (real_ratio - cramer_ratio) / cramer_ratio * 100 : 0.0;
        
        cout << "\n" << cls << ": ";
        
        if (abs(diff_percent) < 5) {
            cout << "Konsistent mit Cramér";
        } else if (diff_percent > 10) {
            cout << "STARK primzahl-spezifisch (+";
            cout << fixed << setprecision(1) << diff_percent << "%)";
        } else if (diff_percent > 5) {
            cout << "Moderat primzahl-spezifisch (+";
            cout << fixed << setprecision(1) << diff_percent << "%)";
        }
    }
    
    cout << "\n\n" << string(80, '=') << endl;
    cout << "SCHLUSSFOLGERUNG" << endl;
    cout << string(80, '=') << endl;
    
    double excess = (real_stats.geometric_mean_ratio() - avg_cramer_stats.geometric_mean_ratio()) / 
                    avg_cramer_stats.geometric_mean_ratio() * 100;
    
    if (abs(excess) < 5) {
        cout << "\nDas Cramér-Modell ERKLÄRT die Gap-Asymmetrie vollständig." << endl;
        cout << "Die EABC-Struktur ist NICHT primzahl-spezifisch." << endl;
        cout << "\nNÄCHSTER SCHRITT: Theoretische Analyse des Cramér-Modells" << endl;
    } else if (excess > 5 && excess < 20) {
        cout << "\nDas Cramér-Modell erklärt den HAUPTEFFEKT," << endl;
        cout << "aber Primzahlen zeigen ZUSÄTZLICHE Struktur." << endl;
        cout << "\nNÄCHSTER SCHRITT: Analyse der Sieb-Korrekturen" << endl;
    } else if (excess > 20) {
        cout << "\nDas Cramér-Modell ist UNZUREICHEND." << endl;
        cout << "Die Gap-Asymmetrie ist STARK primzahl-spezifisch." << endl;
        cout << "\nNÄCHSTER SCHRITT: Detaillierte Siebtheorie-Analyse" << endl;
    }
    
    cout << "\n" << string(80, '=') << endl;
    cout << "Für weitere Analysen:" << endl;
    cout << "  - gap_distribution_windowed (Fensterstabilität)" << endl;
    cout << "  - Erhöhe num_trials für stabilere Cramér-Statistik" << endl;
    cout << "  - Teste mit verschiedenen Limits" << endl;
    cout << string(80, '=') << endl;
    
    return 0;
}
