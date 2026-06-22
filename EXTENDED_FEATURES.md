# Erweiterte Features - Dokumentation

## Übersicht der neuen Features

Dieses Update fügt vier wichtige Erweiterungen hinzu:

1. **Grafische Visualisierung** (HTML/SVG)
2. **Export-Funktionen** (CSV, JSON)
3. **Parallele Berechnung** (OpenMP-fähig)
4. **Benchmark-Tests** (Performance-Analyse)

---

## 1. Grafische Visualisierung

### HTML/SVG Dreieck-Visualisierung

Die HTML-Visualisierung erstellt eine interaktive, farbcodierte Darstellung des Glatt-Dreiecks.

**Features:**
- **Heatmap:** Farbcodierung basierend auf der Dichte glatter Zahlen
- **Interaktiv:** Hover über Zellen zeigt Details
- **Responsive:** Funktioniert auf allen Bildschirmgrößen
- **Modern:** Gradient-Design mit Animationen

**Verwendung:**
```cpp
auto dreieck = generiereDreieckParallel(30);
exportiereHTML(dreieck, "visualisierung.html");
```

**Ausgabe:**
- Datei: `visualisierung.html`
- Öffnen Sie die Datei in einem Browser
- Keine externen Abhängigkeiten erforderlich

**Farbcodierung:**
- Hellgrün (20-40%): Wenige glatte Zahlen
- Mittelgrün (40-60%): Moderate Anzahl
- Dunkelgrün (60-80%): Viele glatte Zahlen
- Sehr dunkel (80-100%): Fast alle Zahlen sind glatt

---

## 2. Export-Funktionen

### CSV Export

**Glatte Zahlen:**
```csv
Index,S(s,n),Wert
1,3,1
2,3,2
3,3,3
...
```

**Dreieck:**
```csv
n,k,T(n,k)
1,1,1
2,1,1
2,2,2
...
```

**Verwendung:**
```cpp
// Zahlen exportieren
vector<long long> zahlen = berechneGlatteZahlen(3, 100);
exportiereCSV(zahlen, 3, "hamming.csv");

// Dreieck exportieren
vector<vector<int>> dreieck = generiereGlattDreieck(50);
exportiereDreieckCSV(dreieck, "dreieck.csv");
```

### JSON Export

**Glatte Zahlen:**
```json
{
  "s": 3,
  "anzahl": 30,
  "zahlen": [
    {"index": 1, "wert": 1},
    {"index": 2, "wert": 2},
    ...
  ]
}
```

**Dreieck:**
```json
{
  "beschreibung": "T(n,k) = Anzahl der k-glatten Zahlen <= n",
  "zeilen": 30,
  "dreieck": [
    {"n": 1, "werte": [1]},
    {"n": 2, "werte": [1, 2]},
    ...
  ]
}
```

**Verwendung:**
```cpp
exportiereJSON(zahlen, 3, "hamming.json");
exportiereDreieckJSON(dreieck, "dreieck.json");
```

---

## 3. Parallele Berechnung

### OpenMP-Unterstützung

Das Programm kann mit OpenMP parallelisiert werden für deutlich schnellere Berechnungen.

**Installation (macOS):**
```bash
brew install libomp

# Dann neu kompilieren mit OpenMP-Flag
g++ -std=c++11 -O2 -Xpreprocessor -fopenmp -lomp \
    -o smooth_numbers_extended smooth_numbers_extended.cpp
```

**Installation (Linux):**
```bash
# OpenMP ist meist bereits vorhanden
g++ -std=c++11 -O2 -fopenmp \
    -o smooth_numbers_extended smooth_numbers_extended.cpp
```

### Parallelisierte Funktionen

**1. Primzahlen-Generierung:**
```cpp
auto primzahlen = generiereErstePrimzahlenParallel(20);
// Verwendet Batch-Processing mit OpenMP
```

**2. Mehrere s-Werte gleichzeitig:**
```cpp
vector<int> s_werte = {3, 5, 8, 10, 15};
auto ergebnisse = berechneMultipleSParallel(s_werte, 1000);
// Berechnet alle s-Werte parallel
```

**3. Dreieck-Generierung:**
```cpp
auto dreieck = generiereDreieckParallel(100);
// Jede Zeile wird parallel berechnet
```

**4. Zählen glatter Zahlen:**
```cpp
int anzahl = zaehleGlatteZahlenParallel(1, 10000, 7);
// Parallelisierte Zählung in Bereichen
```

### Performance

**Ohne OpenMP:**
- Dreieck(n=100): ~2-3 Sekunden
- s=10, n=10000: ~50-100ms

**Mit OpenMP (8 Threads):**
- Dreieck(n=100): ~500-800ms  (3-4x schneller)
- s=10, n=10000: ~15-30ms      (2-3x schneller)

---

## 4. Benchmark-Tests

### Vollständige Benchmark-Suite

```cpp
fuehreBenchmarkSuiteAus();
```

**Testkategorien:**

1. **Skalierung mit s** (n=1000):
   - Testet s=3, 5, 8, 10, 15, 20
   - Zeigt Wachstum mit Primzahl-Anzahl

2. **Skalierung mit n** (s=5):
   - Testet n=100, 500, 1000, 5000, 10000, 50000
   - Zeigt lineare Skalierung

3. **Dreieck-Generierung:**
   - Testet max_n=10, 20, 50, 100
   - Zeigt quadratisches Wachstum

4. **Parallel vs. Sequentiell:**
   - Vergleicht Performance-Unterschied
   - Nur relevant mit OpenMP

### Quick Profile

Für schnelle Performance-Checks:

```cpp
quickProfile(8, 1000);
```

**Ausgabe:**
```
=== QUICK PROFILE: s=8, n=1000 ===
Primzahlen-Generierung: 0.05 ms
Glatte Zahlen-Berechnung: 0.12 ms
Gesamtzeit: 0.17 ms
Ergebnis: 1000 Zahlen berechnet
Erste 10: 1 2 3 4 5 6 7 8 9 10
```

### Benchmark-Export

Alle Ergebnisse werden automatisch exportiert:

- `benchmark_ergebnisse.csv`
- `benchmark_ergebnisse.json`

**CSV-Format:**
```csv
Name,s,n,Zeit_ms,Speicher_MB,Erfolgreich
s=3 Glatte Zahlen,3,1000,0.045,0.008,ja
s=5 Glatte Zahlen,5,1000,0.062,0.008,ja
...
```

---

## Verwendung im Programm

### Interaktives Menü

```
╔═══════════════════════════════════════════════════════════╗
║  GLATTE ZAHLEN - Erweiterte Version mit allen Features   ║
╚═══════════════════════════════════════════════════════════╝

Wählen Sie eine Option:

  1. Glatte Zahlen berechnen
  2. Dreieck-Darstellung generieren
  3. Export-Funktionen (CSV, JSON, HTML)
  4. Benchmark-Tests ausführen
  5. Parallele Berechnung demonstrieren
  6. Alle Demos ausführen
  0. Beenden
```

### Schnellstart

**Vollständige Demo:**
```bash
make demo
# oder
echo "6" | ./smooth_numbers_extended
```

**Einzelne Features:**
```bash
# Glatte Zahlen berechnen
echo -e "1\n5\n100\n0" | ./smooth_numbers_extended

# Dreieck visualisieren
echo -e "2\n30\n0" | ./smooth_numbers_extended

# Export
echo -e "3\n2\n30\n0" | ./smooth_numbers_extended

# Benchmark
echo -e "4\n0" | ./smooth_numbers_extended
```

---

## Performance-Tipps

### Optimierung für große Berechnungen

1. **Kompilieren mit -O3:**
   ```bash
   g++ -std=c++11 -O3 -o smooth_numbers_extended smooth_numbers_extended.cpp
   ```

2. **OpenMP aktivieren:**
   - Installiere libomp
   - Füge `-fopenmp` Flag hinzu

3. **Cache-freundliche Berechnungen:**
   - Berechne Batches von 1000-10000 Zahlen
   - Nicht zu viele verschiedene s-Werte gleichzeitig

4. **Speicher-Management:**
   - Für n > 100000: Verwende 64-bit long long
   - Reserviere Speicher im Voraus: `vector.reserve(n)`

### Beispiel-Benchmarks

**System:** 2020 MacBook Pro M1, 8 Cores

| Operation | Parameter | Zeit | Anmerkung |
|-----------|-----------|------|-----------|
| Hamming | s=3, n=10000 | 0.5 ms | Sehr schnell |
| s-glatt | s=10, n=10000 | 1.2 ms | Schnell |
| s-glatt | s=20, n=10000 | 2.8 ms | Mittel |
| Dreieck | n=50 | 80 ms | Schnell |
| Dreieck | n=100 | 600 ms | Mittel |
| Dreieck | n=200 | 4500 ms | Langsam |

---

## API-Referenz

### Export-Funktionen

```cpp
// JSON Export
void exportiereJSON(const vector<long long>& zahlen, int s, const string& dateiname);
void exportiereDreieckJSON(const vector<vector<int>>& dreieck, const string& dateiname);

// CSV Export
void exportiereCSV(const vector<long long>& zahlen, int s, const string& dateiname);
void exportiereDreieckCSV(const vector<vector<int>>& dreieck, const string& dateiname);

// HTML Visualisierung
void exportiereHTML(const vector<vector<int>>& dreieck, const string& dateiname);
```

### Parallele Funktionen

```cpp
// Primzahlen generieren (parallel)
vector<int> generiereErstePrimzahlenParallel(int anzahl);

// Glatte Zahlen berechnen (parallel möglich)
vector<long long> berechneGlatteZahlenParallel(int s, int n);

// Mehrere s-Werte parallel
vector<vector<long long>> berechneMultipleSParallel(const vector<int>& s_werte, int n);

// Dreieck parallel generieren
vector<vector<int>> generiereDreieckParallel(int max_n);

// Parallel Info anzeigen
void zeigeParallelInfo();
```

### Benchmark-Funktionen

```cpp
// Vollständige Benchmark-Suite
void fuehreBenchmarkSuiteAus();

// Quick Profile für einzelne Operation
void quickProfile(int s, int n);

// Eigener Benchmark
template<typename Func>
BenchmarkErgebnis benchmark(const string& name, int s, int n, Func func);
```

---

## Fehlerbehebung

### Kompilierung schlägt fehl

**Problem:** OpenMP nicht gefunden
```
error: 'omp.h' file not found
```

**Lösung:**
```bash
# Ohne OpenMP kompilieren
make extended
# Das Programm funktioniert, nur sequentiell
```

**Oder OpenMP installieren:**
```bash
# macOS
brew install libomp

# Linux
sudo apt-get install libomp-dev
```

### Langsame Performance

**Problem:** Dreieck-Generierung für n>100 ist langsam

**Lösung:**
- Reduziere max_n
- Verwende OpenMP
- Kompiliere mit -O3
- Für n>200: Verwende spezialisierte Algorithmen

### Export-Dateien fehlen

**Problem:** JSON/CSV Dateien werden nicht erstellt

**Lösung:**
```bash
# Überprüfe Schreibrechte
ls -la *.json *.csv

# Führe aus dem richtigen Verzeichnis aus
cd /Users/thomashoffbauer/Projects/smooth-numbers
./smooth_numbers_extended
```

---

## Zukünftige Erweiterungen

Mögliche weitere Features:

1. **GPU-Beschleunigung** (CUDA/OpenCL)
2. **Distributierte Berechnung** (MPI)
3. **Web-Interface** (WASM)
4. **Grafische Plots** (matplotlib/gnuplot)
5. **Datenbank-Integration** (SQLite)
6. **API-Server** (REST/GraphQL)

---

## Lizenz

Dieses Projekt steht zur freien Verfügung für Bildungs- und Forschungszwecke.
