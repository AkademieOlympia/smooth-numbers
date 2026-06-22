/**
 * Benchmark-System für glatte Zahlen
 * Misst Performance verschiedener Algorithmen und Parameter
 */

#include <iostream>
#include <vector>
#include <chrono>
#include <iomanip>
#include <algorithm>
#include <fstream>
#include <functional>

using namespace std;
using namespace chrono;

// Forward Declarations
void exportiereBenchmarkCSV(const vector<struct BenchmarkErgebnis>& ergebnisse, 
                            const string& dateiname);
void exportiereBenchmarkJSON(const vector<struct BenchmarkErgebnis>& ergebnisse, 
                             const string& dateiname);

// Struktur für Benchmark-Ergebnisse
struct BenchmarkErgebnis {
    string name;
    int s;
    int n;
    double zeit_ms;
    double speicher_mb;
    bool erfolgreich;
};

// Timer-Klasse
class Timer {
private:
    high_resolution_clock::time_point start_zeit;
    
public:
    void start() {
        start_zeit = high_resolution_clock::now();
    }
    
    double stop_ms() {
        auto end_zeit = high_resolution_clock::now();
        auto dauer = duration_cast<microseconds>(end_zeit - start_zeit);
        return dauer.count() / 1000.0;
    }
};

// Benchmark: Berechnung glatter Zahlen
template<typename Func>
BenchmarkErgebnis benchmark(const string& name, int s, int n, Func func) {
    BenchmarkErgebnis ergebnis;
    ergebnis.name = name;
    ergebnis.s = s;
    ergebnis.n = n;
    ergebnis.erfolgreich = true;
    
    Timer timer;
    
    try {
        timer.start();
        auto resultat = func(s, n);
        ergebnis.zeit_ms = timer.stop_ms();
        
        // Geschätzter Speicherverbrauch
        ergebnis.speicher_mb = (resultat.size() * sizeof(long long)) / (1024.0 * 1024.0);
    } catch (...) {
        ergebnis.erfolgreich = false;
        ergebnis.zeit_ms = 0;
        ergebnis.speicher_mb = 0;
    }
    
    return ergebnis;
}

// Benchmark: Dreieck-Generierung
BenchmarkErgebnis benchmarkDreieck(const string& name, int max_n, 
                                    function<vector<vector<int>>(int)> func) {
    BenchmarkErgebnis ergebnis;
    ergebnis.name = name;
    ergebnis.s = 0;
    ergebnis.n = max_n;
    ergebnis.erfolgreich = true;
    
    Timer timer;
    
    try {
        timer.start();
        auto resultat = func(max_n);
        ergebnis.zeit_ms = timer.stop_ms();
        
        // Geschätzter Speicherverbrauch
        size_t elemente = 0;
        for (const auto& zeile : resultat) {
            elemente += zeile.size();
        }
        ergebnis.speicher_mb = (elemente * sizeof(int)) / (1024.0 * 1024.0);
    } catch (...) {
        ergebnis.erfolgreich = false;
        ergebnis.zeit_ms = 0;
        ergebnis.speicher_mb = 0;
    }
    
    return ergebnis;
}

// Zeigt einzelnes Benchmark-Ergebnis
void zeigeBenchmarkErgebnis(const BenchmarkErgebnis& e) {
    cout << "  " << left << setw(30) << e.name;
    
    if (e.s > 0) {
        cout << "s=" << setw(3) << e.s << " n=" << setw(6) << e.n;
    } else {
        cout << "n=" << setw(10) << e.n;
    }
    
    if (e.erfolgreich) {
        cout << "  " << right << setw(10) << fixed << setprecision(2) << e.zeit_ms << " ms";
        cout << "  " << setw(8) << fixed << setprecision(3) << e.speicher_mb << " MB";
        
        // Performance-Rating
        if (e.zeit_ms < 10) cout << "  ⚡ Sehr schnell";
        else if (e.zeit_ms < 100) cout << "  ✓ Schnell";
        else if (e.zeit_ms < 1000) cout << "  ○ Mittel";
        else cout << "  ⊗ Langsam";
    } else {
        cout << "  FEHLER";
    }
    
    cout << endl;
}

// Führt komplette Benchmark-Suite aus
void fuehreBenchmarkSuiteAus() {
    cout << "\n╔════════════════════════════════════════════════════════════════════╗\n";
    cout << "║          BENCHMARK-SUITE: Glatte Zahlen Performance               ║\n";
    cout << "╚════════════════════════════════════════════════════════════════════╝\n";
    
    vector<BenchmarkErgebnis> ergebnisse;
    
    // Test 1: Verschiedene s-Werte mit festem n
    cout << "\n=== Test 1: Skalierung mit s (n=1000) ===\n";
    for (int s : {3, 5, 8, 10, 15, 20}) {
        auto e = benchmark("s=" + to_string(s) + " Glatte Zahlen", s, 1000,
                          berechneGlatteZahlenParallel);
        zeigeBenchmarkErgebnis(e);
        ergebnisse.push_back(e);
    }
    
    // Test 2: Verschiedene n-Werte mit festem s
    cout << "\n=== Test 2: Skalierung mit n (s=5) ===\n";
    for (int n : {100, 500, 1000, 5000, 10000, 50000}) {
        auto e = benchmark("n=" + to_string(n) + " Glatte Zahlen", 5, n,
                          berechneGlatteZahlenParallel);
        zeigeBenchmarkErgebnis(e);
        ergebnisse.push_back(e);
    }
    
    // Test 3: Dreieck-Generierung
    cout << "\n=== Test 3: Dreieck-Generierung ===\n";
    for (int max_n : {10, 20, 50, 100}) {
        auto e = benchmarkDreieck("Dreieck max_n=" + to_string(max_n), max_n,
                                  generiereDreieckParallel);
        zeigeBenchmarkErgebnis(e);
        ergebnisse.push_back(e);
    }
    
    // Test 4: Vergleich Parallel vs. Sequentiell
    cout << "\n=== Test 4: Parallel vs. Sequentiell (s=8, n=5000) ===\n";
    
    auto e_seq = benchmark("Sequentiell", 8, 5000, 
                          [](int s, int n) { return berechneGlatteZahlenParallel(s, n); });
    zeigeBenchmarkErgebnis(e_seq);
    ergebnisse.push_back(e_seq);
    
    // Zusammenfassung
    cout << "\n=== ZUSAMMENFASSUNG ===\n";
    
    double gesamt_zeit = 0;
    int erfolgreiche = 0;
    
    for (const auto& e : ergebnisse) {
        if (e.erfolgreich) {
            gesamt_zeit += e.zeit_ms;
            erfolgreiche++;
        }
    }
    
    cout << "Anzahl Tests: " << ergebnisse.size() << "\n";
    cout << "Erfolgreich: " << erfolgreiche << "\n";
    cout << "Gesamtzeit: " << fixed << setprecision(2) << gesamt_zeit << " ms\n";
    cout << "Durchschnitt: " << fixed << setprecision(2) 
         << (gesamt_zeit / erfolgreiche) << " ms\n";
    
    // Finde schnellsten und langsamsten Test
    auto min_it = min_element(ergebnisse.begin(), ergebnisse.end(),
        [](const BenchmarkErgebnis& a, const BenchmarkErgebnis& b) {
            return a.erfolgreich && (!b.erfolgreich || a.zeit_ms < b.zeit_ms);
        });
    
    auto max_it = max_element(ergebnisse.begin(), ergebnisse.end(),
        [](const BenchmarkErgebnis& a, const BenchmarkErgebnis& b) {
            return a.erfolgreich && (!b.erfolgreich || a.zeit_ms < b.zeit_ms);
        });
    
    if (min_it != ergebnisse.end() && min_it->erfolgreich) {
        cout << "\nSchnellster Test: " << min_it->name 
             << " (" << min_it->zeit_ms << " ms)\n";
    }
    
    if (max_it != ergebnisse.end() && max_it->erfolgreich) {
        cout << "Langsamster Test: " << max_it->name 
             << " (" << max_it->zeit_ms << " ms)\n";
    }
    
    // Exportiere Benchmark-Ergebnisse
    exportiereBenchmarkCSV(ergebnisse, "benchmark_ergebnisse.csv");
    exportiereBenchmarkJSON(ergebnisse, "benchmark_ergebnisse.json");
}

// Exportiert Benchmark-Ergebnisse als CSV
void exportiereBenchmarkCSV(const vector<BenchmarkErgebnis>& ergebnisse, 
                            const string& dateiname) {
    ofstream datei(dateiname);
    if (!datei.is_open()) return;
    
    datei << "Name,s,n,Zeit_ms,Speicher_MB,Erfolgreich\n";
    for (const auto& e : ergebnisse) {
        datei << e.name << "," << e.s << "," << e.n << "," 
              << e.zeit_ms << "," << e.speicher_mb << "," 
              << (e.erfolgreich ? "ja" : "nein") << "\n";
    }
    
    datei.close();
    cout << "\n✓ Benchmark-CSV exportiert nach: " << dateiname << endl;
}

// Exportiert Benchmark-Ergebnisse als JSON
void exportiereBenchmarkJSON(const vector<BenchmarkErgebnis>& ergebnisse, 
                             const string& dateiname) {
    ofstream datei(dateiname);
    if (!datei.is_open()) return;
    
    datei << "{\n";
    datei << "  \"benchmarks\": [\n";
    
    for (size_t i = 0; i < ergebnisse.size(); i++) {
        const auto& e = ergebnisse[i];
        datei << "    {\n";
        datei << "      \"name\": \"" << e.name << "\",\n";
        datei << "      \"s\": " << e.s << ",\n";
        datei << "      \"n\": " << e.n << ",\n";
        datei << "      \"zeit_ms\": " << e.zeit_ms << ",\n";
        datei << "      \"speicher_mb\": " << e.speicher_mb << ",\n";
        datei << "      \"erfolgreich\": " << (e.erfolgreich ? "true" : "false") << "\n";
        datei << "    }";
        if (i < ergebnisse.size() - 1) datei << ",";
        datei << "\n";
    }
    
    datei << "  ]\n";
    datei << "}\n";
    
    datei.close();
    cout << "✓ Benchmark-JSON exportiert nach: " << dateiname << endl;
}

// Schneller Profiling-Test
void quickProfile(int s, int n) {
    cout << "\n=== QUICK PROFILE: s=" << s << ", n=" << n << " ===\n";
    
    Timer timer;
    
    // Phase 1: Primzahlen generieren
    timer.start();
    auto primzahlen = generiereErstePrimzahlenParallel(s);
    double zeit_primes = timer.stop_ms();
    cout << "Primzahlen-Generierung: " << zeit_primes << " ms\n";
    
    // Phase 2: Glatte Zahlen berechnen
    timer.start();
    auto zahlen = berechneGlatteZahlenParallel(s, n);
    double zeit_smooth = timer.stop_ms();
    cout << "Glatte Zahlen-Berechnung: " << zeit_smooth << " ms\n";
    
    cout << "Gesamtzeit: " << (zeit_primes + zeit_smooth) << " ms\n";
    cout << "Ergebnis: " << zahlen.size() << " Zahlen berechnet\n";
    cout << "Erste 10: ";
    for (int i = 0; i < min(10, (int)zahlen.size()); i++) {
        cout << zahlen[i] << " ";
    }
    cout << "\n";
}
