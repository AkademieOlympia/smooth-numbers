// Nullmodell-Hierarchie: R_Poisson, R_Cramér, R_Prime
// 
// Dieser Test ist der derzeit interessanteste des gesamten Projekts.
//
// Hypothese: Falls R_Poisson > R_Cramér > R_Prime,
// dann wirkt die Primzahlstruktur regularisierend, nicht erzeugend.
//
// Drei Nullmodelle:
// 1. Poisson-Prozess: Maximale Zufälligkeit (unkorrelierte Dünnheit)
// 2. Cramér-Modell: Logarithmische Dichte, keine Siebstruktur
// 3. Echte Primzahlen: Volle arithmetische Korrelationen
//
// Für alle drei Modelle:
// - Identische Stichprobengröße
// - Identische mod-12-Auswertung
// - Identische Gap-Asymmetrie-Messung
//
// Erwartetes Resultat:
// R_Poisson > R_Cramér > R_Prime
//
// Interpretation:
// Die arithmetischen Korrelationen der Primzahlen schwächen
// die durch Dünnheit erzeugte Asymmetrie ab.

#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <algorithm>
#include <iomanip>
#include <map>

using namespace std;

// EABC-Klassifikation modulo 12
char classify_prime(long long p) {
    int mod = p % 12;
    if (mod == 1) return 'E';
    if (mod == 5) return 'A';
    if (mod == 7) return 'B';
    if (mod == 11) return 'C';
    return '?';
}

// Sieb von Eratosthenes für echte Primzahlen
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
    primes.push_back(2);
    primes.push_back(3);
    for (long long i = 5; i <= limit; i += 2) {
        if (is_prime[i]) primes.push_back(i);
    }
    
    return primes;
}

// Cramér-Modell: Zufällige Menge mit logarithmischer Dichte
vector<long long> generate_cramer_primes(long long limit, unsigned int seed) {
    vector<long long> cramer_primes;
    mt19937 gen(seed);
    uniform_real_distribution<> dis(0.0, 1.0);
    
    cramer_primes.push_back(2);
    cramer_primes.push_back(3);
    
    for (long long n = 5; n <= limit; n += 2) {
        double prob = 1.0 / log(n);
        if (dis(gen) < prob) {
            cramer_primes.push_back(n);
        }
    }
    
    return cramer_primes;
}

// Poisson-Prozess: Unkorrelierte Dünnheit mit mittlerer Primdichte
vector<long long> generate_poisson_sequence(long long limit, unsigned int seed) {
    vector<long long> poisson_seq;
    mt19937 gen(seed);
    
    // Mittlere Gap-Größe bei echten Primzahlen: ln(n)
    // Wir generieren eine Poisson-Punktfolge mit dieser Rate
    
    poisson_seq.push_back(2);
    poisson_seq.push_back(3);
    
    long long current = 5;
    while (current <= limit) {
        // Mittlerer Gap bei current: log(current)
        double lambda = log(current);
        exponential_distribution<> exp_dist(1.0 / lambda);
        
        double gap = exp_dist(gen);
        current += static_cast<long long>(gap);
        
        // Nur ungerade Zahlen
        if (current % 2 == 0) current++;
        
        if (current <= limit) {
            poisson_seq.push_back(current);
        }
    }
    
    return poisson_seq;
}

// Gap-Statistik für eine Zahlenfolge
struct GapStats {
    string label;
    int count;
    
    // Bedingte Gap-Verteilung: P(g mod 12 | start_class)
    map<char, map<int, int>> cond_gap_dist;  // [class][gap_mod_12] -> count
    map<char, int> class_count;               // [class] -> total count
    
    // Gap-Asymmetrie-Ratios
    map<char, double> ratio_2_4_vs_8_10;      // P(g≡2,4) / P(g≡8,10) für jede Klasse
    
    // Geometrisches Mittel der Ratios
    double geom_mean_ratio;
    
    GapStats(const string& lbl) : label(lbl), count(0), geom_mean_ratio(1.0) {}
};

GapStats analyze_gaps(const vector<long long>& sequence, const string& label) {
    GapStats stats(label);
    
    // Initialisiere Zähler
    for (char c : {'E', 'A', 'B', 'C'}) {
        stats.class_count[c] = 0;
        for (int g = 0; g < 12; ++g) {
            stats.cond_gap_dist[c][g] = 0;
        }
    }
    
    // Zähle Gaps
    for (size_t i = 0; i < sequence.size() - 1; ++i) {
        long long p1 = sequence[i];
        long long p2 = sequence[i + 1];
        
        if (p1 <= 3 || p2 <= 3) continue;  // Überspringe 2, 3
        
        char class1 = classify_prime(p1);
        if (class1 == '?') continue;
        
        long long gap = p2 - p1;
        int gap_mod_12 = gap % 12;
        
        stats.cond_gap_dist[class1][gap_mod_12]++;
        stats.class_count[class1]++;
        stats.count++;
    }
    
    // Berechne Gap-Asymmetrie-Ratios für jede Klasse
    double product = 1.0;
    int valid_ratios = 0;
    
    for (char c : {'E', 'A', 'B', 'C'}) {
        int total = stats.class_count[c];
        if (total == 0) continue;
        
        int count_2_4 = stats.cond_gap_dist[c][2] + stats.cond_gap_dist[c][4];
        int count_8_10 = stats.cond_gap_dist[c][8] + stats.cond_gap_dist[c][10];
        
        if (count_8_10 > 0) {
            double ratio = static_cast<double>(count_2_4) / count_8_10;
            stats.ratio_2_4_vs_8_10[c] = ratio;
            product *= ratio;
            valid_ratios++;
        }
    }
    
    // Geometrisches Mittel
    if (valid_ratios > 0) {
        stats.geom_mean_ratio = pow(product, 1.0 / valid_ratios);
    }
    
    return stats;
}

void print_gap_stats(const GapStats& stats) {
    cout << "\n=== " << stats.label << " ===" << endl;
    cout << "Anzahl Gaps (p > 3): " << stats.count << endl;
    
    cout << "\nBedingte Gap-Verteilung P(g mod 12 | start_class):\n";
    cout << "       ";
    for (int g = 0; g < 12; ++g) {
        cout << setw(6) << g;
    }
    cout << endl;
    
    for (char c : {'E', 'A', 'B', 'C'}) {
        cout << "  " << c << " (" << setw(2) << (c == 'E' ? 1 : c == 'A' ? 5 : c == 'B' ? 7 : 11) << "): ";
        
        int total = stats.class_count.at(c);
        if (total == 0) {
            cout << " (keine Daten)" << endl;
            continue;
        }
        
        for (int g = 0; g < 12; ++g) {
            double prob = 100.0 * stats.cond_gap_dist.at(c).at(g) / total;
            cout << fixed << setprecision(1) << setw(5) << prob << "%";
        }
        cout << endl;
    }
    
    cout << "\nGap-Asymmetrie: P(g≡2,4) vs. P(g≡8,10):\n";
    for (char c : {'E', 'A', 'B', 'C'}) {
        if (stats.ratio_2_4_vs_8_10.count(c) == 0) continue;
        
        cout << "  " << c << " (" << setw(2) << (c == 'E' ? 1 : c == 'A' ? 5 : c == 'B' ? 7 : 11) << "): ";
        
        int total = stats.class_count.at(c);
        int count_2_4 = stats.cond_gap_dist.at(c).at(2) + stats.cond_gap_dist.at(c).at(4);
        int count_8_10 = stats.cond_gap_dist.at(c).at(8) + stats.cond_gap_dist.at(c).at(10);
        
        double prob_2_4 = 100.0 * count_2_4 / total;
        double prob_8_10 = 100.0 * count_8_10 / total;
        double ratio = stats.ratio_2_4_vs_8_10.at(c);
        
        cout << "P(2,4)=" << fixed << setprecision(1) << setw(5) << prob_2_4 << "%  ";
        cout << "P(8,10)=" << fixed << setprecision(1) << setw(5) << prob_8_10 << "%  ";
        cout << "Ratio=" << fixed << setprecision(3) << setw(6) << ratio << endl;
    }
    
    cout << "\n→ Geometrisches Mittel: R_gap = " << fixed << setprecision(3) 
         << stats.geom_mean_ratio << endl;
}

void print_hierarchy_comparison(const GapStats& poisson, const GapStats& cramer, const GapStats& real) {
    cout << "\n╔════════════════════════════════════════════════════════════╗" << endl;
    cout << "║     NULLMODELL-HIERARCHIE: R_Poisson, R_Cramér, R_Prime   ║" << endl;
    cout << "╚════════════════════════════════════════════════════════════╝" << endl;
    
    cout << "\nHYPOTHESE: R_Poisson > R_Cramér > R_Prime" << endl;
    cout << "\n(Falls erfüllt: Primzahlstruktur wirkt regularisierend)\n" << endl;
    
    cout << "Modell              | Stichprobe | R_gap    | Interpretation" << endl;
    cout << "--------------------+------------+----------+-----------------------------------" << endl;
    
    cout << "Poisson-Prozess     | " << setw(10) << poisson.count 
         << " | " << fixed << setprecision(3) << setw(8) << poisson.geom_mean_ratio 
         << " | Maximale Zufälligkeit (unkorreliert)" << endl;
    
    cout << "Cramér-Modell       | " << setw(10) << cramer.count 
         << " | " << fixed << setprecision(3) << setw(8) << cramer.geom_mean_ratio 
         << " | Logarithmische Dichte, keine Siebstruktur" << endl;
    
    cout << "Echte Primzahlen    | " << setw(10) << real.count 
         << " | " << fixed << setprecision(3) << setw(8) << real.geom_mean_ratio 
         << " | Volle arithmetische Korrelationen" << endl;
    
    cout << "\n─────────────────────────────────────────────────────────────" << endl;
    
    // Überprüfe Hierarchie
    bool poisson_gt_cramer = poisson.geom_mean_ratio > cramer.geom_mean_ratio;
    bool cramer_gt_real = cramer.geom_mean_ratio > real.geom_mean_ratio;
    bool hierarchy_holds = poisson_gt_cramer && cramer_gt_real;
    
    cout << "\nHierarchie-Test:" << endl;
    cout << "  R_Poisson > R_Cramér?   " << (poisson_gt_cramer ? "✓ JA" : "✗ NEIN") 
         << "  (Δ = " << showpos << fixed << setprecision(3) 
         << (poisson.geom_mean_ratio - cramer.geom_mean_ratio) << noshowpos << ")" << endl;
    
    cout << "  R_Cramér > R_Prime?     " << (cramer_gt_real ? "✓ JA" : "✗ NEIN") 
         << "  (Δ = " << showpos << fixed << setprecision(3) 
         << (cramer.geom_mean_ratio - real.geom_mean_ratio) << noshowpos << ")" << endl;
    
    cout << "\n─────────────────────────────────────────────────────────────" << endl;
    
    if (hierarchy_holds) {
        cout << "\n✓ HIERARCHIE ERFÜLLT: R_Poisson > R_Cramér > R_Prime\n" << endl;
        
        double reduction_cramer = 100.0 * (1.0 - cramer.geom_mean_ratio / poisson.geom_mean_ratio);
        double reduction_prime = 100.0 * (1.0 - real.geom_mean_ratio / cramer.geom_mean_ratio);
        double reduction_total = 100.0 * (1.0 - real.geom_mean_ratio / poisson.geom_mean_ratio);
        
        cout << "Regularisierungseffekte:" << endl;
        cout << "  Poisson → Cramér: " << fixed << setprecision(1) << reduction_cramer 
             << "% Reduktion (Logarithmische Dichte)" << endl;
        cout << "  Cramér → Prime:   " << fixed << setprecision(1) << reduction_prime 
             << "% Reduktion (Siebstruktur)" << endl;
        cout << "  Poisson → Prime:  " << fixed << setprecision(1) << reduction_total 
             << "% Gesamtreduktion" << endl;
        
        cout << "\n═════════════════════════════════════════════════════════════" << endl;
        cout << "INTERPRETATION:" << endl;
        cout << "═════════════════════════════════════════════════════════════" << endl;
        cout << "\nDie Primzahlstruktur wirkt REGULARISIEREND, nicht erzeugend.\n" << endl;
        cout << "Die Asymmetrie entsteht durch:" << endl;
        cout << "  1. Dünnheit der Menge (Poisson: maximaler Effekt)" << endl;
        cout << "  2. Logarithmische Dichte (Cramér: reduziert)" << endl;
        cout << "  3. Arithmetische Korrelationen (Prime: weiter reduziert)" << endl;
        cout << "\nDies ist der interessanteste Befund des gesamten Projekts." << endl;
        cout << "═════════════════════════════════════════════════════════════\n" << endl;
    } else if (poisson_gt_cramer && !cramer_gt_real) {
        cout << "\n⚠ TEILWEISE ERFÜLLT: R_Poisson > R_Cramér, aber R_Cramér ≯ R_Prime\n" << endl;
        cout << "Interpretation: Die Siebstruktur verstärkt die Asymmetrie im" << endl;
        cout << "Vergleich zum reinen Cramér-Modell.\n" << endl;
    } else {
        cout << "\n✗ HIERARCHIE NICHT ERFÜLLT\n" << endl;
        cout << "Interpretation: Die Primzahlstruktur verhält sich anders als" << endl;
        cout << "die einfache Regularisierungs-Hypothese vorhersagt.\n" << endl;
    }
}

int main(int argc, char* argv[]) {
    long long limit = 100000;
    unsigned int seed = 42;
    
    if (argc > 1) {
        limit = atoll(argv[1]);
    }
    if (argc > 2) {
        seed = static_cast<unsigned int>(atoi(argv[2]));
    }
    
    cout << "╔════════════════════════════════════════════════════════════╗" << endl;
    cout << "║  NULLMODELL-HIERARCHIE FÜR GAP-ASYMMETRIE MOD 12          ║" << endl;
    cout << "╚════════════════════════════════════════════════════════════╝" << endl;
    cout << "\nParametro:" << endl;
    cout << "  Limit: " << limit << endl;
    cout << "  Seed:  " << seed << endl;
    
    // Generiere drei Sequenzen
    cout << "\n[1/3] Generiere echte Primzahlen..." << endl;
    vector<long long> real_primes = sieve_primes(limit);
    cout << "      → " << real_primes.size() << " Primzahlen gefunden" << endl;
    
    cout << "[2/3] Generiere Cramér-Modell..." << endl;
    vector<long long> cramer_primes = generate_cramer_primes(limit, seed);
    cout << "      → " << cramer_primes.size() << " Cramér-Punkte generiert" << endl;
    
    cout << "[3/3] Generiere Poisson-Prozess..." << endl;
    vector<long long> poisson_seq = generate_poisson_sequence(limit, seed + 1);
    cout << "      → " << poisson_seq.size() << " Poisson-Punkte generiert" << endl;
    
    // Analysiere Gap-Verteilungen
    cout << "\nAnalysiere Gap-Verteilungen..." << endl;
    GapStats real_stats = analyze_gaps(real_primes, "ECHTE PRIMZAHLEN");
    GapStats cramer_stats = analyze_gaps(cramer_primes, "CRAMÉR-MODELL");
    GapStats poisson_stats = analyze_gaps(poisson_seq, "POISSON-PROZESS");
    
    // Zeige Detailergebnisse
    print_gap_stats(real_stats);
    print_gap_stats(cramer_stats);
    print_gap_stats(poisson_stats);
    
    // Vergleiche Hierarchie
    print_hierarchy_comparison(poisson_stats, cramer_stats, real_stats);
    
    return 0;
}
