/**
 * Erweiterte Version mit allen Features:
 * - Grafische Visualisierung (HTML/SVG)
 * - Export (CSV, JSON)
 * - Parallele Berechnung (OpenMP)
 * - Benchmark-Tests
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <set>
#include <string>

using namespace std;

// Include Headers
#include "parallel.h"
#include "export.h"
#include "benchmark.h"

// Basis-Funktionen (aus smooth_numbers.cpp)
bool istPrimzahl(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

vector<int> generiereErstePrimzahlen(int anzahl) {
    vector<int> primzahlen;
    int kandidat = 2;
    
    while (primzahlen.size() < anzahl) {
        if (istPrimzahl(kandidat)) {
            primzahlen.push_back(kandidat);
        }
        kandidat++;
    }
    
    return primzahlen;
}

bool istSGlatt(long long n, int groesste_primzahl) {
    if (n == 1) return true;
    
    for (int p = 2; p <= groesste_primzahl && p * p <= n; p++) {
        while (n % p == 0) {
            n /= p;
        }
    }
    
    return (n == 1 || n <= groesste_primzahl);
}

vector<long long> berechneGlatteZahlen(int s, int n) {
    vector<int> primzahlen = generiereErstePrimzahlen(s);
    vector<long long> glatte_zahlen(n);
    glatte_zahlen[0] = 1;
    
    vector<int> indizes(s, 0);
    vector<long long> naechste_kandidaten(s);
    
    for (int i = 0; i < s; i++) {
        naechste_kandidaten[i] = primzahlen[i];
    }
    
    for (int pos = 1; pos < n; pos++) {
        long long min_kandidat = *min_element(naechste_kandidaten.begin(), 
                                               naechste_kandidaten.end());
        glatte_zahlen[pos] = min_kandidat;
        
        for (int i = 0; i < s; i++) {
            if (naechste_kandidaten[i] == min_kandidat) {
                indizes[i]++;
                naechste_kandidaten[i] = glatte_zahlen[indizes[i]] * primzahlen[i];
            }
        }
    }
    
    return glatte_zahlen;
}

int zaehleGlatteZahlen(int n, int k) {
    if (k < 2) return (n >= 1) ? 1 : 0;
    
    int anzahl = 0;
    for (int i = 1; i <= n; i++) {
        if (istSGlatt(i, k)) {
            anzahl++;
        }
    }
    return anzahl;
}

vector<vector<int>> generiereGlattDreieck(int max_n, int max_k = 20) {
    vector<vector<int>> dreieck(max_n);
    
    for (int n = 1; n <= max_n; n++) {
        dreieck[n-1].resize(min(n, max_k));
        for (int k = 1; k <= min(n, max_k); k++) {
            dreieck[n-1][k-1] = zaehleGlatteZahlen(n, k);
        }
    }
    
    return dreieck;
}

void zeigeMenu() {
    cout << "\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  GLATTE ZAHLEN - Erweiterte Version mit allen Features   ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n";
    cout << "\nWählen Sie eine Option:\n\n";
    cout << "  1. Glatte Zahlen berechnen\n";
    cout << "  2. Dreieck-Darstellung generieren\n";
    cout << "  3. Export-Funktionen (CSV, JSON, HTML)\n";
    cout << "  4. Benchmark-Tests ausführen\n";
    cout << "  5. Parallele Berechnung demonstrieren\n";
    cout << "  6. Alle Demos ausführen\n";
    cout << "  0. Beenden\n";
    cout << "\nIhre Wahl: ";
}

void option1() {
    int s, n;
    cout << "\n=== GLATTE ZAHLEN BERECHNEN ===\n";
    cout << "Anzahl Primzahlen (s): ";
    cin >> s;
    cout << "Anzahl zu berechnender Zahlen (n): ";
    cin >> n;
    
    if (s < 1 || s > 20 || n < 1 || n > 100000) {
        cout << "Ungültige Eingabe! s: 1-20, n: 1-100000\n";
        return;
    }
    
    cout << "\nBerechne mit Parallelisierung...\n";
    auto zahlen = berechneGlatteZahlenParallel(s, n);
    
    cout << "\nErste 20 Zahlen:\n";
    for (int i = 0; i < min(20, (int)zahlen.size()); i++) {
        cout << "S(" << s << ", " << (i+1) << ") = " << zahlen[i];
        if ((i+1) % 5 == 0) cout << "\n";
        else cout << ", ";
    }
    
    if (zahlen.size() > 20) {
        cout << "\n...\nLetzte 5 Zahlen:\n";
        for (int i = max(0, (int)zahlen.size()-5); i < zahlen.size(); i++) {
            cout << "S(" << s << ", " << (i+1) << ") = " << zahlen[i] << "\n";
        }
    }
}

void option2() {
    int max_n;
    cout << "\n=== DREIECK-DARSTELLUNG ===\n";
    cout << "Maximale Zeilenzahl (max_n): ";
    cin >> max_n;
    
    if (max_n < 1 || max_n > 100) {
        cout << "Ungültige Eingabe! max_n: 1-100\n";
        return;
    }
    
    cout << "\nGeneriere Dreieck (parallel)...\n";
    auto dreieck = generiereDreieckParallel(max_n);
    
    cout << "\nDreieck T(n,k) = Anzahl k-glatter Zahlen <= n:\n\n";
    cout << "n\\k ";
    for (int k = 1; k <= min(15, max_n); k++) {
        cout << setw(4) << k;
    }
    cout << "\n" << string(4 + min(15, max_n) * 4, '-') << "\n";
    
    for (int n = 1; n <= max_n; n++) {
        cout << setw(3) << n << " ";
        for (int k = 0; k < min((int)dreieck[n-1].size(), 15); k++) {
            cout << setw(4) << dreieck[n-1][k];
        }
        cout << "\n";
    }
}

void option3() {
    cout << "\n=== EXPORT-FUNKTIONEN ===\n";
    cout << "1. Glatte Zahlen exportieren\n";
    cout << "2. Dreieck exportieren\n";
    cout << "Wahl: ";
    
    int wahl;
    cin >> wahl;
    
    if (wahl == 1) {
        int s, n;
        cout << "s: ";
        cin >> s;
        cout << "n: ";
        cin >> n;
        
        auto zahlen = berechneGlatteZahlenParallel(s, n);
        
        exportiereJSON(zahlen, s, "glatte_zahlen.json");
        exportiereCSV(zahlen, s, "glatte_zahlen.csv");
        
    } else if (wahl == 2) {
        int max_n;
        cout << "max_n: ";
        cin >> max_n;
        
        auto dreieck = generiereDreieckParallel(max_n);
        
        exportiereDreieckJSON(dreieck, "dreieck.json");
        exportiereDreieckCSV(dreieck, "dreieck.csv");
        exportiereHTML(dreieck, "dreieck_visualisierung.html");
        
        cout << "\n✨ Öffnen Sie 'dreieck_visualisierung.html' im Browser!\n";
    }
}

void option4() {
    cout << "\n=== BENCHMARK-TESTS ===\n";
    fuehreBenchmarkSuiteAus();
}

void option5() {
    cout << "\n=== PARALLELE BERECHNUNG ===\n";
    zeigeParallelInfo();
    
    cout << "\nBerechne mehrere s-Werte parallel...\n";
    vector<int> s_werte = {3, 5, 8, 10};
    
    auto ergebnisse = berechneMultipleSParallel(s_werte, 50);
    
    for (size_t i = 0; i < s_werte.size(); i++) {
        cout << "\ns=" << s_werte[i] << ": ";
        for (int j = 0; j < min(10, (int)ergebnisse[i].size()); j++) {
            cout << ergebnisse[i][j] << " ";
        }
        cout << "...";
    }
    cout << "\n";
}

void option6() {
    cout << "\n╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║              VOLLSTÄNDIGE DEMONSTRATION                   ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n";
    
    // Demo 1: Hamming-Zahlen
    cout << "\n*** DEMO 1: Hamming-Zahlen (s=3) ***\n";
    auto hamming = berechneGlatteZahlenParallel(3, 30);
    cout << "Erste 30 Hamming-Zahlen: ";
    for (int i = 0; i < 30; i++) {
        cout << hamming[i];
        if (i < 29) cout << ", ";
        if ((i+1) % 10 == 0) cout << "\n                         ";
    }
    cout << "\n";
    
    exportiereJSON(hamming, 3, "hamming_zahlen.json");
    exportiereCSV(hamming, 3, "hamming_zahlen.csv");
    
    // Demo 2: Dreieck
    cout << "\n*** DEMO 2: Dreieck-Darstellung (n=30) ***\n";
    auto dreieck = generiereDreieckParallel(30);
    exportiereDreieckJSON(dreieck, "dreieck_demo.json");
    exportiereDreieckCSV(dreieck, "dreieck_demo.csv");
    exportiereHTML(dreieck, "dreieck_demo.html");
    
    // Demo 3: Parallelisierung
    cout << "\n*** DEMO 3: Parallele Berechnung ***\n";
    zeigeParallelInfo();
    
    // Demo 4: Quick Profile
    cout << "\n*** DEMO 4: Performance-Profiling ***\n";
    quickProfile(8, 1000);
    
    // Demo 5: Benchmark
    cout << "\n*** DEMO 5: Mini-Benchmark ***\n";
    auto b1 = benchmark("s=5, n=1000", 5, 1000, berechneGlatteZahlenParallel);
    zeigeBenchmarkErgebnis(b1);
    
    auto b2 = benchmark("s=10, n=1000", 10, 1000, berechneGlatteZahlenParallel);
    zeigeBenchmarkErgebnis(b2);
    
    cout << "\n✨ Alle Demos abgeschlossen!\n";
    cout << "📁 Exportierte Dateien:\n";
    cout << "   - hamming_zahlen.json/csv\n";
    cout << "   - dreieck_demo.json/csv/html\n";
    cout << "\n💡 Öffnen Sie die HTML-Datei im Browser für die Visualisierung!\n";
}

int main() {
    int wahl;
    
    do {
        zeigeMenu();
        cin >> wahl;
        
        switch (wahl) {
            case 1: option1(); break;
            case 2: option2(); break;
            case 3: option3(); break;
            case 4: option4(); break;
            case 5: option5(); break;
            case 6: option6(); break;
            case 0: cout << "\nAuf Wiedersehen!\n"; break;
            default: cout << "\nUngültige Wahl!\n";
        }
        
        if (wahl != 0) {
            cout << "\nDrücken Sie Enter um fortzufahren...";
            cin.ignore();
            cin.get();
        }
        
    } while (wahl != 0);
    
    return 0;
}
