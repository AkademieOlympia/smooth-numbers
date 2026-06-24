/*
 * Gap Distribution Windowed Analysis
 * 
 * Testet die Stabilität der Gap-Asymmetrie P(g mod 12 | a) über verschiedene
 * Primzahlfenster [10^k, 10^(k+1)].
 * 
 * Dies ist der KRITISCHSTE TEST des gesamten Projekts:
 * - Falls R_gap(k) → 1: Endlichkeitseffekt, Phänomen verschwindet
 * - Falls R_gap(k) → c > 1: Persistente Asymmetrie, fundamental
 * - Falls R_gap(k) oszilliert: Prime-Race-artiges Verhalten
 * 
 * Autor: Thomas Hoffbauer
 * Datum: Juni 2026
 */

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <iomanip>
#include <string>
#include <sstream>
#include <algorithm>

using namespace std;

// EABC-Klassifikation
string classify_prime(long long p) {
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

// Sieb von Eratosthenes für Fenster
vector<long long> sieve_window(long long start, long long end) {
    if (start < 2) start = 2;
    
    long long range = end - start;
    vector<bool> is_prime(range, true);
    
    // Markiere Vielfache kleiner Primzahlen
    long long sqrt_end = (long long)sqrt(end) + 1;
    for (long long p = 2; p <= sqrt_end; p++) {
        // Finde erstes Vielfaches von p in [start, end)
        long long first_multiple = ((start + p - 1) / p) * p;
        if (first_multiple == p) first_multiple += p;  // p selbst nicht markieren
        
        for (long long j = first_multiple; j < end; j += p) {
            if (j >= start) {
                is_prime[j - start] = false;
            }
        }
    }
    
    vector<long long> primes;
    for (long long i = 0; i < range; i++) {
        if (is_prime[i]) {
            long long candidate = start + i;
            if (candidate >= start && candidate < end) {
                primes.push_back(candidate);
            }
        }
    }
    
    return primes;
}

// Gap-Verteilung für ein Fenster berechnen
struct WindowGapStats {
    long long window_start;
    long long window_end;
    long long num_primes;
    
    // gap_counts[start_class][gap_mod_12] = count
    map<string, map<int, int>> gap_counts;
    
    // Ratios für jede Startklasse
    map<string, double> ratio_2_4_vs_8_10;
    
    void compute_ratios() {
        vector<string> classes = {"E", "A", "B", "C"};
        
        for (const auto& cls : classes) {
            if (gap_counts[cls].empty()) continue;
            
            double sum_2_4 = gap_counts[cls][2] + gap_counts[cls][4];
            double sum_8_10 = gap_counts[cls][8] + gap_counts[cls][10];
            
            if (sum_8_10 > 0) {
                ratio_2_4_vs_8_10[cls] = sum_2_4 / sum_8_10;
            } else {
                ratio_2_4_vs_8_10[cls] = 0.0;
            }
        }
    }
    
    double get_geometric_mean_ratio() const {
        double product = 1.0;
        int count = 0;
        
        for (const auto& [cls, ratio] : ratio_2_4_vs_8_10) {
            if (ratio > 0) {
                product *= ratio;
                count++;
            }
        }
        
        return (count > 0) ? pow(product, 1.0 / count) : 0.0;
    }
};

WindowGapStats analyze_window(long long start, long long end) {
    WindowGapStats stats;
    stats.window_start = start;
    stats.window_end = end;
    
    cout << "Analysiere Fenster [" << start << ", " << end << ")..." << endl;
    
    vector<long long> primes = sieve_window(start, end);
    stats.num_primes = primes.size();
    
    if (primes.size() < 2) {
        cout << "  Zu wenige Primzahlen im Fenster!" << endl;
        return stats;
    }
    
    cout << "  Gefunden: " << primes.size() << " Primzahlen" << endl;
    
    // Gap-Verteilung berechnen
    for (size_t i = 0; i < primes.size() - 1; i++) {
        long long p = primes[i];
        long long q = primes[i + 1];
        long long gap = q - p;
        
        string cls = classify_prime(p);
        if (cls == "2" || cls == "3" || cls == "X") continue;
        
        int gap_mod = gap % 12;
        stats.gap_counts[cls][gap_mod]++;
    }
    
    stats.compute_ratios();
    
    return stats;
}

void print_window_stats(const WindowGapStats& stats) {
    cout << "\n=== Fenster [" << stats.window_start << ", " << stats.window_end << ") ===" << endl;
    cout << "Primzahlen: " << stats.num_primes << endl;
    cout << "\nRatios P(g≡2,4) / P(g≡8,10):" << endl;
    cout << string(50, '-') << endl;
    
    vector<string> classes = {"E", "A", "B", "C"};
    
    for (const auto& cls : classes) {
        if (stats.gap_counts.find(cls) != stats.gap_counts.end()) {
            const auto& counts = stats.gap_counts.at(cls);
            
            int sum_2_4 = (counts.count(2) ? counts.at(2) : 0) + 
                          (counts.count(4) ? counts.at(4) : 0);
            int sum_8_10 = (counts.count(8) ? counts.at(8) : 0) + 
                           (counts.count(10) ? counts.at(10) : 0);
            
            double ratio = stats.ratio_2_4_vs_8_10.count(cls) ? 
                          stats.ratio_2_4_vs_8_10.at(cls) : 0.0;
            
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
         << stats.get_geometric_mean_ratio() << endl;
}

void print_comparison_table(const vector<WindowGapStats>& windows) {
    cout << "\n" << string(80, '=') << endl;
    cout << "FENSTERSTABILITÄTSANALYSE" << endl;
    cout << string(80, '=') << endl;
    
    // Header
    cout << "\nWindow         ";
    vector<string> classes = {"E", "A", "B", "C"};
    for (const auto& cls : classes) {
        cout << setw(8) << cls;
    }
    cout << setw(10) << "Geom.Mean" << endl;
    cout << string(80, '-') << endl;
    
    // Daten
    for (const auto& stats : windows) {
        // Window-Bereich als [10^k, 10^(k+1)]
        int k = (int)log10(stats.window_start);
        cout << "[10^" << k << ", 10^" << (k+1) << "]  ";
        
        for (const auto& cls : classes) {
            double ratio = stats.ratio_2_4_vs_8_10.count(cls) ? 
                          stats.ratio_2_4_vs_8_10.at(cls) : 0.0;
            cout << fixed << setprecision(3) << setw(8) << ratio;
        }
        
        cout << fixed << setprecision(3) << setw(10) 
             << stats.get_geometric_mean_ratio() << endl;
    }
    
    cout << string(80, '-') << endl;
    
    // Trend-Analyse
    cout << "\nTREND-ANALYSE:" << endl;
    
    if (windows.size() >= 2) {
        double first_mean = windows.front().get_geometric_mean_ratio();
        double last_mean = windows.back().get_geometric_mean_ratio();
        double change = last_mean - first_mean;
        double percent_change = (first_mean > 0) ? (change / first_mean * 100) : 0;
        
        cout << "Erstes Fenster: " << fixed << setprecision(3) << first_mean << endl;
        cout << "Letztes Fenster: " << fixed << setprecision(3) << last_mean << endl;
        cout << "Änderung: " << showpos << fixed << setprecision(3) << change 
             << " (" << percent_change << "%)" << noshowpos << endl;
        
        cout << "\nINTERPRETATION:" << endl;
        if (abs(percent_change) < 5) {
            cout << "✓ STABIL: Ratio bleibt nahezu konstant" << endl;
            cout << "  → Gap-Asymmetrie persistiert über Größenordnungen" << endl;
        } else if (change < 0 && abs(percent_change) > 20) {
            cout << "⚠ FALLEND: Ratio nimmt signifikant ab" << endl;
            cout << "  → Möglicher Trend zu R → 1 (Vorasymptotik)" << endl;
        } else if (change > 0) {
            cout << "↗ STEIGEND: Ratio nimmt zu" << endl;
            cout << "  → Unerwartetes Verhalten, weitere Analyse nötig" << endl;
        } else {
            cout << "≈ LEICHT FALLEND: Moderate Abnahme" << endl;
            cout << "  → Weiteres Monitoring bis 10^8 empfohlen" << endl;
        }
    }
    
    // Klassen-spezifische Trends
    cout << "\nKLASSEN-SPEZIFISCHE TRENDS:" << endl;
    for (const auto& cls : classes) {
        cout << "\n" << cls << ": ";
        
        vector<double> ratios;
        for (const auto& stats : windows) {
            if (stats.ratio_2_4_vs_8_10.count(cls)) {
                ratios.push_back(stats.ratio_2_4_vs_8_10.at(cls));
            }
        }
        
        if (ratios.size() >= 2) {
            double first = ratios.front();
            double last = ratios.back();
            double change = last - first;
            
            cout << fixed << setprecision(3) << first << " → " << last;
            cout << " (" << showpos << change << noshowpos << ")";
            
            if (abs(change) < 0.1) {
                cout << " [stabil]";
            } else if (change < 0) {
                cout << " [fallend]";
            } else {
                cout << " [steigend]";
            }
        }
    }
    
    cout << "\n" << endl;
}

int main(int argc, char* argv[]) {
    cout << "=== GAP DISTRIBUTION WINDOWED ANALYSIS ===" << endl;
    cout << "Der kritischste Test für EABC-Persistenz" << endl;
    cout << endl;
    
    // Standard-Fenster: [10^k, 10^(k+1)] für k = 3,4,5,6
    vector<pair<long long, long long>> default_windows = {
        {1000, 10000},          // 10^3 - 10^4
        {10000, 100000},        // 10^4 - 10^5
        {100000, 1000000},      // 10^5 - 10^6
        {1000000, 10000000}     // 10^6 - 10^7
    };
    
    // Parse command line arguments
    vector<pair<long long, long long>> windows;
    
    if (argc == 1) {
        // Default: Alle Fenster bis 10^6
        windows = {default_windows[0], default_windows[1], default_windows[2]};
        cout << "Verwende Standard-Fenster bis 10^6" << endl;
        cout << "Für größere Fenster: " << argv[0] << " --large" << endl;
        cout << endl;
    } else if (argc == 2 && string(argv[1]) == "--large") {
        windows = default_windows;
        cout << "Analysiere ALLE Fenster bis 10^7 (WARNUNG: Rechenintensiv!)" << endl;
        cout << endl;
    } else if (argc == 3) {
        // Custom window: start end
        long long start = stoll(argv[1]);
        long long end = stoll(argv[2]);
        windows.push_back({start, end});
        cout << "Benutzerdefiniertes Fenster: [" << start << ", " << end << ")" << endl;
        cout << endl;
    } else {
        cout << "Verwendung:" << endl;
        cout << "  " << argv[0] << "              # Standard bis 10^6" << endl;
        cout << "  " << argv[0] << " --large      # Bis 10^7 (langsam)" << endl;
        cout << "  " << argv[0] << " <start> <end> # Eigenes Fenster" << endl;
        return 1;
    }
    
    // Analyse durchführen
    vector<WindowGapStats> results;
    
    for (const auto& [start, end] : windows) {
        WindowGapStats stats = analyze_window(start, end);
        print_window_stats(stats);
        results.push_back(stats);
        cout << endl;
    }
    
    // Vergleichstabelle
    if (results.size() > 1) {
        print_comparison_table(results);
    }
    
    // Kritische Bewertung
    cout << string(80, '=') << endl;
    cout << "KRITISCHE BEWERTUNG" << endl;
    cout << string(80, '=') << endl;
    
    if (results.size() >= 2) {
        double last_mean = results.back().get_geometric_mean_ratio();
        
        cout << "\nAktueller Status (letztes Fenster): R_gap = " 
             << fixed << setprecision(3) << last_mean << endl;
        
        if (last_mean > 1.2) {
            cout << "\n✓ SIGNIFIKANTE ASYMMETRIE BESTÄTIGT" << endl;
            cout << "  Die Gap-Verteilung zeigt persistente Asymmetrie." << endl;
            cout << "  P(g≡2,4) > P(g≡8,10) ist robust über Größenordnungen." << endl;
            cout << "\n  NÄCHSTER SCHRITT: Cramér-Nullmodell zum Vergleich" << endl;
        } else if (last_mean > 1.05) {
            cout << "\n≈ SCHWACHE ASYMMETRIE" << endl;
            cout << "  Trend deutet auf R → 1, aber noch nicht verschwindend." << endl;
            cout << "\n  NÄCHSTER SCHRITT: Erweitere bis 10^7 oder 10^8" << endl;
        } else {
            cout << "\n✗ ASYMMETRIE VERSCHWINDET" << endl;
            cout << "  Gap-Verteilung konvergiert zur Symmetrie." << endl;
            cout << "  Das Phänomen ist wahrscheinlich ein Endlichkeitseffekt." << endl;
            cout << "\n  KONSEQUENZ: EABC-Chiralität ist Vorasymptotik" << endl;
        }
    }
    
    cout << "\n" << string(80, '=') << endl;
    cout << "Für weitere Analysen siehe:" << endl;
    cout << "  - cramer_comparison.cpp (Cramér-Nullmodell)" << endl;
    cout << "  - ratio_asymptotic.cpp (R(X) Langzeitverhalten)" << endl;
    cout << string(80, '=') << endl;
    
    return 0;
}
