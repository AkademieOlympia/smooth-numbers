/**
 * ÜBERGANGSMATRIX-ANALYSE FÜR EABC-RESTKLASSEN
 * 
 * Der wichtigste theoretische Schritt:
 * 
 * Berechne die 4×4 Übergangsmatrix
 * M = (P(a → b))_{a,b ∈ {E,A,B,C}}
 * 
 * wobei P(a → b) = P(p_{n+1} ≡ b mod 12 | p_n ≡ a mod 12)
 * 
 * Kritische Fragen:
 * 1. Ist M symmetrisch oder asymmetrisch?
 * 2. Was ist die stationäre Verteilung?
 * 3. Erklärt M den beobachteten Chiralitätsbias?
 * 
 * Falls M asymmetrische Struktur zeigt, könnte der gesamte
 * Orientierungsbias H_C(X) als Konsequenz dieser Markov-Dynamik
 * verstanden werden.
 */

#include <iostream>
#include <vector>
#include <map>
#include <iomanip>
#include <cmath>
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

char klasse_zeichen(Klasse k) {
    switch (k) {
        case Klasse::E: return 'E';
        case Klasse::A: return 'A';
        case Klasse::B: return 'B';
        case Klasse::C: return 'C';
        default: return '?';
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

// ========== Übergangsmatrix ==========

struct Uebergangsmatrix {
    int counts[4][4]; // counts[a][b] = Anzahl Übergänge a → b
    int row_totals[4]; // Gesamtzahl Übergänge von a
    
    Uebergangsmatrix() {
        for (int i = 0; i < 4; i++) {
            row_totals[i] = 0;
            for (int j = 0; j < 4; j++) {
                counts[i][j] = 0;
            }
        }
    }
    
    void addiere_uebergang(Klasse von, Klasse nach) {
        if (von == Klasse::Sonder || nach == Klasse::Sonder) return;
        
        int a = static_cast<int>(von);
        int b = static_cast<int>(nach);
        
        counts[a][b]++;
        row_totals[a]++;
    }
    
    double P(int a, int b) const {
        if (row_totals[a] == 0) return 0;
        return (double)counts[a][b] / row_totals[a];
    }
    
    void ausgabe() const {
        cout << "\n╔════════════════════════════════════════════════════════════╗\n";
        cout << "║  ÜBERGANGSMATRIX P(a → b)                               ║\n";
        cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        cout << "P(p_{n+1} ≡ b | p_n ≡ a):\n\n";
        
        // Header
        cout << "     │";
        for (int j = 0; j < 4; j++) {
            cout << "    " << klasse_name(j) << "   ";
        }
        cout << "│  Total\n";
        cout << "─────┼";
        for (int j = 0; j < 4; j++) cout << "─────────";
        cout << "┼─────────\n";
        
        // Zeilen
        for (int i = 0; i < 4; i++) {
            cout << "  " << klasse_name(i) << "  │";
            for (int j = 0; j < 4; j++) {
                cout << " " << fixed << setprecision(4) << setw(7) << P(i, j);
            }
            cout << " │ " << setw(7) << row_totals[i] << "\n";
        }
        cout << "\n";
    }
    
    void analysiere_symmetrie() const {
        cout << "╔════════════════════════════════════════════════════════════╗\n";
        cout << "║  SYMMETRIE-ANALYSE                                       ║\n";
        cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        double max_asymmetrie = 0;
        int max_i = -1, max_j = -1;
        
        cout << "Asymmetrien |P(a→b) - P(b→a)|:\n\n";
        
        for (int i = 0; i < 4; i++) {
            for (int j = i+1; j < 4; j++) {
                double diff = abs(P(i,j) - P(j,i));
                
                if (diff > 0.01) {
                    cout << "  " << klasse_name(i) << "→" << klasse_name(j) 
                         << " vs " << klasse_name(j) << "→" << klasse_name(i)
                         << ": |" << setprecision(4) << P(i,j) << " - " << P(j,i) 
                         << "| = " << diff;
                    
                    if (diff > 0.02) cout << "  ← signifikant!";
                    cout << "\n";
                }
                
                if (diff > max_asymmetrie) {
                    max_asymmetrie = diff;
                    max_i = i;
                    max_j = j;
                }
            }
        }
        
        cout << "\nMaximale Asymmetrie: " << klasse_name(max_i) << "↔" 
             << klasse_name(max_j) << " = " << setprecision(4) << max_asymmetrie << "\n\n";
        
        if (max_asymmetrie < 0.01) {
            cout << "✓ Matrix ist nahezu symmetrisch\n";
            cout << "  → Keine starke Markov-Asymmetrie sichtbar\n";
        } else if (max_asymmetrie < 0.03) {
            cout << "~ Matrix zeigt schwache Asymmetrien\n";
            cout << "  → Mögliche lokale Korrelationen\n";
        } else {
            cout << "✗ Matrix zeigt deutliche Asymmetrien!\n";
            cout << "  → Starke lokale Restklassenkorrelationen\n";
        }
        
        cout << "\n";
    }
    
    void berechne_stationaere_verteilung() const {
        cout << "╔════════════════════════════════════════════════════════════╗\n";
        cout << "║  STATIONÄRE VERTEILUNG                                   ║\n";
        cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        // Empirische stationäre Verteilung (aus Zeilensummen)
        int total = 0;
        for (int i = 0; i < 4; i++) total += row_totals[i];
        
        cout << "Empirische Verteilung π (aus Primzahlhäufigkeiten):\n\n";
        
        double pi[4];
        for (int i = 0; i < 4; i++) {
            pi[i] = (double)row_totals[i] / total;
            cout << "  π(" << klasse_name(i) << ") = " 
                 << fixed << setprecision(4) << pi[i];
            
            double expected = 0.25; // Uniformverteilung
            double diff = abs(pi[i] - expected);
            if (diff > 0.01) {
                cout << "  (Abweichung: " << setprecision(3) 
                     << (diff * 100) << "%)";
            }
            cout << "\n";
        }
        
        // Test: π·P = π?
        cout << "\nTest der stationären Eigenschaft (π·P = π):\n\n";
        
        double pi_P[4] = {0, 0, 0, 0};
        for (int j = 0; j < 4; j++) {
            for (int i = 0; i < 4; i++) {
                pi_P[j] += pi[i] * P(i, j);
            }
        }
        
        bool is_stationary = true;
        for (int i = 0; i < 4; i++) {
            double diff = abs(pi_P[i] - pi[i]);
            cout << "  (π·P)(" << klasse_name(i) << ") = " 
                 << setprecision(4) << pi_P[i] 
                 << "  vs  π(" << klasse_name(i) << ") = " << pi[i]
                 << "  |diff| = " << setprecision(5) << diff << "\n";
            
            if (diff > 0.001) is_stationary = false;
        }
        
        cout << "\n";
        if (is_stationary) {
            cout << "✓ π ist (näherungsweise) stationär unter P\n";
        } else {
            cout << "✗ π ist NICHT stationär unter P\n";
            cout << "  → Die Verteilung ist noch nicht im Gleichgewicht\n";
        }
        
        cout << "\n";
    }
    
    void analysiere_chiralitaets_verbindung() const {
        cout << "╔════════════════════════════════════════════════════════════╗\n";
        cout << "║  VERBINDUNG ZUM CHIRALITÄTSBIAS                          ║\n";
        cout << "╚════════════════════════════════════════════════════════════╝\n\n";
        
        cout << "Hypothese: Falls Übergänge asymmetrisch sind, könnte dies\n";
        cout << "den beobachteten Orientierungsbias H_C(X) erklären.\n\n";
        
        // Analysiere zyklische Strukturen
        cout << "Zyklische Übergänge (EABC-Orientierung):\n";
        cout << "  E→A: " << setprecision(4) << P(0,1) << "\n";
        cout << "  A→B: " << P(1,2) << "\n";
        cout << "  B→C: " << P(2,3) << "\n";
        cout << "  C→E: " << P(3,0) << "\n";
        double forward_prod = P(0,1) * P(1,2) * P(2,3) * P(3,0);
        cout << "  Produkt: " << setprecision(6) << forward_prod << "\n\n";
        
        cout << "Zyklische Übergänge (ECBA-Orientierung):\n";
        cout << "  E→C: " << setprecision(4) << P(0,3) << "\n";
        cout << "  C→B: " << P(3,2) << "\n";
        cout << "  B→A: " << P(2,1) << "\n";
        cout << "  A→E: " << P(1,0) << "\n";
        double backward_prod = P(0,3) * P(3,2) * P(2,1) * P(1,0);
        cout << "  Produkt: " << setprecision(6) << backward_prod << "\n\n";
        
        double ratio = forward_prod / backward_prod;
        cout << "Verhältnis EABC/ECBA = " << setprecision(4) << ratio << "\n\n";
        
        if (abs(ratio - 1.0) < 0.05) {
            cout << "✓ Zyklische Übergänge sind symmetrisch\n";
            cout << "  → Markov-Struktur allein erklärt den Bias NICHT\n";
            cout << "  → Bias muss aus höherer Ordnung stammen\n";
        } else if (ratio > 1.1) {
            cout << "✗ EABC-Richtung ist bevorzugt!\n";
            cout << "  → Markov-Struktur könnte Bias (teilweise) erklären\n";
        } else {
            cout << "✗ ECBA-Richtung ist bevorzugt!\n";
            cout << "  → Interessant: Widerspruch zum beobachteten Bias?\n";
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
    cout << "║  ÜBERGANGSMATRIX-ANALYSE DER EABC-RESTKLASSEN           ║\n";
    cout << "║  Der wichtigste theoretische Schritt                    ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    cout << "Frage: Erklärt die lokale Markov-Dynamik P(a→b) den\n";
    cout << "       beobachteten Orientierungsbias H_C(X)?\n\n";
    
    cout << "Generiere " << n_primes << " Primzahlen...\n";
    vector<int> primzahlen = erzeuge_primzahlen(n_primes);
    cout << "Fertig. Bereich: 2 bis " << primzahlen.back() << "\n";
    
    // Berechne Übergangsmatrix
    Uebergangsmatrix M;
    
    for (size_t i = 0; i + 1 < primzahlen.size(); i++) {
        Klasse k_current = klassifiziere(primzahlen[i]);
        Klasse k_next = klassifiziere(primzahlen[i+1]);
        
        M.addiere_uebergang(k_current, k_next);
    }
    
    // Ausgaben
    M.ausgabe();
    M.analysiere_symmetrie();
    M.berechne_stationaere_verteilung();
    M.analysiere_chiralitaets_verbindung();
    
    // Zusammenfassung
    cout << "╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  ZUSAMMENFASSUNG                                         ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    cout << "Die Übergangsmatrix P(a→b) beschreibt die lokale Dynamik\n";
    cout << "konsekutiver Primzahl-Restklassen modulo 12.\n\n";
    
    cout << "Kritische Fragen:\n\n";
    cout << "1. Ist P symmetrisch?\n";
    cout << "   → Falls ja: Bias muss aus höherer Ordnung stammen\n";
    cout << "   → Falls nein: Markov-Struktur könnte Bias erklären\n\n";
    
    cout << "2. Ist die Verteilung π stationär?\n";
    cout << "   → Test: π·P = π?\n\n";
    
    cout << "3. Bevorzugt P zyklische EABC- oder ECBA-Pfade?\n";
    cout << "   → Vergleiche Produkte der Übergangswahrscheinlichkeiten\n\n";
    
    cout << "Für größere Datensätze:\n";
    cout << "  ./transition_matrix 1000000\n\n";
    
    return 0;
}
