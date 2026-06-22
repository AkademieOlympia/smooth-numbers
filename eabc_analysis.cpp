/**
 * EABC/ABCE Smooth Numbers - Bamberg-Modell Implementierung
 * 
 * Untersucht glatte Zahlen als:
 * - Schichtzahlen im 4D-Gitter
 * - Vektorzahlen mit Signatur (n_E, n_A, n_B, n_C)
 * - Gitterpunkte im Quaternionen-inspirierten Raum
 * - Verbindung zur Recamán-Folge
 */

#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include "eabc_model.h"

using namespace std;

// Generiert Recamán-Folge
pair<vector<long long>, set<long long>> generiere_recaman(int n) {
    vector<long long> folge = {0};
    set<long long> besucht = {0};
    
    long long aktuell = 0;
    
    for (int i = 1; i < n; i++) {
        long long rueckwaerts = aktuell - i;
        
        if (rueckwaerts > 0 && besucht.find(rueckwaerts) == besucht.end()) {
            aktuell = rueckwaerts;
        } else {
            aktuell = aktuell + i;
        }
        
        folge.push_back(aktuell);
        besucht.insert(aktuell);
    }
    
    return {folge, besucht};
}

// Analysiert nicht-besuchte Zahlen der Recamán-Folge
void analysiere_recaman_luecken(int max_recaman_schritte, int max_pruef_zahl) {
    cout << "\n╔══════════════════════════════════════════════════════════╗\n";
    cout << "║     RECAMÁN-FOLGE & GLATTE ZAHLEN (Bamberg-Analyse)    ║\n";
    cout << "╚══════════════════════════════════════════════════════════╝\n";
    
    cout << "\nGeneriere Recamán-Folge mit " << max_recaman_schritte << " Schritten...\n";
    auto [folge, besucht] = generiere_recaman(max_recaman_schritte);
    
    cout << "Besuchte Zahlen: " << besucht.size() << "\n";
    cout << "Maximale Zahl: " << *besucht.rbegin() << "\n\n";
    
    // Finde nicht-besuchte Zahlen
    vector<long long> nicht_besucht;
    for (long long n = 1; n <= max_pruef_zahl; n++) {
        if (besucht.find(n) == besucht.end()) {
            nicht_besucht.push_back(n);
        }
    }
    
    cout << "Nicht besuchte Zahlen bis " << max_pruef_zahl << ": " 
         << nicht_besucht.size() << "\n";
    
    // EABC-Analyse der nicht-besuchten Zahlen
    double durchschnitt_schicht = 0;
    
    if (nicht_besucht.size() > 0) {
        cout << "Erste 30: ";
        for (size_t i = 0; i < min(nicht_besucht.size(), size_t(30)); i++) {
            cout << nicht_besucht[i] << " ";
        }
        cout << "\n\n";
        
        // EABC-Analyse der nicht-besuchten Zahlen
        cout << "=== EABC-ANALYSE DER NICHT-BESUCHTEN ZAHLEN ===\n\n";
        
        int hochglatt_count = 0;
        map<int, int> schicht_verteilung;
        
        for (long long n : nicht_besucht) {
            auto f = faktorisiere(n);
            auto sig = zu_eabc_signatur(f);
            int schicht = sig.schichtzahl();
            
            durchschnitt_schicht += schicht;
            schicht_verteilung[schicht]++;
            
            // Hochglatt = Schicht >= 3 und kleine Faktoren
            if (schicht >= 3) {
                bool nur_kleine = true;
                for (const auto& [p, _] : f.faktoren) {
                    if (p > 5) nur_kleine = false;
                }
                if (nur_kleine) hochglatt_count++;
            }
        }
        
        if (nicht_besucht.size() > 0) {
            durchschnitt_schicht /= nicht_besucht.size();
        }
        
        cout << "Durchschnittliche Schichtzahl: " << fixed << setprecision(2) 
             << durchschnitt_schicht << "\n";
        cout << "Hochglatte Zahlen (σ≥3, nur 2,3,5): " << hochglatt_count 
             << " (" << (100.0 * hochglatt_count / nicht_besucht.size()) << "%)\n\n";
        
        cout << "Schicht-Verteilung:\n";
        for (const auto& [schicht, anzahl] : schicht_verteilung) {
            cout << "  σ=" << schicht << ": " << anzahl << " Zahlen\n";
        }
        
        // Detaillierte Analyse einiger Beispiele
        cout << "\n=== DETAILANALYSE ERSTER NICHT-BESUCHTER ZAHLEN ===\n";
        for (size_t i = 0; i < min(nicht_besucht.size(), size_t(10)); i++) {
            analysiere_zahl(nicht_besucht[i]);
        }
    }
    
    // Vergleich: Besuchte vs. Nicht-besuchte
    cout << "\n=== VERGLEICH: BESUCHT vs. NICHT-BESUCHT ===\n\n";
    
    vector<long long> besucht_vec(besucht.begin(), besucht.end());
    sort(besucht_vec.begin(), besucht_vec.end());
    
    // Nimm nur Zahlen bis max_pruef_zahl
    besucht_vec.erase(
        remove_if(besucht_vec.begin(), besucht_vec.end(), 
                  [max_pruef_zahl](long long n) { return n > max_pruef_zahl; }),
        besucht_vec.end()
    );
    
    double durchschnitt_besucht = 0;
    for (long long n : besucht_vec) {
        if (n > 0) {
            auto f = faktorisiere(n);
            durchschnitt_besucht += f.exponentensumme();
        }
    }
    durchschnitt_besucht /= besucht_vec.size();
    
    cout << "Durchschnittliche Schichtzahl (besucht): " 
         << fixed << setprecision(2) << durchschnitt_besucht << "\n";
    cout << "Durchschnittliche Schichtzahl (nicht besucht): " 
         << durchschnitt_schicht << "\n\n";
    
    if (durchschnitt_schicht > durchschnitt_besucht) {
        cout << "→ HYPOTHESE BESTÄTIGT: Nicht-besuchte Zahlen tendieren zu höheren Schichten!\n";
        cout << "  Die Recamán-Folge bevorzugt Randpunkte (Primzahlen, niedrige Schichten)\n";
        cout << "  und meidet hochglatte Innenpunkte des Gitters.\n";
    } else {
        cout << "→ HYPOTHESE NICHT BESTÄTIGT: Kein signifikanter Unterschied.\n";
    }
}

// Hauptmenü
void zeige_menu() {
    cout << "\n╔══════════════════════════════════════════════════════════╗\n";
    cout << "║         EABC/ABCE SMOOTH NUMBERS (Bamberg-Modell)      ║\n";
    cout << "╚══════════════════════════════════════════════════════════╝\n";
    cout << "\nWählen Sie eine Option:\n\n";
    cout << "  1. Einzelne Zahl analysieren\n";
    cout << "  2. Periodensystem generieren\n";
    cout << "  3. Schichten visualisieren\n";
    cout << "  4. EABC-Verteilung analysieren\n";
    cout << "  5. Primzahlen vs. Glatte Zahlen\n";
    cout << "  6. Recamán-Verbindung untersuchen\n";
    cout << "  7. Vollständige Demo\n";
    cout << "  0. Beenden\n";
    cout << "\nIhre Wahl: ";
}

int main() {
    int wahl;
    
    do {
        zeige_menu();
        cin >> wahl;
        
        switch (wahl) {
            case 1: {
                long long n;
                cout << "\nZahl eingeben: ";
                cin >> n;
                analysiere_zahl(n);
                break;
            }
            
            case 2: {
                int max_n;
                cout << "\nMaximale Zahl: ";
                cin >> max_n;
                generiere_periodensystem(max_n, 4);
                break;
            }
            
            case 3: {
                cout << "\n3-glatte Zahlen (Hamming-Zahlen):\n";
                vector<long long> hamming;
                for (long long n = 1; n <= 100; n++) {
                    auto f = faktorisiere(n);
                    bool ist_glatt = true;
                    for (const auto& [p, _] : f.faktoren) {
                        if (p > 5) ist_glatt = false;
                    }
                    if (ist_glatt) hamming.push_back(n);
                }
                auto schichten = generiere_schichten(hamming);
                zeige_schichten(schichten, 6);
                break;
            }
            
            case 4: {
                int max_n;
                cout << "\nBis welche Zahl analysieren? ";
                cin >> max_n;
                vector<long long> zahlen;
                for (long long n = 1; n <= max_n; n++) {
                    zahlen.push_back(n);
                }
                analysiere_eabc_verteilung(zahlen);
                break;
            }
            
            case 5: {
                int max_n;
                cout << "\nBis welche Zahl? ";
                cin >> max_n;
                vergleiche_prim_glatt(max_n, 3);
                break;
            }
            
            case 6: {
                int schritte, max_pruef;
                cout << "\nAnzahl Recamán-Schritte: ";
                cin >> schritte;
                cout << "Prüfe Zahlen bis: ";
                cin >> max_pruef;
                analysiere_recaman_luecken(schritte, max_pruef);
                break;
            }
            
            case 7: {
                cout << "\n╔══════════════════════════════════════════════════════════╗\n";
                cout << "║              VOLLSTÄNDIGE BAMBERG-DEMO                  ║\n";
                cout << "╚══════════════════════════════════════════════════════════╝\n";
                
                // Demo 1: Beispielzahlen
                cout << "\n*** DEMO 1: Beispiel-Analysen ***\n";
                vector<long long> beispiele = {30, 385, 3025, 2310, 72, 108, 144, 216};
                for (long long n : beispiele) {
                    analysiere_zahl(n);
                }
                
                // Demo 2: Periodensystem
                cout << "\n*** DEMO 2: Periodensystem ***\n";
                generiere_periodensystem(60, 3);
                
                // Demo 3: Primzahlen vs. Glatte
                cout << "\n*** DEMO 3: Geometrische Interpretation ***\n";
                vergleiche_prim_glatt(100, 3);
                
                // Demo 4: Recamán-Verbindung
                cout << "\n*** DEMO 4: Recamán-Hypothese ***\n";
                analysiere_recaman_luecken(500, 300);
                
                cout << "\n✨ Demo abgeschlossen!\n";
                break;
            }
            
            case 0:
                cout << "\nAuf Wiedersehen!\n";
                break;
                
            default:
                cout << "\nUngültige Wahl!\n";
        }
        
        if (wahl != 0) {
            cout << "\nDrücken Sie Enter um fortzufahren...";
            cin.ignore();
            cin.get();
        }
        
    } while (wahl != 0);
    
    return 0;
}
