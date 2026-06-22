/**
 * Smooth Numbers - Rekursive Berechnung und Dreieck-Darstellung
 * 
 * Eine s-glatte Zahl ist eine positive ganze Zahl, deren Primfaktoren
 * alle kleiner oder gleich der s-ten Primzahl sind.
 * 
 * Rekursive Formel: S(s, n) = min{S(s, i) × p_j | i < n, j ≤ s}
 * wobei p_j die j-te Primzahl ist.
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <set>

using namespace std;

// Hilfsfunktion: Prüft ob eine Zahl prim ist
bool istPrimzahl(int n) {
    if (n < 2) return false;
    if (n == 2) return true;
    if (n % 2 == 0) return false;
    
    for (int i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

// Generiert die ersten n Primzahlen
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

// Prüft ob eine Zahl s-glatt ist (alle Primfaktoren ≤ größte_primzahl)
bool istSGlatt(long long n, int groesste_primzahl) {
    if (n == 1) return true;
    
    for (int p = 2; p <= groesste_primzahl && p * p <= n; p++) {
        while (n % p == 0) {
            n /= p;
        }
    }
    
    // Falls n > 1 übrig bleibt, muss es ein Primfaktor > größte_primzahl sein
    return (n == 1 || n <= groesste_primzahl);
}

// Berechnet die ersten n s-glatten Zahlen mit dynamischer Programmierung
// Dies ist der Hamming-Algorithmus verallgemeinert auf s Primzahlen
vector<long long> berechneGlatteZahlen(int s, int n) {
    vector<int> primzahlen = generiereErstePrimzahlen(s);
    vector<long long> glatte_zahlen(n);
    glatte_zahlen[0] = 1;
    
    // Indizes für jede Primzahl
    vector<int> indizes(s, 0);
    
    // Nächste Kandidaten für jede Primzahl
    vector<long long> naechste_kandidaten(s);
    for (int i = 0; i < s; i++) {
        naechste_kandidaten[i] = primzahlen[i];
    }
    
    for (int pos = 1; pos < n; pos++) {
        // Finde das Minimum aller Kandidaten
        long long min_kandidat = *min_element(naechste_kandidaten.begin(), 
                                               naechste_kandidaten.end());
        glatte_zahlen[pos] = min_kandidat;
        
        // Aktualisiere alle Indizes, deren Kandidat gleich dem Minimum ist
        for (int i = 0; i < s; i++) {
            if (naechste_kandidaten[i] == min_kandidat) {
                indizes[i]++;
                naechste_kandidaten[i] = glatte_zahlen[indizes[i]] * primzahlen[i];
            }
        }
    }
    
    return glatte_zahlen;
}

// Zählt die Anzahl der k-glatten Zahlen ≤ n
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

// Generiert das Dreieck T(n, k) = Anzahl der k-glatten Zahlen ≤ n
void generiereGlattDreieck(int max_n) {
    cout << "\n=== GLATT-DREIECK (analog zu Pascal's Dreieck) ===\n";
    cout << "T(n,k) = Anzahl der k-glatten Zahlen <= n\n\n";
    
    // Kopfzeile
    cout << "n\\k ";
    for (int k = 1; k <= min(max_n, 15); k++) {
        cout << setw(4) << k;
    }
    cout << "\n";
    
    // Trennlinie
    cout << string(4 + min(max_n, 15) * 4, '-') << "\n";
    
    // Zeilen des Dreiecks
    for (int n = 1; n <= max_n; n++) {
        cout << setw(3) << n << " ";
        for (int k = 1; k <= min(n, 15); k++) {
            int anzahl = zaehleGlatteZahlen(n, k);
            cout << setw(4) << anzahl;
        }
        cout << "\n";
    }
}

// Zeigt die ersten n s-glatten Zahlen an
void zeigeGlatteZahlen(int s, int n) {
    vector<int> primzahlen = generiereErstePrimzahlen(s);
    
    cout << "\n=== S-GLATTE ZAHLEN (s = " << s << ") ===\n";
    cout << "Erlaubte Primzahlen: ";
    for (int i = 0; i < s; i++) {
        cout << primzahlen[i];
        if (i < s - 1) cout << ", ";
    }
    cout << "\n\n";
    
    vector<long long> glatte_zahlen = berechneGlatteZahlen(s, n);
    
    cout << "Die ersten " << n << " " << s << "-glatten Zahlen:\n";
    for (int i = 0; i < n; i++) {
        cout << "S(" << s << ", " << (i+1) << ") = " << glatte_zahlen[i];
        if ((i + 1) % 5 == 0) cout << "\n";
        else if (i < n - 1) cout << ", ";
    }
    cout << "\n";
}

// Rekursive Formel demonstrieren
void demonstriereRekursion(int s, int n) {
    vector<int> primzahlen = generiereErstePrimzahlen(s);
    
    cout << "\n=== REKURSIVE BERECHNUNG ===\n";
    cout << "Rekursionsformel für s = " << s << ":\n";
    cout << "S(s, 1) = 1\n";
    cout << "S(s, n) = min{S(s, i) × p_j | für alle i < n und j ≤ " << s << "}\n";
    cout << "wobei p_j ∈ {";
    for (int i = 0; i < s; i++) {
        cout << primzahlen[i];
        if (i < s - 1) cout << ", ";
    }
    cout << "}\n\n";
    
    vector<long long> glatte = berechneGlatteZahlen(s, min(n, 10));
    
    cout << "Beispielberechnung:\n";
    for (int i = 0; i < min(n, 10) && i < 6; i++) {
        cout << "S(" << s << ", " << (i+1) << ") = " << glatte[i];
        if (i > 0) {
            cout << "  (aus: ";
            bool erste = true;
            for (int j = 0; j < s && j < i; j++) {
                long long produkt = glatte[i-1] * primzahlen[j];
                if (!erste) cout << ", ";
                cout << glatte[i-1] << "×" << primzahlen[j] << "=" << produkt;
                erste = false;
            }
            cout << ")";
        }
        cout << "\n";
    }
}

int main() {
    cout << "╔═══════════════════════════════════════════════════════════╗\n";
    cout << "║  GLATTE ZAHLEN - Rekursive Formel & Dreieck-Darstellung  ║\n";
    cout << "╚═══════════════════════════════════════════════════════════╝\n";
    
    // Beispiel 1: Hamming-Zahlen (3-glatte Zahlen mit Primzahlen 2, 3, 5)
    cout << "\n*** BEISPIEL 1: Hamming-Zahlen (s=3) ***\n";
    zeigeGlatteZahlen(3, 20);
    demonstriereRekursion(3, 10);
    
    // Beispiel 2: 5-glatte Zahlen
    cout << "\n\n*** BEISPIEL 2: 5-glatte Zahlen (s=5) ***\n";
    zeigeGlatteZahlen(5, 30);
    
    // Beispiel 3: 8-glatte Zahlen (wie in der Anfrage erwähnt)
    cout << "\n\n*** BEISPIEL 3: 8-glatte Zahlen (s=8) ***\n";
    cout << "Primzahlen bis p_8 = 19: {2, 3, 5, 7, 11, 13, 17, 19}\n";
    zeigeGlatteZahlen(8, 25);
    
    // Dreieck-Darstellung
    cout << "\n\n*** DREIECK-DARSTELLUNG ***\n";
    generiereGlattDreieck(20);
    
    // Interaktiver Teil
    cout << "\n\n*** EIGENE BERECHNUNG ***\n";
    int s, n;
    cout << "Geben Sie s ein (Anzahl der Primzahlen): ";
    cin >> s;
    cout << "Geben Sie n ein (Anzahl der zu berechnenden Zahlen): ";
    cin >> n;
    
    if (s > 0 && s <= 20 && n > 0 && n <= 1000) {
        zeigeGlatteZahlen(s, n);
        demonstriereRekursion(s, n);
    } else {
        cout << "Ungültige Eingabe! s sollte 1-20 und n sollte 1-1000 sein.\n";
    }
    
    return 0;
}
