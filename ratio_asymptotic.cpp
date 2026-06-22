/**
 * ASYMPTOTISCHE ANALYSE VON R(X)
 * 
 * Der kritischste Test: Wie verhält sich das Zyklus-Verhältnis
 * 
 *     R(X) = P(EABC) / P(ECBA)
 * 
 * asymptotisch?
 * 
 * DREI SZENARIEN:
 * 
 * 1. R(X) → 1
 *    → Vorasymptotik-Effekt, verschwindet für große X
 *    → Interessant, aber nicht fundamental
 * 
 * 2. R(X) → c > 1
 *    → Stabile Asymmetrie
 *    → Genuine Struktur in Restklassenübergängen
 * 
 * 3. R(X) oszilliert
 *    → Prime-Race-Phänomen
 *    → Verbindung zu Chebyshev-Bias
 *    → Vermutlich das spannendste Resultat
 * 
 * KRITISCH: Dieser Test entscheidet über die Interpretation
 */

#include <iostream>
#include <vector>
#include <map>
#include <iomanip>
#include <cmath>

using namespace std;

// ========== Primzahl-Funktionen ==========

bool ist_primzahl(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

vector<int> erzeuge_primzahlen(int anzahl) {
    vector<int> primzahlen;
    primzahlen.reserve(anzahl);
    for (int n = 2; primzahlen.size() < (size_t)anzahl; n++) {
        if (ist_primzahl(n)) {
            primzahlen.push_back(n);
        }
    }
    return primzahlen;
}

// ========== EABC-Klassifikation ==========

enum class Klasse { E = 0, A = 1, B = 2, C = 3, Sonder = 4 };

Klasse klassifiziere(int p) {
    if (p == 2 || p == 3) return Klasse::Sonder;
    int rest = p % 12;
    switch (rest) {
        case 1: return Klasse::E;
        case 5: return Klasse::A;
        case 7: return Klasse::B;
        case 11: return Klasse::C;
        default: return Klasse::Sonder;
    }
}

string klasse_name(Klasse k) {
    switch(k) {
        case Klasse::E: return "E";
        case Klasse::A: return "A";
        case Klasse::B: return "B";
        case Klasse::C: return "C";
        default: return "?";
    }
}

// ========== Gap-Statistik ==========

struct GapStatistik {
    map<int, map<int, int>> gap_counts;  // [a][g mod 12] = count
    map<int, int> total;                  // [a] = total count
    
    void addiere(Klasse von, int gap) {
        if (von == Klasse::Sonder) return;
        int a = static_cast<int>(von);
        int g = ((gap % 12) + 12) % 12;
        gap_counts[a][g]++;
        total[a]++;
    }
    
    double P(int a, int g) const {
        auto it_a = gap_counts.find(a);
        if (it_a == gap_counts.end()) return 0;
        auto it_g = it_a->second.find(g);
        if (it_g == it_a->second.end()) return 0;
        auto it_tot = total.find(a);
        if (it_tot == total.end() || it_tot->second == 0) return 0;
        return (double)it_g->second / it_tot->second;
    }
};

// ========== R(X) Messung ==========

struct RMessung {
    int X;
    int n_quadrupel;
    double p_eabc;
    double p_ecba;
    double R;
    
    void ausgabe() const {
        cout << "X = " << setw(7) << X 
             << "  |  N_quad = " << setw(6) << n_quadrupel
             << "  |  P(EABC) = " << fixed << setprecision(6) << p_eabc
             << "  |  P(ECBA) = " << setprecision(6) << p_ecba
             << "  |  R = " << setprecision(4) << R;
    }
};

RMessung berechne_R(const GapStatistik& gaps) {
    RMessung m;
    
    // E→A→B→C→E (EABC)
    double p_E_4 = gaps.P(0, 4);
    double p_A_2 = gaps.P(1, 2);
    double p_B_4 = gaps.P(2, 4);
    double p_C_2 = gaps.P(3, 2);
    m.p_eabc = p_E_4 * p_A_2 * p_B_4 * p_C_2;
    
    // E→C→B→A→E (ECBA)
    double p_E_10 = gaps.P(0, 10);
    double p_C_8 = gaps.P(3, 8);
    double p_B_10 = gaps.P(2, 10);
    double p_A_8 = gaps.P(1, 8);
    m.p_ecba = p_E_10 * p_C_8 * p_B_10 * p_A_8;
    
    // Ratio
    m.R = (m.p_ecba > 1e-15) ? (m.p_eabc / m.p_ecba) : 0.0;
    
    // Total aus Gap-Statistik
    m.n_quadrupel = 0;
    for (const auto& [a, count] : gaps.total) {
        m.n_quadrupel += count;
    }
    
    return m;
}

// ========== Hauptprogramm ==========

int main(int argc, char* argv[]) {
    // Defaultwerte
    vector<int> X_werte = {10000, 50000, 100000, 500000, 1000000};
    
    if (argc > 1) {
        X_werte.clear();
        for (int i = 1; i < argc; i++) {
            X_werte.push_back(atoi(argv[i]));
        }
    }
    
    int max_X = *max_element(X_werte.begin(), X_werte.end());
    
    cout << "\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  ASYMPTOTISCHE ANALYSE VON R(X)                         ║\n";
    cout << "║  Die kritischste Frage                                  ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    cout << "R(X) = P(EABC) / P(ECBA)\n\n";
    
    cout << "Drei mögliche Szenarien:\n\n";
    cout << "  1. R(X) → 1       : Vorasymptotik-Effekt\n";
    cout << "  2. R(X) → c > 1   : Stabile Asymmetrie\n";
    cout << "  3. R(X) oszilliert: Prime-Race-Phänomen\n\n";
    
    cout << "Generiere " << max_X << " Primzahlen...\n";
    vector<int> primes = erzeuge_primzahlen(max_X);
    cout << "Fertig. Bereich: 2 bis " << primes.back() << "\n\n";
    
    cout << "Berechne R(X) für verschiedene X...\n\n";
    
    // Sammle Gap-Daten inkrementell
    GapStatistik gaps;
    
    vector<RMessung> messungen;
    size_t x_idx = 0;
    
    for (size_t i = 0; i + 1 < primes.size() && x_idx < X_werte.size(); i++) {
        Klasse k = klassifiziere(primes[i]);
        int gap = primes[i+1] - primes[i];
        gaps.addiere(k, gap);
        
        // Check ob wir einen Messpunkt erreicht haben
        if ((int)i >= X_werte[x_idx]) {
            RMessung m = berechne_R(gaps);
            m.X = X_werte[x_idx];
            messungen.push_back(m);
            x_idx++;
        }
    }
    
    // Ausgabe
    cout << "═══════════════════════════════════════════════════════════\n";
    cout << "ERGEBNISSE\n";
    cout << "═══════════════════════════════════════════════════════════\n\n";
    
    for (const auto& m : messungen) {
        m.ausgabe();
        cout << "\n";
    }
    
    cout << "\n";
    
    // Trend-Analyse
    if (messungen.size() >= 2) {
        cout << "╔═══════════════════════════════════════════════════════════╗\n";
        cout << "║  TREND-ANALYSE                                           ║\n";
        cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
        
        double R_first = messungen[0].R;
        double R_last = messungen.back().R;
        double delta_R = R_last - R_first;
        double rel_change = (R_first > 0) ? (delta_R / R_first * 100.0) : 0.0;
        
        cout << "R(" << messungen[0].X << ") = " << fixed << setprecision(4) << R_first << "\n";
        cout << "R(" << messungen.back().X << ") = " << setprecision(4) << R_last << "\n";
        cout << "Δ = " << setprecision(4) << delta_R 
             << "  (" << setprecision(2) << rel_change << "%)\n\n";
        
        // Monotonie-Check
        bool monoton_fallend = true;
        bool monoton_steigend = true;
        
        for (size_t i = 1; i < messungen.size(); i++) {
            if (messungen[i].R > messungen[i-1].R) monoton_fallend = false;
            if (messungen[i].R < messungen[i-1].R) monoton_steigend = false;
        }
        
        cout << "Monotonie:\n";
        if (monoton_fallend) {
            cout << "  ↓ Streng monoton fallend\n";
            cout << "  → Hinweis auf R(X) → 1 (Szenario 1)\n";
        } else if (monoton_steigend) {
            cout << "  ↑ Streng monoton steigend\n";
            cout << "  → Hinweis auf R(X) → c > 1 (Szenario 2)\n";
        } else {
            cout << "  ≈ Nicht monoton\n";
            cout << "  → Hinweis auf Oszillation (Szenario 3)\n";
        }
        
        cout << "\n";
        
        // Stabilität
        if (messungen.size() >= 3) {
            double var = 0.0;
            double mean = 0.0;
            for (const auto& m : messungen) {
                mean += m.R;
            }
            mean /= messungen.size();
            
            for (const auto& m : messungen) {
                var += (m.R - mean) * (m.R - mean);
            }
            var /= messungen.size();
            double stddev = sqrt(var);
            double cv = (mean > 0) ? (stddev / mean * 100.0) : 0.0;
            
            cout << "Stabilität:\n";
            cout << "  Mittelwert R̄ = " << fixed << setprecision(4) << mean << "\n";
            cout << "  Standardabw. σ = " << setprecision(4) << stddev << "\n";
            cout << "  Variationskoeff. = " << setprecision(2) << cv << "%\n\n";
            
            if (cv < 5.0) {
                cout << "  ✓ Sehr stabil (CV < 5%)\n";
                cout << "  → Starker Hinweis auf R(X) → c ≈ " << setprecision(3) << mean << " (Szenario 2)\n";
            } else if (cv < 15.0) {
                cout << "  ~ Moderat stabil (CV < 15%)\n";
                cout << "  → Trend nicht eindeutig\n";
            } else {
                cout << "  ✗ Instabil (CV > 15%)\n";
                cout << "  → Oszillation oder Vorasymptotik\n";
            }
        }
        
        cout << "\n";
    }
    
    cout << "╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  INTERPRETATION                                          ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    if (messungen.size() >= 3) {
        double R_last = messungen.back().R;
        
        if (R_last > 3.5 && R_last < 5.0) {
            cout << "VORLÄUFIGE EINSCHÄTZUNG:\n\n";
            cout << "R(X) scheint sich um ~4 zu stabilisieren.\n";
            cout << "Falls dieser Trend für X → 10⁷, 10⁸ anhält:\n";
            cout << "  → Szenario 2: Stabile Asymmetrie\n";
            cout << "  → Genuine Struktur in Restklassenübergängen\n";
            cout << "  → Verbindung zu lokalen Prime-Race-Phänomenen\n\n";
        } else if (R_last < 2.0) {
            cout << "VORLÄUFIGE EINSCHÄTZUNG:\n\n";
            cout << "R(X) nähert sich 1.\n";
            cout << "  → Szenario 1: Vorasymptotik-Effekt\n";
            cout << "  → Bias verschwindet asymptotisch\n";
            cout << "  → Interessanter Kleinzahleneffekt\n\n";
        } else {
            cout << "VORLÄUFIGE EINSCHÄTZUNG:\n\n";
            cout << "Trend noch nicht eindeutig.\n";
            cout << "Benötigt: X = 10⁶, 10⁷, 10⁸\n\n";
        }
    }
    
    cout << "NÄCHSTE SCHRITTE:\n\n";
    cout << "1. Für X = 10⁶, 10⁷ rechnen\n";
    cout << "2. R(X)-Verlauf plotten\n";
    cout << "3. Falls R(X) → c > 1: Verbindung zu Prime Races untersuchen\n";
    cout << "4. Falls R(X) → 1: Geschwindigkeit der Konvergenz messen\n\n";
    
    cout << "Aufruf für größere Bereiche:\n";
    cout << "  ./ratio_asymptotic 10000 100000 1000000\n";
    cout << "  ./ratio_asymptotic 10000 50000 100000 500000 1000000 5000000\n\n";
    
    return 0;
}
