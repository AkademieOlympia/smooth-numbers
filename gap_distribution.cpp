/**
 * GAP-VERTEILUNG UND ÜBERGANGSMATRIX
 * 
 * Die kausale Kette:
 * 
 * Gap-Verteilung P(g mod 12 | p_n ≡ a)
 *     ↓
 * Übergangsmatrix P(a → b) mit b ≡ a + g (mod 12)
 *     ↓
 * Zykluspräferenz EABC vs ECBA
 *     ↓
 * Orientierungsbias H_C(X)
 * 
 * KRITISCHE BEOBACHTUNG:
 * 
 * EABC-Zyklus verwendet:
 *   E→A: g ≡ 4 (mod 12)
 *   A→B: g ≡ 2 (mod 12)
 *   B→C: g ≡ 4 (mod 12)
 *   C→E: g ≡ 2 (mod 12)
 * 
 * ECBA-Zyklus verwendet:
 *   E→C: g ≡ 10 (mod 12)
 *   C→B: g ≡ 8 (mod 12)
 *   B→A: g ≡ 10 (mod 12)
 *   A→E: g ≡ 8 (mod 12)
 * 
 * HYPOTHESE:
 * Falls g ≡ 2,4 (mod 12) häufiger als g ≡ 8,10 (mod 12),
 * dann erklärt dies den EABC-Bias direkt.
 */

#include <iostream>
#include <vector>
#include <map>
#include <iomanip>
#include <string>

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

int klasse_rest(Klasse k) {
    switch (k) {
        case Klasse::E: return 1;
        case Klasse::A: return 5;
        case Klasse::B: return 7;
        case Klasse::C: return 11;
        default: return 0;
    }
}

string klasse_name(int idx) {
    switch(idx) {
        case 0: return "E";
        case 1: return "A";
        case 2: return "B";
        case 3: return "C";
        default: return "?";
    }
}

// ========== Gap-Verteilung ==========

struct GapVerteilung {
    // gap_counts[a][g] = Anzahl Gaps mit g mod 12, startend von Klasse a
    map<int, map<int, int>> gap_counts;
    map<int, int> total_counts;
    
    void addiere_gap(Klasse von, int gap) {
        if (von == Klasse::Sonder) return;
        
        int a = static_cast<int>(von);
        int g_mod = ((gap % 12) + 12) % 12;
        
        gap_counts[a][g_mod]++;
        total_counts[a]++;
    }
    
    double P_gap(int a, int g_mod) const {
        auto it_a = gap_counts.find(a);
        if (it_a == gap_counts.end()) return 0;
        
        auto it_g = it_a->second.find(g_mod);
        if (it_g == it_a->second.end()) return 0;
        
        auto it_tot = total_counts.find(a);
        if (it_tot == total_counts.end() || it_tot->second == 0) return 0;
        
        return (double)it_g->second / it_tot->second;
    }
    
    void ausgabe_gap_verteilung() const {
        cout << "\n╔════════════════════════════════════════════════════════════╗\n";
        cout << "║  GAP-VERTEILUNG P(g mod 12 | p_n ≡ a)                   ║\n";
        cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        cout << "Primzahllücken sind gerade → nur g ∈ {0,2,4,6,8,10} mod 12\n\n";
        
        // Header
        cout << "Start│";
        for (int g = 0; g <= 10; g += 2) {
            cout << "  g≡" << setw(2) << g << "  ";
        }
        cout << "│ Total\n";
        cout << "─────┼";
        for (int g = 0; g <= 10; g += 2) cout << "────────";
        cout << "┼────────\n";
        
        // Zeilen
        for (int a = 0; a < 4; a++) {
            cout << "  " << klasse_name(a) << "  │";
            for (int g = 0; g <= 10; g += 2) {
                double p = P_gap(a, g);
                cout << " " << fixed << setprecision(4) << setw(6) << p;
            }
            
            auto it = total_counts.find(a);
            int total = (it != total_counts.end()) ? it->second : 0;
            cout << " │ " << setw(6) << total << "\n";
        }
        
        cout << "\n";
    }
    
    void analysiere_zyklus_gaps() const {
        cout << "╔════════════════════════════════════════════════════════════╗\n";
        cout << "║  ZYKLISCHE PFADE UND GAP-KLASSEN                         ║\n";
        cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        cout << "EABC-Zyklus (positiv orientiert):\n";
        cout << "  E→A: " << klasse_name(0) << "(" << klasse_rest(Klasse::E) << ") → " 
             << klasse_name(1) << "(" << klasse_rest(Klasse::A) << ")  ⇒  g ≡ 4 (mod 12)  P = " 
             << fixed << setprecision(4) << P_gap(0, 4) << "\n";
        cout << "  A→B: " << klasse_name(1) << "(" << klasse_rest(Klasse::A) << ") → " 
             << klasse_name(2) << "(" << klasse_rest(Klasse::B) << ")  ⇒  g ≡ 2 (mod 12)  P = " 
             << P_gap(1, 2) << "\n";
        cout << "  B→C: " << klasse_name(2) << "(" << klasse_rest(Klasse::B) << ") → " 
             << klasse_name(3) << "(" << klasse_rest(Klasse::C) << ")  ⇒  g ≡ 4 (mod 12)  P = " 
             << P_gap(2, 4) << "\n";
        cout << "  C→E: " << klasse_name(3) << "(" << klasse_rest(Klasse::C) << ") → " 
             << klasse_name(0) << "(" << klasse_rest(Klasse::E) << ")  ⇒  g ≡ 2 (mod 12)  P = " 
             << P_gap(3, 2) << "\n";
        
        double p_eabc = P_gap(0, 4) * P_gap(1, 2) * P_gap(2, 4) * P_gap(3, 2);
        cout << "  Produkt P(EABC) = " << setprecision(6) << p_eabc << "\n\n";
        
        cout << "ECBA-Zyklus (negativ orientiert):\n";
        cout << "  E→C: " << klasse_name(0) << "(" << klasse_rest(Klasse::E) << ") → " 
             << klasse_name(3) << "(" << klasse_rest(Klasse::C) << ")  ⇒  g ≡ 10 (mod 12)  P = " 
             << setprecision(4) << P_gap(0, 10) << "\n";
        cout << "  C→B: " << klasse_name(3) << "(" << klasse_rest(Klasse::C) << ") → " 
             << klasse_name(2) << "(" << klasse_rest(Klasse::B) << ")  ⇒  g ≡ 8 (mod 12)  P = " 
             << P_gap(3, 8) << "\n";
        cout << "  B→A: " << klasse_name(2) << "(" << klasse_rest(Klasse::B) << ") → " 
             << klasse_name(1) << "(" << klasse_rest(Klasse::A) << ")  ⇒  g ≡ 10 (mod 12)  P = " 
             << P_gap(2, 10) << "\n";
        cout << "  A→E: " << klasse_name(1) << "(" << klasse_rest(Klasse::A) << ") → " 
             << klasse_name(0) << "(" << klasse_rest(Klasse::E) << ")  ⇒  g ≡ 8 (mod 12)  P = " 
             << P_gap(1, 8) << "\n";
        
        double p_ecba = P_gap(0, 10) * P_gap(3, 8) * P_gap(2, 10) * P_gap(1, 8);
        cout << "  Produkt P(ECBA) = " << setprecision(6) << p_ecba << "\n\n";
        
        double ratio = p_eabc / p_ecba;
        cout << "═══════════════════════════════════════════════════════════\n";
        cout << "VERHÄLTNIS: P(EABC) / P(ECBA) = " << setprecision(4) << ratio << "\n";
        cout << "═══════════════════════════════════════════════════════════\n\n";
        
        if (ratio > 2.0) {
            cout << "✗ EABC ist stark bevorzugt!\n";
            cout << "  → Gap-Klassen 2,4 sind häufiger/günstiger als 8,10\n";
            cout << "  → Dies erklärt den beobachteten Orientierungsbias\n";
        } else if (ratio > 1.2) {
            cout << "~ EABC ist moderat bevorzugt\n";
            cout << "  → Schwache Gap-Asymmetrie\n";
        } else if (ratio < 0.8) {
            cout << "~ ECBA ist moderat bevorzugt\n";
            cout << "  → Interessant: Widerspruch?\n";
        } else {
            cout << "✓ Zyklen sind näherungsweise symmetrisch\n";
            cout << "  → Bias muss aus höherer Ordnung stammen\n";
        }
        
        cout << "\n";
    }
    
    void analysiere_gap_asymmetrie() const {
        cout << "╔════════════════════════════════════════════════════════════╗\n";
        cout << "║  GAP-ASYMMETRIE: {2,4} vs {8,10}                         ║\n";
        cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        cout << "EABC verwendet g ≡ {2,4}, ECBA verwendet g ≡ {8,10}\n\n";
        
        for (int a = 0; a < 4; a++) {
            double p_2_4 = P_gap(a, 2) + P_gap(a, 4);
            double p_8_10 = P_gap(a, 8) + P_gap(a, 10);
            double ratio = p_2_4 / (p_8_10 + 1e-10);
            
            cout << "Von " << klasse_name(a) << ": P(g≡2,4) = " << fixed << setprecision(4) 
                 << p_2_4 << "  vs  P(g≡8,10) = " << p_8_10 
                 << "  →  Ratio = " << setprecision(3) << ratio;
            
            if (ratio > 1.2) cout << "  ← EABC bevorzugt";
            else if (ratio < 0.8) cout << "  ← ECBA bevorzugt";
            
            cout << "\n";
        }
        
        cout << "\n";
    }
};

// ========== Hauptprogramm ==========

int main(int argc, char* argv[]) {
    int n_primes = 100000;
    
    if (argc > 1) {
        n_primes = atoi(argv[1]);
        if (n_primes < 1000) n_primes = 1000;
        if (n_primes > 10000000) n_primes = 10000000;
    }
    
    cout << "\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  GAP-VERTEILUNG UND ORIENTIERUNGSBIAS                   ║\n";
    cout << "║  Die kausale Kette                                      ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    cout << "Fundamentale Relation: b ≡ a + g (mod 12)\n\n";
    
    cout << "Hypothese: Der EABC-Bias entsteht durch asymmetrische\n";
    cout << "           Gap-Verteilung P(g mod 12 | p_n ≡ a)\n\n";
    
    cout << "Generiere " << n_primes << " Primzahlen...\n";
    vector<int> primzahlen = erzeuge_primzahlen(n_primes);
    cout << "Fertig. Bereich: 2 bis " << primzahlen.back() << "\n";
    
    // Berechne Gap-Verteilung
    GapVerteilung gaps;
    
    for (size_t i = 0; i + 1 < primzahlen.size(); i++) {
        Klasse k_current = klassifiziere(primzahlen[i]);
        int gap = primzahlen[i+1] - primzahlen[i];
        
        gaps.addiere_gap(k_current, gap);
    }
    
    // Ausgaben
    gaps.ausgabe_gap_verteilung();
    gaps.analysiere_gap_asymmetrie();
    gaps.analysiere_zyklus_gaps();
    
    // Finale Zusammenfassung
    cout << "╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  KAUSALE KETTE                                           ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    cout << "1. Primzahllücken g haben eine Verteilung mod 12\n";
    cout << "2. Diese Verteilung hängt von der Startklasse a ab\n";
    cout << "3. Durch b ≡ a + g entsteht die Übergangsmatrix P(a→b)\n";
    cout << "4. EABC benötigt g ≡ {2,4}, ECBA benötigt g ≡ {8,10}\n";
    cout << "5. Falls {2,4} häufiger → EABC-Präferenz → H_C(X) > 0\n\n";
    
    cout << "Nächster theoretischer Schritt:\n";
    cout << "  Warum ist P(g ≡ 2,4) > P(g ≡ 8,10)?\n";
    cout << "  → Vermutung: Siebeffekte durch kleine Primmoduli\n\n";
    
    cout << "Für größere Datensätze:\n";
    cout << "  ./gap_distribution 1000000\n\n";
    
    return 0;
}
