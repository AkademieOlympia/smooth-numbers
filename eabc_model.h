/**
 * EABC/ABCE-Modell Integration für glatte Zahlen
 * 
 * Implementiert die Bamberg-Interpretation glatter Zahlen als:
 * - Schichtzahlen (Exponentensumme σ(n))
 * - Vektorzahlen (Signaturvektor v(n))
 * - 4D-Gitterpunkte im Quaternionen-inspirierten Raum
 */

#include <iostream>
#include <vector>
#include <map>
#include <cmath>
#include <iomanip>
#include <algorithm>

using namespace std;

// Struktur für Primfaktorzerlegung
struct Faktorisierung {
    map<int, int> faktoren;  // Primzahl -> Exponent
    
    int exponentensumme() const {
        int summe = 0;
        for (const auto& p : faktoren) {
            summe += p.second;
        }
        return summe;
    }
    
    void ausgabe() const {
        bool erste = true;
        for (const auto& [prim, exp] : faktoren) {
            if (!erste) cout << " × ";
            cout << prim;
            if (exp > 1) cout << "^" << exp;
            erste = false;
        }
    }
};

// EABC-Signatur: E=1, A=5, B=7, C=11 (mod 12)
struct EABCSignatur {
    int n_2;  // Sonderrolle
    int n_3;  // Sonderrolle
    int n_E;  // Primzahlen ≡ 1 (mod 12): keine außer 13, 37, 61...
    int n_A;  // Primzahlen ≡ 5 (mod 12): 5, 17, 29, 41...
    int n_B;  // Primzahlen ≡ 7 (mod 12): 7, 19, 31, 43...
    int n_C;  // Primzahlen ≡ 11 (mod 12): 11, 23, 47, 59...
    
    EABCSignatur() : n_2(0), n_3(0), n_E(0), n_A(0), n_B(0), n_C(0) {}
    
    int schichtzahl() const {
        return n_2 + n_3 + n_E + n_A + n_B + n_C;
    }
    
    // Nur EABC-Komponenten (ohne 2 und 3)
    int eabc_summe() const {
        return n_E + n_A + n_B + n_C;
    }
    
    void ausgabe() const {
        cout << "(2^" << n_2 << " 3^" << n_3 << " | ";
        cout << "E^" << n_E << " A^" << n_A << " B^" << n_B << " C^" << n_C << ")";
    }
    
    string zu_string() const {
        return "(" + to_string(n_E) + "," + to_string(n_A) + "," + 
               to_string(n_B) + "," + to_string(n_C) + ")";
    }
};

// Klassifiziert Primzahl nach EABC
char klassifiziere_primzahl(int p) {
    if (p == 2 || p == 3) return '0';  // Sonderrolle
    
    int rest = p % 12;
    switch (rest) {
        case 1: return 'E';
        case 5: return 'A';
        case 7: return 'B';
        case 11: return 'C';
        default: return '?';  // Sollte nicht vorkommen für echte Primzahlen
    }
}

// Berechnet Primfaktorzerlegung
Faktorisierung faktorisiere(long long n) {
    Faktorisierung f;
    
    // Teile durch 2
    while (n % 2 == 0) {
        f.faktoren[2]++;
        n /= 2;
    }
    
    // Teile durch ungerade Zahlen
    for (long long i = 3; i * i <= n; i += 2) {
        while (n % i == 0) {
            f.faktoren[i]++;
            n /= i;
        }
    }
    
    // Rest ist Primzahl
    if (n > 1) {
        f.faktoren[n]++;
    }
    
    return f;
}

// Konvertiert Faktorisierung zu EABC-Signatur
EABCSignatur zu_eabc_signatur(const Faktorisierung& f) {
    EABCSignatur sig;
    
    for (const auto& [prim, exp] : f.faktoren) {
        if (prim == 2) {
            sig.n_2 = exp;
        } else if (prim == 3) {
            sig.n_3 = exp;
        } else {
            char klasse = klassifiziere_primzahl(prim);
            switch (klasse) {
                case 'E': sig.n_E += exp; break;
                case 'A': sig.n_A += exp; break;
                case 'B': sig.n_B += exp; break;
                case 'C': sig.n_C += exp; break;
            }
        }
    }
    
    return sig;
}

// Analysiert eine einzelne Zahl
void analysiere_zahl(long long n) {
    cout << "\n=== ANALYSE VON " << n << " ===\n";
    
    auto f = faktorisiere(n);
    cout << "Faktorisierung: ";
    f.ausgabe();
    cout << "\n";
    
    auto sig = zu_eabc_signatur(f);
    cout << "EABC-Signatur: ";
    sig.ausgabe();
    cout << "\n";
    
    cout << "Schichtzahl σ(n): " << sig.schichtzahl() << "\n";
    cout << "Vektorzahl v(n): " << sig.zu_string() << "\n";
    cout << "EABC-Summe: " << sig.eabc_summe() << "\n";
    
    // Interpretation
    if (sig.schichtzahl() == 1) {
        cout << "→ PRIMZAHL (liegt auf einer Achse)\n";
    } else if (sig.eabc_summe() == 0) {
        cout << "→ 2-3-GLATT (nur Faktoren 2 und 3)\n";
    } else if (sig.n_2 == 0 && sig.n_3 == 0 && sig.eabc_summe() == 1) {
        cout << "→ EABC-PRIMZAHL (Achsenpunkt)\n";
    } else {
        cout << "→ GITTERPUNKT (Innenpunkt, Schicht " << sig.schichtzahl() << ")\n";
    }
}

// Generiert Schichten nach Exponentensumme
map<int, vector<long long>> generiere_schichten(const vector<long long>& zahlen) {
    map<int, vector<long long>> schichten;
    
    for (long long n : zahlen) {
        auto f = faktorisiere(n);
        int schicht = f.exponentensumme();
        schichten[schicht].push_back(n);
    }
    
    return schichten;
}

// Zeigt Schichten an
void zeige_schichten(const map<int, vector<long long>>& schichten, int max_schicht = 5) {
    cout << "\n=== SCHICHT-DARSTELLUNG ===\n";
    cout << "σ = Exponentensumme\n\n";
    
    for (int s = 0; s <= max_schicht && schichten.count(s); s++) {
        cout << "Schicht " << s << ": ";
        const auto& zahlen = schichten.at(s);
        
        for (size_t i = 0; i < min(zahlen.size(), size_t(20)); i++) {
            cout << zahlen[i];
            if (i < min(zahlen.size(), size_t(20)) - 1) cout << ", ";
        }
        
        if (zahlen.size() > 20) {
            cout << ", ... (" << zahlen.size() << " insgesamt)";
        }
        cout << "\n";
    }
}

// Analysiert EABC-Verteilung
void analysiere_eabc_verteilung(const vector<long long>& zahlen) {
    cout << "\n=== EABC-VERTEILUNG ===\n";
    
    int nur_23 = 0;
    int hat_E = 0, hat_A = 0, hat_B = 0, hat_C = 0;
    int primzahlen = 0;
    int gitterpunkte = 0;
    
    map<string, int> vektor_haeufigkeit;
    
    for (long long n : zahlen) {
        auto f = faktorisiere(n);
        auto sig = zu_eabc_signatur(f);
        
        if (sig.schichtzahl() == 1) {
            primzahlen++;
        } else if (sig.eabc_summe() == 0) {
            nur_23++;
        } else {
            gitterpunkte++;
        }
        
        if (sig.n_E > 0) hat_E++;
        if (sig.n_A > 0) hat_A++;
        if (sig.n_B > 0) hat_B++;
        if (sig.n_C > 0) hat_C++;
        
        vektor_haeufigkeit[sig.zu_string()]++;
    }
    
    cout << "Primzahlen (Achsenpunkte): " << primzahlen << "\n";
    cout << "Nur 2-3-glatt: " << nur_23 << "\n";
    cout << "Gitterpunkte (Innenpunkte): " << gitterpunkte << "\n\n";
    
    cout << "Enthält E-Komponente (≡1 mod 12): " << hat_E << "\n";
    cout << "Enthält A-Komponente (≡5 mod 12): " << hat_A << "\n";
    cout << "Enthält B-Komponente (≡7 mod 12): " << hat_B << "\n";
    cout << "Enthält C-Komponente (≡11 mod 12): " << hat_C << "\n\n";
    
    cout << "Häufigste EABC-Vektoren:\n";
    vector<pair<int, string>> sortiert;
    for (const auto& [vektor, anzahl] : vektor_haeufigkeit) {
        sortiert.push_back({anzahl, vektor});
    }
    sort(sortiert.rbegin(), sortiert.rend());
    
    for (size_t i = 0; i < min(sortiert.size(), size_t(10)); i++) {
        cout << "  v=" << sortiert[i].second << ": " << sortiert[i].first << "x\n";
    }
}

// Generiert "Periodensystem" - Zahlen nach (Schicht, Vektor)
void generiere_periodensystem(int max_n, int max_schicht = 4) {
    cout << "\n=== PERIODENSYSTEM DER ZAHLEN ===\n";
    cout << "Zahlen bis " << max_n << " nach (σ, v)\n\n";
    
    map<int, map<string, vector<long long>>> system;
    
    for (long long n = 1; n <= max_n; n++) {
        auto f = faktorisiere(n);
        auto sig = zu_eabc_signatur(f);
        int schicht = sig.schichtzahl();
        string vektor = sig.zu_string();
        
        if (schicht <= max_schicht) {
            system[schicht][vektor].push_back(n);
        }
    }
    
    for (int s = 0; s <= max_schicht; s++) {
        if (system.count(s) == 0) continue;
        
        cout << "═══ Schicht σ=" << s << " ═══\n";
        
        for (const auto& [vektor, zahlen] : system[s]) {
            cout << "  v=" << vektor << ": ";
            for (size_t i = 0; i < min(zahlen.size(), size_t(15)); i++) {
                cout << zahlen[i];
                if (i < min(zahlen.size(), size_t(15)) - 1) cout << ", ";
            }
            if (zahlen.size() > 15) cout << "...";
            cout << "\n";
        }
        cout << "\n";
    }
}

// Vergleich: Primzahlen vs. Glatte Zahlen
void vergleiche_prim_glatt(int max_n, int s_glatt = 3) {
    cout << "\n=== PRIMZAHLEN vs. GLATTE ZAHLEN ===\n";
    cout << "Bis n=" << max_n << "\n\n";
    
    vector<long long> primzahlen;
    vector<long long> glatte_zahlen;
    
    for (long long n = 2; n <= max_n; n++) {
        auto f = faktorisiere(n);
        auto sig = zu_eabc_signatur(f);
        
        // Primzahl?
        if (sig.schichtzahl() == 1) {
            primzahlen.push_back(n);
        }
        
        // s-glatt? (alle Faktoren ≤ p_s)
        bool ist_glatt = true;
        int groesster_faktor = 0;
        for (const auto& [p, _] : f.faktoren) {
            groesster_faktor = max(groesster_faktor, (int)p);
        }
        
        // Für s=3: bis Primzahl 5
        vector<int> grenzen = {0, 2, 3, 5, 7, 11, 13, 17, 19, 23};
        if (s_glatt < grenzen.size() && groesster_faktor <= grenzen[s_glatt]) {
            glatte_zahlen.push_back(n);
        }
    }
    
    cout << "Primzahlen: " << primzahlen.size() << " Zahlen\n";
    cout << "  → Achsenpunkte des Gitters\n";
    cout << "  → 'Harte' Faktorisierung\n";
    cout << "  → Erste 20: ";
    for (size_t i = 0; i < min(primzahlen.size(), size_t(20)); i++) {
        cout << primzahlen[i] << " ";
    }
    cout << "\n\n";
    
    cout << s_glatt << "-glatte Zahlen: " << glatte_zahlen.size() << " Zahlen\n";
    cout << "  → Gitterpunkte im Inneren\n";
    cout << "  → 'Weiche' Faktorisierung\n";
    cout << "  → Erste 20: ";
    for (size_t i = 0; i < min(glatte_zahlen.size(), size_t(20)); i++) {
        cout << glatte_zahlen[i] << " ";
    }
    cout << "\n\n";
    
    cout << "Verhältnis Glatt/Prim: " 
         << fixed << setprecision(2) 
         << (double)glatte_zahlen.size() / primzahlen.size() << "\n";
}
