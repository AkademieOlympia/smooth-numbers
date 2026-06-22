/**
 * Parallele Berechnung von glatten Zahlen
 * Verwendet OpenMP für Multi-Threading (wenn verfügbar)
 */

#include <iostream>
#include <vector>
#include <algorithm>

#ifdef _OPENMP
#include <omp.h>
#else
// Fallback-Definitionen wenn OpenMP nicht verfügbar
inline int omp_get_max_threads() { return 1; }
inline int omp_get_num_procs() { return 1; }
inline int omp_get_thread_num() { return 0; }
#endif

using namespace std;

// Hilfsfunktion: Prüft ob eine Zahl prim ist
bool istPrimzahlParallel(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// Generiert die ersten n Primzahlen (parallel)
vector<int> generiereErstePrimzahlenParallel(int anzahl) {
    vector<int> primzahlen;
    primzahlen.reserve(anzahl);
    
    // Für kleine Anzahlen ist sequentiell schneller
    if (anzahl < 100) {
        int kandidat = 2;
        while (primzahlen.size() < anzahl) {
            if (istPrimzahlParallel(kandidat)) {
                primzahlen.push_back(kandidat);
            }
            kandidat++;
        }
        return primzahlen;
    }
    
    // Parallele Variante für größere Anzahlen
    const int CHUNK_SIZE = 1000;
    int kandidat = 2;
    
    while (primzahlen.size() < anzahl) {
        vector<int> kandidaten;
        kandidaten.reserve(CHUNK_SIZE);
        
        for (int i = 0; i < CHUNK_SIZE; i++) {
            kandidaten.push_back(kandidat++);
        }
        
        vector<bool> ist_prim(CHUNK_SIZE);
        
        #ifdef _OPENMP
        #pragma omp parallel for
        #endif
        for (int i = 0; i < CHUNK_SIZE; i++) {
            ist_prim[i] = istPrimzahlParallel(kandidaten[i]);
        }
        
        for (int i = 0; i < CHUNK_SIZE; i++) {
            if (ist_prim[i]) {
                primzahlen.push_back(kandidaten[i]);
                if (primzahlen.size() >= anzahl) break;
            }
        }
    }
    
    primzahlen.resize(anzahl);
    return primzahlen;
}

// Berechnet glatte Zahlen (Standard-Algorithmus bleibt sequentiell,
// da er inherent sequentiell ist - aber wir können mehrere s-Werte parallel berechnen)
vector<long long> berechneGlatteZahlenParallel(int s, int n) {
    vector<int> primzahlen = generiereErstePrimzahlenParallel(s);
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

// Berechnet mehrere s-glatte Zahlen-Sequenzen parallel
vector<vector<long long>> berechneMultipleSParallel(const vector<int>& s_werte, int n) {
    int anzahl = s_werte.size();
    vector<vector<long long>> ergebnisse(anzahl);
    
    #ifdef _OPENMP
    #pragma omp parallel for schedule(dynamic)
    #endif
    for (int i = 0; i < anzahl; i++) {
        ergebnisse[i] = berechneGlatteZahlenParallel(s_werte[i], n);
    }
    
    return ergebnisse;
}

// Prüft ob eine Zahl s-glatt ist (parallel für große Batches)
bool istSGlattParallel(long long n, int groesste_primzahl) {
    if (n == 1) return true;
    
    for (int p = 2; p <= groesste_primzahl && p * p <= n; p++) {
        while (n % p == 0) {
            n /= p;
        }
    }
    
    return (n == 1 || n <= groesste_primzahl);
}

// Zählt glatte Zahlen in einem Bereich (parallelisiert)
int zaehleGlatteZahlenParallel(int von, int bis, int k) {
    if (k < 2) return (von <= 1 && bis >= 1) ? 1 : 0;
    
    int bereich = bis - von + 1;
    
    #ifdef _OPENMP
    vector<int> lokale_zaehler(omp_get_max_threads(), 0);
    
    #pragma omp parallel
    {
        int thread_id = omp_get_thread_num();
        
        #pragma omp for
        for (int i = von; i <= bis; i++) {
            if (istSGlattParallel(i, k)) {
                lokale_zaehler[thread_id]++;
            }
        }
    }
    
    int gesamt = 0;
    for (int z : lokale_zaehler) {
        gesamt += z;
    }
    return gesamt;
    #else
    // Sequentielle Variante ohne OpenMP
    int gesamt = 0;
    for (int i = von; i <= bis; i++) {
        if (istSGlattParallel(i, k)) {
            gesamt++;
        }
    }
    return gesamt;
    #endif
}

// Generiert Dreieck parallel
vector<vector<int>> generiereDreieckParallel(int max_n) {
    vector<vector<int>> dreieck(max_n);
    
    #ifdef _OPENMP
    #pragma omp parallel for schedule(dynamic)
    #endif
    for (int n = 1; n <= max_n; n++) {
        dreieck[n-1].resize(min(n, 20));
        for (int k = 1; k <= min(n, 20); k++) {
            dreieck[n-1][k-1] = zaehleGlatteZahlenParallel(1, n, k);
        }
    }
    
    return dreieck;
}

// Zeigt Informationen über Parallelisierung
void zeigeParallelInfo() {
    cout << "\n=== PARALLELISIERUNGS-INFO ===\n";
    cout << "Maximale Threads: " << omp_get_max_threads() << "\n";
    cout << "Anzahl Prozessoren: " << omp_get_num_procs() << "\n";
    
    #ifdef _OPENMP
    cout << "OpenMP aktiviert: Ja (Version " << _OPENMP << ")\n";
    #else
    cout << "OpenMP aktiviert: Nein\n";
    #endif
}
