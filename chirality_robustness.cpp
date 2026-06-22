/**
 * EABC-Chiralitäts-Robustheitstests
 * 
 * Kritische Überprüfung der beobachteten ABCEA-Dominanz:
 * 
 * Test A: Zufällige Umordnung derselben Primzahlen
 * Test B: Alternative Quadrupel-Konstruktionen (konsekutive statt "außerhalb Schale")
 * Test C: Andere Moduli (30, 60, 210)
 * Test D: Große Datensätze bis 10⁷ Primzahlen
 * 
 * Ziel: Unterscheiden zwischen echter Chiralitätsasymmetrie und Definitionsartefakt
 */

#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <iomanip>
#include <cmath>
#include <random>
#include <chrono>

using namespace std;

namespace ChiralityRobustness {

// EABC-Klassifikation
enum class Klasse { E, A, B, C, Sonder };

Klasse klassifiziere_mod12(int p) {
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

// Klassifikation für andere Moduli
Klasse klassifiziere_mod30(int p) {
    if (p == 2 || p == 3 || p == 5) return Klasse::Sonder;
    int rest = p % 30;
    // Primitivklassen mod 30: 1,7,11,13,17,19,23,29
    // Gruppiere in 4 Klassen
    if (rest == 1 || rest == 11) return Klasse::E;
    if (rest == 7 || rest == 17) return Klasse::A;
    if (rest == 13 || rest == 23) return Klasse::B;
    if (rest == 19 || rest == 29) return Klasse::C;
    return Klasse::Sonder;
}

Klasse klassifiziere_mod60(int p) {
    if (p <= 5) return Klasse::Sonder;
    int rest = p % 60;
    // Vereinfachte 4-Klassen-Einteilung
    if (rest % 4 == 1) return Klasse::E;
    if (rest % 4 == 3) return Klasse::A;
    if (rest < 30) return Klasse::B;
    return Klasse::C;
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

bool ist_primzahl(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// Quadrupel
struct Quadrupel {
    int p, q, r, s;
    Klasse kp, kq, kr, ks;
    
    bool ist_vollstaendig() const {
        set<Klasse> klassen = {kp, kq, kr, ks};
        return klassen.size() == 4 && 
               klassen.count(Klasse::Sonder) == 0;
    }
    
    string normalisiert() const {
        string sig;
        sig += klasse_zeichen(kp);
        sig += klasse_zeichen(kq);
        sig += klasse_zeichen(kr);
        sig += klasse_zeichen(ks);
        
        // Rotiere bis E am Anfang
        for (int i = 0; i < 4; i++) {
            if (sig[0] == 'E') break;
            sig = sig.substr(1) + sig[0];
        }
        return sig;
    }
    
    // Chiralitäts-Observable χ(Q)
    int chi() const {
        if (!ist_vollstaendig()) return 0;
        string norm = normalisiert();
        if (norm == "EABC") return +1;  // ABCEA-Chiralität
        if (norm == "ECBA") return -1;  // CEABC-Chiralität
        return 0;  // Andere
    }
};

// Statistik
struct ChiralitaetsStatistik {
    int n_total = 0;
    int n_plus = 0;   // EABC
    int n_minus = 0;  // ECBA
    int n_andere = 0;
    
    map<string, int> signaturen;
    
    void aktualisiere(const Quadrupel& q) {
        if (!q.ist_vollstaendig()) return;
        
        n_total++;
        int c = q.chi();
        
        if (c == +1) n_plus++;
        else if (c == -1) n_minus++;
        else n_andere++;
        
        signaturen[q.normalisiert()]++;
    }
    
    // Holonomie-Größe H = Σ χ(Q)
    int holonomie() const {
        return n_plus - n_minus;
    }
    
    // Relative Häufigkeiten
    double p_plus() const { return n_total > 0 ? (double)n_plus / n_total : 0; }
    double p_minus() const { return n_total > 0 ? (double)n_minus / n_total : 0; }
    double p_andere() const { return n_total > 0 ? (double)n_andere / n_total : 0; }
    
    void ausgabe(const string& titel) const {
        cout << "\n=== " << titel << " ===\n";
        cout << "Vollständige Quadrupel: " << n_total << "\n";
        cout << "  EABC (+1): " << n_plus << " (" << fixed << setprecision(1) 
             << (100.0 * p_plus()) << "%)\n";
        cout << "  ECBA (-1): " << n_minus << " (" << (100.0 * p_minus()) << "%)\n";
        cout << "  Andere:    " << n_andere << " (" << (100.0 * p_andere()) << "%)\n";
        
        int H = holonomie();
        cout << "  Holonomie H = N₊ - N₋ = " << H << "\n";
        
        if (n_total > 0) {
            double asymmetrie = (p_plus() - p_minus()) / (p_plus() + p_minus() + 1e-10);
            cout << "  Asymmetrie: " << setprecision(3) << asymmetrie << "\n";
            
            // Bias-Funktionen
            double h = (double)H / n_total;
            double Z = (double)H / sqrt((double)n_total);
            double Z_star = sqrt(3.0) * Z;  // Standardisierter Nullhypothesen-Score
            
            cout << "  Normalisierter Bias h = H/N = " << setprecision(4) << h << "\n";
            cout << "  Skalierter Bias Z = H/√N = " << setprecision(3) << Z << "\n";
            cout << "  Standardisierter Bias Z* = √3·H/√N = " << setprecision(3) << Z_star << "\n";
        }
    }
};

// ========== TEST A: Zufällige Umordnung ==========

ChiralitaetsStatistik test_a_zufaellige_umordnung(int n_primzahlen, int n_permutationen = 1000) {
    cout << "\n╔══════════════════════════════════════════════════════════╗\n";
    cout << "║  TEST A: Zufällige Umordnung derselben Primzahlen      ║\n";
    cout << "╚══════════════════════════════════════════════════════════╝\n";
    cout << "\nZiel: Prüfen ob Chiralität von der gerichteten Ordnung abhängt\n";
    
    // Generiere Primzahlen
    vector<int> primzahlen;
    for (int p = 2; primzahlen.size() < n_primzahlen; p++) {
        if (ist_primzahl(p)) primzahlen.push_back(p);
    }
    
    ChiralitaetsStatistik stats;
    random_device rd;
    mt19937 gen(rd());
    
    // Nimm erste vollständige Quadrupel und permutiere
    for (size_t i = 0; i + 3 < primzahlen.size(); i++) {
        vector<int> quad = {primzahlen[i], primzahlen[i+1], 
                            primzahlen[i+2], primzahlen[i+3]};
        
        // Prüfe ob vollständig
        Quadrupel q_original;
        q_original.p = quad[0]; q_original.q = quad[1];
        q_original.r = quad[2]; q_original.s = quad[3];
        q_original.kp = klassifiziere_mod12(quad[0]);
        q_original.kq = klassifiziere_mod12(quad[1]);
        q_original.kr = klassifiziere_mod12(quad[2]);
        q_original.ks = klassifiziere_mod12(quad[3]);
        
        if (!q_original.ist_vollstaendig()) continue;
        
        // Permutiere n_permutationen mal
        for (int perm = 0; perm < n_permutationen; perm++) {
            shuffle(quad.begin(), quad.end(), gen);
            
            Quadrupel q;
            q.p = quad[0]; q.q = quad[1];
            q.r = quad[2]; q.s = quad[3];
            q.kp = klassifiziere_mod12(quad[0]);
            q.kq = klassifiziere_mod12(quad[1]);
            q.kr = klassifiziere_mod12(quad[2]);
            q.ks = klassifiziere_mod12(quad[3]);
            
            stats.aktualisiere(q);
        }
        
        if (stats.n_total >= 10000) break;  // Genug Samples
    }
    
    stats.ausgabe("TEST A: Zufällige Umordnung");
    
    cout << "\nInterpretation:\n";
    if (abs(stats.p_plus() - stats.p_minus()) < 0.1) {
        cout << "→ ✓ Chiralität ist weitgehend symmetrisch bei zufälliger Ordnung\n";
        cout << "→ Die ursprüngliche Asymmetrie war ein Definitionsartefakt!\n";
    } else {
        cout << "→ ! Asymmetrie bleibt auch bei zufälliger Ordnung erhalten\n";
    }
    
    return stats;
}

// ========== TEST B: Konsekutive Primzahlen ==========

ChiralitaetsStatistik test_b_konsekutive_primzahlen(int max_primzahl) {
    cout << "\n╔══════════════════════════════════════════════════════════╗\n";
    cout << "║  TEST B: Konsekutive Primzahlen (p_n, p_{n+1}, ...)    ║\n";
    cout << "╚══════════════════════════════════════════════════════════╝\n";
    cout << "\nZiel: Alternative Konstruktion ohne 'außerhalb Schale'\n";
    
    vector<int> primzahlen;
    for (int p = 2; p <= max_primzahl; p++) {
        if (ist_primzahl(p)) primzahlen.push_back(p);
    }
    
    ChiralitaetsStatistik stats;
    
    // Bilde konsekutive 4er-Quadrupel
    for (size_t i = 0; i + 3 < primzahlen.size(); i++) {
        Quadrupel q;
        q.p = primzahlen[i];
        q.q = primzahlen[i+1];
        q.r = primzahlen[i+2];
        q.s = primzahlen[i+3];
        q.kp = klassifiziere_mod12(q.p);
        q.kq = klassifiziere_mod12(q.q);
        q.kr = klassifiziere_mod12(q.r);
        q.ks = klassifiziere_mod12(q.s);
        
        stats.aktualisiere(q);
    }
    
    stats.ausgabe("TEST B: Konsekutive Primzahlen");
    
    cout << "\nVergleich mit ursprünglicher Methode:\n";
    cout << "Ursprünglich: EABC ~60%, ECBA ~0%\n";
    cout << "Konsekutiv:   EABC " << (100.0 * stats.p_plus()) << "%, ECBA " 
         << (100.0 * stats.p_minus()) << "%\n";
    
    return stats;
}

// ========== TEST C: Andere Moduli ==========

ChiralitaetsStatistik test_c_andere_moduli(int max_primzahl, int modulus) {
    cout << "\n╔══════════════════════════════════════════════════════════╗\n";
    cout << "║  TEST C: Modulus " << modulus << "                                   ║\n";
    cout << "╚══════════════════════════════════════════════════════════╝\n";
    
    vector<int> primzahlen;
    for (int p = 2; p <= max_primzahl; p++) {
        if (ist_primzahl(p)) primzahlen.push_back(p);
    }
    
    ChiralitaetsStatistik stats;
    
    auto klassifiziere = (modulus == 30) ? klassifiziere_mod30 : 
                         (modulus == 60) ? klassifiziere_mod60 : 
                         klassifiziere_mod12;
    
    for (size_t i = 0; i + 3 < primzahlen.size(); i++) {
        Quadrupel q;
        q.p = primzahlen[i];
        q.q = primzahlen[i+1];
        q.r = primzahlen[i+2];
        q.s = primzahlen[i+3];
        q.kp = klassifiziere(q.p);
        q.kq = klassifiziere(q.q);
        q.kr = klassifiziere(q.r);
        q.ks = klassifiziere(q.s);
        
        stats.aktualisiere(q);
    }
    
    stats.ausgabe("TEST C: Modulus " + to_string(modulus));
    return stats;
}

// ========== TEST D: Große Datensätze ==========

ChiralitaetsStatistik test_d_grosse_datensaetze(int max_primzahl) {
    cout << "\n╔══════════════════════════════════════════════════════════╗\n";
    cout << "║  TEST D: Große Datensätze bis " << max_primzahl << "              ║\n";
    cout << "╚══════════════════════════════════════════════════════════╝\n";
    
    cout << "\nGeneriere Primzahlen... ";
    cout.flush();
    
    auto start = chrono::high_resolution_clock::now();
    
    vector<int> primzahlen;
    for (int p = 2; p <= max_primzahl; p++) {
        if (ist_primzahl(p)) primzahlen.push_back(p);
    }
    
    auto ende = chrono::high_resolution_clock::now();
    auto dauer = chrono::duration_cast<chrono::milliseconds>(ende - start).count();
    
    cout << primzahlen.size() << " Primzahlen in " << dauer << " ms\n";
    
    ChiralitaetsStatistik stats;
    
    cout << "Analysiere Quadrupel...\n";
    
    for (size_t i = 0; i + 3 < primzahlen.size(); i++) {
        Quadrupel q;
        q.p = primzahlen[i];
        q.q = primzahlen[i+1];
        q.r = primzahlen[i+2];
        q.s = primzahlen[i+3];
        q.kp = klassifiziere_mod12(q.p);
        q.kq = klassifiziere_mod12(q.q);
        q.kr = klassifiziere_mod12(q.r);
        q.ks = klassifiziere_mod12(q.s);
        
        stats.aktualisiere(q);
        
        // Progress
        if (i % 10000 == 0 && i > 0) {
            cout << "  " << i << " Quadrupel analysiert...\r";
            cout.flush();
        }
    }
    
    cout << "\n";
    stats.ausgabe("TEST D: Große Datensätze");
    
    // Holonomie-Wachstum
    cout << "\nHolonomie-Observable:\n";
    cout << "  H(X) = Σ χ(Q) = " << stats.holonomie() << "\n";
    cout << "  H(X) / N(X) = " << fixed << setprecision(4) 
         << ((double)stats.holonomie() / stats.n_total) << "\n";
    
    if (abs((double)stats.holonomie() / stats.n_total) > 0.01) {
        cout << "  → Bias bleibt erhalten!\n";
    } else {
        cout << "  → Bias geht gegen 0\n";
    }
    
    return stats;
}

} // namespace ChiralityRobustness

int main() {
    using namespace ChiralityRobustness;
    
    cout << "╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  EABC-CHIRALITÄTS-ROBUSTHEITSTESTS                       ║\n";
    cout << "║  Kritische Überprüfung der ABCEA-Dominanz               ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n";
    
    cout << "\nZiel: Unterscheiden zwischen:\n";
    cout << "  • Echte Chiralitätsasymmetrie der Primzahlen\n";
    cout << "  • Definitionsartefakt durch Konstruktionsmethode\n";
    
    // TEST A
    auto stats_a = test_a_zufaellige_umordnung(100, 1000);
    
    // TEST B
    auto stats_b = test_b_konsekutive_primzahlen(1000);
    
    // TEST C
    auto stats_c30 = test_c_andere_moduli(1000, 30);
    auto stats_c60 = test_c_andere_moduli(1000, 60);
    
    // TEST D - Start klein
    cout << "\n\n*** Starte TEST D mit verschiedenen Größenordnungen ***\n";
    auto stats_d1 = test_d_grosse_datensaetze(10000);
    auto stats_d2 = test_d_grosse_datensaetze(100000);
    
    // Optional: Noch größer (dauert länger)
    cout << "\nFür 10⁷ Primzahlen: Benötigt ~1-2 Minuten\n";
    cout << "Ausführen? (wird übersprungen, kann manuell aktiviert werden)\n";
    // auto stats_d3 = test_d_grosse_datensaetze(10000000);
    
    // ZUSAMMENFASSUNG
    cout << "\n\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  ZUSAMMENFASSUNG                                         ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n";
    
    cout << "\nVERGLEICH DER TESTS:\n\n";
    cout << "Test              | N(X)  | P(EABC) | P(ECBA) | H/N   |\n";
    cout << "------------------|-------|---------|---------|-------|\n";
    
    auto print_row = [](const string& name, const ChiralitaetsStatistik& s) {
        cout << left << setw(18) << name << "| "
             << right << setw(5) << s.n_total << " | "
             << fixed << setprecision(3) << setw(7) << s.p_plus() << " | "
             << setw(7) << s.p_minus() << " | "
             << setw(5) << ((double)s.holonomie() / (s.n_total + 1e-10)) << " |\n";
    };
    
    print_row("A: Zufällig", stats_a);
    print_row("B: Konsekutiv", stats_b);
    print_row("C: Mod 30", stats_c30);
    print_row("C: Mod 60", stats_c60);
    print_row("D: bis 10⁴", stats_d1);
    print_row("D: bis 10⁵", stats_d2);
    
    cout << "\n\nKRITISCHE INTERPRETATION:\n";
    cout << "Falls P(ECBA) ≈ 0 in ALLEN Tests:\n";
    cout << "  → Echte Chiralitätsasymmetrie (neue Mathematik!)\n\n";
    cout << "Falls P(ECBA) ≈ P(EABC) bei zufälliger Ordnung:\n";
    cout << "  → Definitionsartefakt durch gerichtete Konstruktion\n\n";
    cout << "Falls H/N → 0 für große N:\n";
    cout << "  → Bias verschwindet asymptotisch\n\n";
    cout << "Falls H/N ≈ const > 0:\n";
    cout << "  → Persistenter Chiralitäts-Bias!\n";
    
    return 0;
}
