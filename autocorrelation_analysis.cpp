/**
 * AUTOKORRELATIONSANALYSE DER EABC-CHIRALITÄT
 * 
 * Der entscheidende Test:
 * 
 * 1. Berechne ρ(k) = Corr(χ_n, χ_{n+k}) für k = 1,2,3,4
 * 2. Vergleiche überlappende vs. nichtüberlappende Fenster
 * 3. Berechne N_eff = N / (1 + 2·Σ ρ(k))
 * 4. Berechne Z_eff = H / √(N_eff / 3)
 * 
 * Kritische Frage:
 * Bleibt nach Autokorrelationskorrektur ein Bias?
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <string>
#include <algorithm>

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
    for (int n = 2; primzahlen.size() < anzahl; n++) {
        if (ist_primzahl(n)) {
            primzahlen.push_back(n);
        }
    }
    return primzahlen;
}

// ========== EABC-Klassifikation ==========

enum class Klasse { E, A, B, C, Sonder };

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

// ========== Quadrupel ==========

struct Quadrupel {
    int p, q, r, s;
    
    bool ist_vollstaendig() const {
        Klasse kp = klassifiziere(p);
        Klasse kq = klassifiziere(q);
        Klasse kr = klassifiziere(r);
        Klasse ks = klassifiziere(s);
        
        if (kp == Klasse::Sonder || kq == Klasse::Sonder || 
            kr == Klasse::Sonder || ks == Klasse::Sonder) {
            return false;
        }
        
        // Prüfe ob alle vier verschieden sind
        return (kp != kq) && (kp != kr) && (kp != ks) &&
               (kq != kr) && (kq != ks) && (kr != ks);
    }
    
    string signatur() const {
        string sig;
        sig += klasse_zeichen(klassifiziere(p));
        sig += klasse_zeichen(klassifiziere(q));
        sig += klasse_zeichen(klassifiziere(r));
        sig += klasse_zeichen(klassifiziere(s));
        return sig;
    }
    
    string normalisiert() const {
        string sig = signatur();
        
        // Finde Position von 'E'
        int e_pos = -1;
        for (int i = 0; i < 4; i++) {
            if (sig[i] == 'E') {
                e_pos = i;
                break;
            }
        }
        
        if (e_pos == -1) return sig; // Kein E gefunden (sollte nicht passieren)
        
        // Rotiere so dass E am Anfang steht
        string norm;
        for (int i = 0; i < 4; i++) {
            norm += sig[(e_pos + i) % 4];
        }
        
        return norm;
    }
    
    // Chiralitäts-Observable
    int chi() const {
        if (!ist_vollstaendig()) return 0;
        
        string norm = normalisiert();
        if (norm == "EABC") return +1;
        if (norm == "ECBA") return -1;
        return 0;
    }
};

// ========== Statistik-Funktionen ==========

struct Statistik {
    int N = 0;
    int H = 0;
    double mean_chi = 0;
    double var_chi = 0;
};

double berechne_mittelwert(const vector<int>& werte) {
    if (werte.empty()) return 0;
    double summe = 0;
    for (int v : werte) summe += v;
    return summe / werte.size();
}

double berechne_varianz(const vector<int>& werte, double mittelwert) {
    if (werte.empty()) return 0;
    double summe = 0;
    for (int v : werte) {
        double diff = v - mittelwert;
        summe += diff * diff;
    }
    return summe / werte.size();
}

double berechne_autokorrelation(const vector<int>& chi_seq, int lag) {
    int n = chi_seq.size() - lag;
    if (n <= 0) return 0;
    
    // Berechne Mittelwerte
    double mean1 = 0, mean2 = 0;
    for (int i = 0; i < n; i++) {
        mean1 += chi_seq[i];
        mean2 += chi_seq[i + lag];
    }
    mean1 /= n;
    mean2 /= n;
    
    // Berechne Kovarianz
    double cov = 0;
    double var1 = 0, var2 = 0;
    for (int i = 0; i < n; i++) {
        double d1 = chi_seq[i] - mean1;
        double d2 = chi_seq[i + lag] - mean2;
        cov += d1 * d2;
        var1 += d1 * d1;
        var2 += d2 * d2;
    }
    
    // Korrelationskoeffizient
    if (var1 <= 0 || var2 <= 0) return 0;
    return cov / sqrt(var1 * var2);
}

// ========== Hauptanalyse ==========

void analysiere_konstruktion(const string& name, 
                             const vector<Quadrupel>& quadrupel,
                             bool berechne_autokorr = true) {
    cout << "\n╔════════════════════════════════════════════════════════════╗\n";
    cout << "║  " << left << setw(56) << name << " ║\n";
    cout << "╚════════════════════════════════════════════════════════════╝\n\n";
    
    // Filtere vollständige Quadrupel und berechne χ-Sequenz
    vector<Quadrupel> vollstaendig;
    vector<int> chi_seq;
    
    for (const auto& q : quadrupel) {
        if (q.ist_vollstaendig()) {
            vollstaendig.push_back(q);
            chi_seq.push_back(q.chi());
        }
    }
    
    int N = vollstaendig.size();
    
    if (N == 0) {
        cout << "Keine vollständigen Quadrupel gefunden.\n";
        return;
    }
    
    // Berechne H = Σ χ
    int H = 0;
    for (int chi : chi_seq) H += chi;
    
    // Statistiken
    double mean = berechne_mittelwert(chi_seq);
    double var = berechne_varianz(chi_seq, mean);
    
    double h = (double)H / N;
    double Z = (double)H / sqrt((double)N);
    double Z_star = sqrt(3.0) * Z;
    
    cout << "Anzahl vollständiger Quadrupel: N = " << N << "\n";
    cout << "Bias-Funktion: H = " << H << "\n";
    cout << "Normalisierter Bias: h = H/N = " << fixed << setprecision(4) << h << "\n";
    cout << "\nStatistiken der χ-Sequenz:\n";
    cout << "  E[χ] = " << mean << " (Referenzmodell: 0)\n";
    cout << "  Var[χ] = " << setprecision(4) << var << " (Referenzmodell: 0.333)\n";
    
    cout << "\nNaive Bias-Scores (ohne Autokorrelationskorrektur):\n";
    cout << "  Z = H/√N = " << setprecision(3) << Z << "\n";
    cout << "  Z* = √3·H/√N = " << Z_star << "\n";
    
    if (!berechne_autokorr || N < 10) {
        return;
    }
    
    // Autokorrelationsanalyse
    cout << "\n" << string(60, '-') << "\n";
    cout << "AUTOKORRELATIONSANALYSE\n";
    cout << string(60, '-') << "\n\n";
    
    vector<double> rho;
    double sum_rho = 0;
    
    cout << "Autokorrelationsfunktion ρ(k) = Corr(χ_n, χ_{n+k}):\n\n";
    
    for (int k = 1; k <= min(10, N/2); k++) {
        double r = berechne_autokorrelation(chi_seq, k);
        rho.push_back(r);
        
        if (k <= 4) {
            sum_rho += r;
            cout << "  ρ(" << k << ") = " << setprecision(4) << setw(7) << r;
            if (abs(r) > 0.1) cout << "  ← signifikant!";
            cout << "\n";
        }
    }
    
    // Effektive Stichprobengröße
    double N_eff = N / (1.0 + 2.0 * sum_rho);
    
    // Effektiver Z-Score
    double Z_eff = H / sqrt(N_eff / 3.0);
    
    cout << "\n" << string(60, '-') << "\n";
    cout << "EFFEKTIVE SIGNIFIKANZ (nach Autokorrelationskorrektur)\n";
    cout << string(60, '-') << "\n\n";
    
    cout << "Summe Σ_{k=1}^{4} ρ(k) = " << setprecision(4) << sum_rho << "\n";
    cout << "Effektive Stichprobengröße: N_eff = N / (1 + 2·Σρ) = " 
         << setprecision(1) << fixed << N_eff << "\n";
    cout << "Reduktionsfaktor: N_eff / N = " << setprecision(3) 
         << (N_eff / N) << "\n\n";
    
    cout << "Effektiver Z-Score: Z_eff = H / √(N_eff/3) = " 
         << setprecision(3) << Z_eff << "\n\n";
    
    // Interpretation
    cout << string(60, '-') << "\n";
    cout << "INTERPRETATION\n";
    cout << string(60, '-') << "\n\n";
    
    if (abs(Z_eff) < 2.0) {
        cout << "✓ Nach Autokorrelationskorrektur: KEIN signifikanter Bias\n";
        cout << "  → Der naive Bias war ein Artefakt der Fensterüberlappung\n";
    } else if (abs(Z_eff) < 3.0) {
        cout << "~ Nach Autokorrelationskorrektur: Schwacher Bias (~2-sigma)\n";
        cout << "  → Suggestiv, aber nicht schlüssig\n";
    } else {
        cout << "✗ Nach Autokorrelationskorrektur: SIGNIFIKANTER Bias!\n";
        cout << "  → Dies deutet auf genuine Struktur in Primzahl-Restklassen hin\n";
    }
    
    cout << "\n";
}

// ========== Hauptprogramm ==========

int main(int argc, char* argv[]) {
    int n_primes = 10000;
    
    if (argc > 1) {
        n_primes = atoi(argv[1]);
        if (n_primes < 100) n_primes = 100;
        if (n_primes > 1000000) n_primes = 1000000;
    }
    
    cout << "\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  AUTOKORRELATIONSANALYSE DER EABC-CHIRALITÄT            ║\n";
    cout << "║  Der entscheidende Test                                 ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    cout << "Generiere " << n_primes << " Primzahlen...\n";
    vector<int> primzahlen = erzeuge_primzahlen(n_primes);
    cout << "Fertig. Bereich: 2 bis " << primzahlen.back() << "\n";
    
    // ========== Test 1: Überlappende Fenster (konsekutiv) ==========
    
    vector<Quadrupel> consec;
    for (size_t i = 0; i + 3 < primzahlen.size(); i++) {
        Quadrupel q;
        q.p = primzahlen[i];
        q.q = primzahlen[i+1];
        q.r = primzahlen[i+2];
        q.s = primzahlen[i+3];
        consec.push_back(q);
    }
    
    analysiere_konstruktion("KONSTRUKTION C_consec: Überlappende Fenster", consec, true);
    
    // ========== Test 2: Nichtüberlappende Fenster ==========
    
    vector<Quadrupel> nonoverlap;
    for (size_t i = 0; i + 3 < primzahlen.size(); i += 4) {
        Quadrupel q;
        q.p = primzahlen[i];
        q.q = primzahlen[i+1];
        q.r = primzahlen[i+2];
        q.s = primzahlen[i+3];
        nonoverlap.push_back(q);
    }
    
    analysiere_konstruktion("KONSTRUKTION C_nonoverlap: Nichtüberlappende Fenster", nonoverlap, true);
    
    // ========== Vergleichende Zusammenfassung ==========
    
    cout << "\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  VERGLEICHENDE ZUSAMMENFASSUNG                          ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n\n";
    
    cout << "Kritische Fragen:\n\n";
    cout << "1. Ist ρ_consec(1) > 0?\n";
    cout << "   → Ja: Autokorrelation durch Überlappung\n";
    cout << "   → Nein: Überraschend, würde Unabhängigkeit bedeuten\n\n";
    
    cout << "2. Ist ρ_nonoverlap(1) ≈ 0?\n";
    cout << "   → Ja: Bestätigt, dass Autokorr. von Überlappung kommt\n";
    cout << "   → Nein: Es gibt lokale Korrelation in Primzahlfolge\n\n";
    
    cout << "3. Bleibt Z_eff_consec signifikant?\n";
    cout << "   → Nein: Bias war reines Überlappungsartefakt\n";
    cout << "   → Ja: Genuine Struktur trotz Korrektur\n\n";
    
    cout << "4. Ist Z_eff_nonoverlap signifikant?\n";
    cout << "   → Nein: Bestätigt Konstruktionsabhängigkeit\n";
    cout << "   → Ja: Echter Effekt auch ohne Überlappung!\n\n";
    
    cout << "═══════════════════════════════════════════════════════════\n\n";
    
    cout << "Hinweis: Für robuste Ergebnisse empfohlen:\n";
    cout << "  ./autocorrelation_analysis 100000\n";
    cout << "  ./autocorrelation_analysis 1000000\n\n";
    
    return 0;
}
