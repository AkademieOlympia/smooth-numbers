/**
 * Klein-Flasche Konstruktion über EABC-Primzahl-Quadrupeln
 * 
 * Konzept:
 * 1. Jede glatte Schale endet in EABC-Primzahlen
 * 2. Von einer Primzahl p aus: finde nächste 3 Primzahlen außerhalb der Schale
 * 3. Konstruiere Klein-Flasche über diesem Quadrupel
 * 4. Verbinde via E-Achse → ergibt "8" (∞-Struktur)
 * 5. Berechne Gesamtumlauf numerisch
 */

#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <tuple>

using namespace std;

namespace KleinBottle {

// Primzahl-Test
bool ist_primzahl(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// EABC-Klassifikation
enum class PrimKlasse { E, A, B, C, Sonder };

PrimKlasse klassifiziere(int p) {
    if (p == 2 || p == 3) return PrimKlasse::Sonder;
    int rest = p % 12;
    switch (rest) {
        case 1: return PrimKlasse::E;
        case 5: return PrimKlasse::A;
        case 7: return PrimKlasse::B;
        case 11: return PrimKlasse::C;
        default: return PrimKlasse::Sonder;
    }
}

string klasse_name(PrimKlasse k) {
    switch (k) {
        case PrimKlasse::E: return "E";
        case PrimKlasse::A: return "A";
        case PrimKlasse::B: return "B";
        case PrimKlasse::C: return "C";
        default: return "0";
    }
}

// Faktorisierung
map<int, int> faktorisiere(int n) {
    map<int, int> faktoren;
    while (n % 2 == 0) {
        faktoren[2]++;
        n /= 2;
    }
    for (int i = 3; i * i <= n; i += 2) {
        while (n % i == 0) {
            faktoren[i]++;
            n /= i;
        }
    }
    if (n > 1) faktoren[n]++;
    return faktoren;
}

// Prüft ob n in glatter Schale bis y liegt
bool in_glatter_schale(int n, int y) {
    auto faktoren = faktorisiere(n);
    for (const auto& [p, exp] : faktoren) {
        if (p > y) return false;
    }
    return true;
}

// Primzahl-Quadrupel: (p, q, r, s)
struct PrimQuadrupel {
    int p, q, r, s;
    PrimKlasse kp, kq, kr, ks;
    
    void ausgabe() const {
        cout << "(" << p << "[" << klasse_name(kp) << "], "
             << q << "[" << klasse_name(kq) << "], "
             << r << "[" << klasse_name(kr) << "], "
             << s << "[" << klasse_name(ks) << "])";
    }
    
    // Prüft ob alle vier Klassen unterschiedlich sind
    bool ist_vollstaendig() const {
        set<PrimKlasse> klassen = {kp, kq, kr, ks};
        return klassen.size() == 4 && 
               klassen.count(PrimKlasse::Sonder) == 0;
    }
};

/**
 * Findet nächste 3 Primzahlen nach p, die nicht in glatter Schale bis y liegen
 */
tuple<int, int, int> finde_naechste_drei(int p, int y) {
    vector<int> gefunden;
    int kandidat = p + 1;
    
    while (gefunden.size() < 3) {
        if (ist_primzahl(kandidat) && !in_glatter_schale(kandidat, y)) {
            gefunden.push_back(kandidat);
        }
        kandidat++;
    }
    
    return {gefunden[0], gefunden[1], gefunden[2]};
}

/**
 * Konstruiert Primzahl-Quadrupel für Klein-Flasche
 */
PrimQuadrupel konstruiere_quadrupel(int start_prim, int schalen_grenze) {
    PrimQuadrupel quad;
    quad.p = start_prim;
    quad.kp = klassifiziere(start_prim);
    
    auto [q, r, s] = finde_naechste_drei(start_prim, schalen_grenze);
    quad.q = q;
    quad.r = r;
    quad.s = s;
    quad.kq = klassifiziere(q);
    quad.kr = klassifiziere(r);
    quad.ks = klassifiziere(s);
    
    return quad;
}

/**
 * Klein-Flasche Struktur über Primzahl-Quadrupel
 * 
 * Topologie:
 * - Zwei Möbius-Bänder verbunden
 * - E-Achse als Verbindung
 * - Nicht-orientierbar
 * - Euler-Charakteristik χ = 0
 */
struct KleinFlasche {
    PrimQuadrupel quad;
    
    // Parametrisierung der Klein-Flasche
    // x(u,v), y(u,v), z(u,v), w(u,v) für 4D-Einbettung
    tuple<double, double, double, double> punkt(double u, double v) const {
        // u ∈ [0, 2π], v ∈ [0, 2π]
        
        // Klein-Flasche im R⁴ (figure-8 immersion)
        double R = 2.0;  // Großer Radius
        double r = 1.0;  // Kleiner Radius
        
        double x = (R + r * cos(v)) * cos(u);
        double y = (R + r * cos(v)) * sin(u);
        double z = r * sin(v) * cos(u/2);
        double w = r * sin(v) * sin(u/2);
        
        // Skaliere mit Primzahl-Werten
        double skala = (quad.p + quad.q + quad.r + quad.s) / 100.0;
        
        return {skala * x, skala * y, skala * z, skala * w};
    }
    
    // "8"-Form durch Projektion auf E-Achse
    tuple<double, double> projektion_8(double u) const {
        // Lemniskate (∞-Kurve)
        double a = sqrt(quad.p * quad.q);
        double x = a * cos(u) / (1 + sin(u) * sin(u));
        double y = a * sin(u) * cos(u) / (1 + sin(u) * sin(u));
        return {x, y};
    }
    
    // Gesamtumlauf: Integration über geschlossenen Weg
    double berechne_gesamtumlauf() const {
        const int N = 1000;
        double umlauf = 0.0;
        
        // Integriere entlang u-Richtung bei festem v=0
        for (int i = 0; i < N; i++) {
            double u1 = 2 * M_PI * i / N;
            double u2 = 2 * M_PI * (i + 1) / N;
            
            auto [x1, y1, z1, w1] = punkt(u1, 0);
            auto [x2, y2, z2, w2] = punkt(u2, 0);
            
            // Bogenlänge im R⁴
            double ds = sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) + 
                            (z2-z1)*(z2-z1) + (w2-w1)*(w2-w1));
            
            umlauf += ds;
        }
        
        return umlauf;
    }
    
    // Windungszahl der "8"
    int berechne_windungszahl() const {
        // Für Lemniskate: Windungszahl = 2
        // (Doppelschleife)
        return 2;
    }
    
    // Verknüpfungszahl mit E-Achse
    double e_achsen_verkettung() const {
        // Messe wie stark die Klein-Flasche um die E-Achse wickelt
        // E-Achse: p ≡ 1 (mod 12)
        
        int e_komponenten = 0;
        if (quad.kp == PrimKlasse::E) e_komponenten++;
        if (quad.kq == PrimKlasse::E) e_komponenten++;
        if (quad.kr == PrimKlasse::E) e_komponenten++;
        if (quad.ks == PrimKlasse::E) e_komponenten++;
        
        return e_komponenten / 4.0;
    }
    
    void ausgabe_topologie() const {
        cout << "\n=== KLEIN-FLASCHE ÜBER PRIMZAHL-QUADRUPEL ===\n";
        cout << "Quadrupel: ";
        quad.ausgabe();
        cout << "\n";
        
        cout << "Vollständig (E,A,B,C): " << (quad.ist_vollstaendig() ? "Ja" : "Nein") << "\n";
        cout << "Gesamtumlauf: " << fixed << setprecision(6) << berechne_gesamtumlauf() << "\n";
        cout << "Windungszahl: " << berechne_windungszahl() << "\n";
        cout << "E-Achsen-Verkettung: " << setprecision(3) << e_achsen_verkettung() << "\n";
        
        // Euler-Charakteristik der Klein-Flasche
        cout << "Euler-Charakteristik χ: 0 (nicht-orientierbar)\n";
        
        // Primzahl-Summe als topologische Invariante
        int summe = quad.p + quad.q + quad.r + quad.s;
        cout << "Primzahl-Summe Σp: " << summe << "\n";
        
        // "8"-Form Amplitude
        auto [x_max, y_max] = projektion_8(M_PI/4);
        cout << "8-Form Amplitude: (" << x_max << ", " << y_max << ")\n";
    }
};

/**
 * Sammlung von Klein-Flaschen über verschiedenen Quadrupeln
 */
class KleinFlaschenKomplex {
private:
    vector<KleinFlasche> flaschen;
    
public:
    void fuege_hinzu(const KleinFlasche& flasche) {
        flaschen.push_back(flasche);
    }
    
    // Finde alle vollständigen Quadrupel bis Grenze
    void konstruiere_alle(int max_start, int schalen_grenze) {
        cout << "\n=== KONSTRUIERE KLEIN-FLASCHEN-KOMPLEX ===\n";
        cout << "Start-Primzahlen bis: " << max_start << "\n";
        cout << "Schalen-Grenze: " << schalen_grenze << "\n\n";
        
        for (int p = 2; p <= max_start; p++) {
            if (!ist_primzahl(p)) continue;
            
            auto quad = konstruiere_quadrupel(p, schalen_grenze);
            KleinFlasche flasche;
            flasche.quad = quad;
            
            // Nur vollständige Quadrupel aufnehmen
            if (quad.ist_vollstaendig()) {
                fuege_hinzu(flasche);
                
                cout << "Flasche #" << flaschen.size() << ": ";
                quad.ausgabe();
                cout << " → Umlauf: " << fixed << setprecision(2) 
                     << flasche.berechne_gesamtumlauf() << "\n";
            }
        }
        
        cout << "\nGesamt: " << flaschen.size() << " vollständige Klein-Flaschen\n";
    }
    
    // Analysiere Umlauf-Verteilung
    void analysiere_umlaeufe() const {
        if (flaschen.empty()) {
            cout << "\nKeine Flaschen vorhanden!\n";
            return;
        }
        
        cout << "\n=== ANALYSE DER GESAMTUMLÄUFE ===\n";
        
        vector<double> umlaeufe;
        for (const auto& f : flaschen) {
            umlaeufe.push_back(f.berechne_gesamtumlauf());
        }
        
        sort(umlaeufe.begin(), umlaeufe.end());
        
        double min_u = umlaeufe.front();
        double max_u = umlaeufe.back();
        double mittel = 0;
        for (double u : umlaeufe) mittel += u;
        mittel /= umlaeufe.size();
        
        double median = umlaeufe[umlaeufe.size() / 2];
        
        cout << "Minimum: " << fixed << setprecision(4) << min_u << "\n";
        cout << "Maximum: " << max_u << "\n";
        cout << "Mittelwert: " << mittel << "\n";
        cout << "Median: " << median << "\n";
        
        // Histogram
        cout << "\nHistogramm (10 Bins):\n";
        const int bins = 10;
        vector<int> hist(bins, 0);
        for (double u : umlaeufe) {
            int bin = min(bins - 1, (int)((u - min_u) / (max_u - min_u + 0.001) * bins));
            hist[bin]++;
        }
        
        for (int i = 0; i < bins; i++) {
            double bin_start = min_u + i * (max_u - min_u) / bins;
            double bin_end = min_u + (i + 1) * (max_u - min_u) / bins;
            cout << "[" << setw(6) << bin_start << " - " << setw(6) << bin_end << "]: ";
            for (int j = 0; j < hist[i]; j++) cout << "█";
            cout << " (" << hist[i] << ")\n";
        }
    }
    
    // Finde spezielle Quadrupel mit bestimmten Eigenschaften
    void finde_spezielle() const {
        cout << "\n=== SPEZIELLE QUADRUPEL ===\n";
        
        // 1. Kleinstes vollständiges Quadrupel
        if (!flaschen.empty()) {
            auto min_it = min_element(flaschen.begin(), flaschen.end(),
                [](const KleinFlasche& a, const KleinFlasche& b) {
                    return a.quad.p < b.quad.p;
                });
            
            cout << "\n1. Kleinstes Quadrupel:\n   ";
            min_it->quad.ausgabe();
            cout << "\n   Umlauf: " << min_it->berechne_gesamtumlauf() << "\n";
        }
        
        // 2. Maximale E-Achsen-Verkettung
        auto max_e = max_element(flaschen.begin(), flaschen.end(),
            [](const KleinFlasche& a, const KleinFlasche& b) {
                return a.e_achsen_verkettung() < b.e_achsen_verkettung();
            });
        
        if (max_e != flaschen.end() && max_e->e_achsen_verkettung() > 0) {
            cout << "\n2. Maximale E-Achsen-Verkettung:\n   ";
            max_e->quad.ausgabe();
            cout << "\n   E-Verkettung: " << max_e->e_achsen_verkettung() << "\n";
        }
        
        // 3. Kleinster Umlauf
        auto min_umlauf = min_element(flaschen.begin(), flaschen.end(),
            [](const KleinFlasche& a, const KleinFlasche& b) {
                return a.berechne_gesamtumlauf() < b.berechne_gesamtumlauf();
            });
        
        if (min_umlauf != flaschen.end()) {
            cout << "\n3. Kleinster Gesamtumlauf:\n   ";
            min_umlauf->quad.ausgabe();
            cout << "\n   Umlauf: " << min_umlauf->berechne_gesamtumlauf() << "\n";
        }
    }
    
    void ausgabe_statistik() const {
        cout << "\n=== STATISTIK ===\n";
        cout << "Anzahl Klein-Flaschen: " << flaschen.size() << "\n";
        
        if (flaschen.empty()) return;
        
        // Zähle Klassen-Kombinationen
        map<tuple<PrimKlasse, PrimKlasse, PrimKlasse, PrimKlasse>, int> kombinationen;
        for (const auto& f : flaschen) {
            auto key = make_tuple(f.quad.kp, f.quad.kq, f.quad.kr, f.quad.ks);
            kombinationen[key]++;
        }
        
        cout << "\nKlassen-Kombinationen:\n";
        for (const auto& [kombi, anzahl] : kombinationen) {
            auto [k1, k2, k3, k4] = kombi;
            cout << "  (" << klasse_name(k1) << "," << klasse_name(k2) << "," 
                 << klasse_name(k3) << "," << klasse_name(k4) << "): " << anzahl << "\n";
        }
    }
};

} // namespace KleinBottle

int main() {
    using namespace KleinBottle;
    
    cout << "╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  KLEIN-FLASCHEN über EABC-Primzahl-Quadrupeln           ║\n";
    cout << "║  Topologische Erweiterung des Bamberg-Modells           ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n";
    
    // Beispiel 1: Einzelne Klein-Flasche
    cout << "\n*** BEISPIEL 1: Einzelne Klein-Flasche ***\n";
    
    int start = 5;  // Beginne mit p=5 (A-Klasse)
    int schale = 5; // Glatte Schale bis 5
    
    auto quad = konstruiere_quadrupel(start, schale);
    KleinFlasche flasche;
    flasche.quad = quad;
    flasche.ausgabe_topologie();
    
    // Beispiel 2: Komplex von Klein-Flaschen
    cout << "\n\n*** BEISPIEL 2: Klein-Flaschen-Komplex ***\n";
    
    KleinFlaschenKomplex komplex;
    komplex.konstruiere_alle(50, 7);  // Start-Primzahlen bis 50, Schale bis 7
    komplex.analysiere_umlaeufe();
    komplex.finde_spezielle();
    komplex.ausgabe_statistik();
    
    cout << "\n\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  Die '8'-Struktur verbindet Primzahl-Quadrupel via      ║\n";
    cout << "║  nicht-orientierbare Topologie (Klein-Flasche)          ║\n";
    cout << "║  Der Gesamtumlauf ist eine numerische Invariante        ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n";
    
    return 0;
}
