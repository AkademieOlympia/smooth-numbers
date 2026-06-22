/**
 * Export-Funktionen für glatte Zahlen
 * Unterstützt CSV, JSON und HTML Formate
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <sstream>

using namespace std;

// JSON Export für glatte Zahlen
void exportiereJSON(const vector<long long>& zahlen, int s, const string& dateiname) {
    ofstream datei(dateiname);
    if (!datei.is_open()) {
        cerr << "Fehler: Konnte Datei " << dateiname << " nicht öffnen!" << endl;
        return;
    }
    
    datei << "{\n";
    datei << "  \"s\": " << s << ",\n";
    datei << "  \"anzahl\": " << zahlen.size() << ",\n";
    datei << "  \"zahlen\": [\n";
    
    for (size_t i = 0; i < zahlen.size(); i++) {
        datei << "    {\"index\": " << (i+1) << ", \"wert\": " << zahlen[i] << "}";
        if (i < zahlen.size() - 1) datei << ",";
        datei << "\n";
    }
    
    datei << "  ]\n";
    datei << "}\n";
    
    datei.close();
    cout << "✓ JSON exportiert nach: " << dateiname << endl;
}

// CSV Export für glatte Zahlen
void exportiereCSV(const vector<long long>& zahlen, int s, const string& dateiname) {
    ofstream datei(dateiname);
    if (!datei.is_open()) {
        cerr << "Fehler: Konnte Datei " << dateiname << " nicht öffnen!" << endl;
        return;
    }
    
    datei << "Index,S(" << s << ",n),Wert\n";
    for (size_t i = 0; i < zahlen.size(); i++) {
        datei << (i+1) << "," << s << "," << zahlen[i] << "\n";
    }
    
    datei.close();
    cout << "✓ CSV exportiert nach: " << dateiname << endl;
}

// CSV Export für Dreieck
void exportiereDreieckCSV(const vector<vector<int>>& dreieck, const string& dateiname) {
    ofstream datei(dateiname);
    if (!datei.is_open()) {
        cerr << "Fehler: Konnte Datei " << dateiname << " nicht öffnen!" << endl;
        return;
    }
    
    // Kopfzeile
    datei << "n,k,T(n,k)\n";
    
    // Daten
    for (size_t n = 0; n < dreieck.size(); n++) {
        for (size_t k = 0; k < dreieck[n].size(); k++) {
            datei << (n+1) << "," << (k+1) << "," << dreieck[n][k] << "\n";
        }
    }
    
    datei.close();
    cout << "✓ Dreieck-CSV exportiert nach: " << dateiname << endl;
}

// JSON Export für Dreieck
void exportiereDreieckJSON(const vector<vector<int>>& dreieck, const string& dateiname) {
    ofstream datei(dateiname);
    if (!datei.is_open()) {
        cerr << "Fehler: Konnte Datei " << dateiname << " nicht öffnen!" << endl;
        return;
    }
    
    datei << "{\n";
    datei << "  \"beschreibung\": \"T(n,k) = Anzahl der k-glatten Zahlen <= n\",\n";
    datei << "  \"zeilen\": " << dreieck.size() << ",\n";
    datei << "  \"dreieck\": [\n";
    
    for (size_t n = 0; n < dreieck.size(); n++) {
        datei << "    {\n";
        datei << "      \"n\": " << (n+1) << ",\n";
        datei << "      \"werte\": [";
        
        for (size_t k = 0; k < dreieck[n].size(); k++) {
            datei << dreieck[n][k];
            if (k < dreieck[n].size() - 1) datei << ", ";
        }
        
        datei << "]\n";
        datei << "    }";
        if (n < dreieck.size() - 1) datei << ",";
        datei << "\n";
    }
    
    datei << "  ]\n";
    datei << "}\n";
    
    datei.close();
    cout << "✓ Dreieck-JSON exportiert nach: " << dateiname << endl;
}

// HTML/SVG Visualisierung des Dreiecks
void exportiereHTML(const vector<vector<int>>& dreieck, const string& dateiname) {
    ofstream datei(dateiname);
    if (!datei.is_open()) {
        cerr << "Fehler: Konnte Datei " << dateiname << " nicht öffnen!" << endl;
        return;
    }
    
    datei << "<!DOCTYPE html>\n";
    datei << "<html lang=\"de\">\n";
    datei << "<head>\n";
    datei << "    <meta charset=\"UTF-8\">\n";
    datei << "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n";
    datei << "    <title>Glatt-Dreieck Visualisierung</title>\n";
    datei << "    <style>\n";
    datei << "        body {\n";
    datei << "            font-family: 'Courier New', monospace;\n";
    datei << "            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n";
    datei << "            padding: 20px;\n";
    datei << "            margin: 0;\n";
    datei << "        }\n";
    datei << "        .container {\n";
    datei << "            background: white;\n";
    datei << "            border-radius: 15px;\n";
    datei << "            padding: 30px;\n";
    datei << "            max-width: 1200px;\n";
    datei << "            margin: 0 auto;\n";
    datei << "            box-shadow: 0 10px 40px rgba(0,0,0,0.2);\n";
    datei << "        }\n";
    datei << "        h1 {\n";
    datei << "            text-align: center;\n";
    datei << "            color: #667eea;\n";
    datei << "            margin-bottom: 10px;\n";
    datei << "        }\n";
    datei << "        .subtitle {\n";
    datei << "            text-align: center;\n";
    datei << "            color: #666;\n";
    datei << "            margin-bottom: 30px;\n";
    datei << "            font-size: 14px;\n";
    datei << "        }\n";
    datei << "        table {\n";
    datei << "            border-collapse: collapse;\n";
    datei << "            margin: 20px auto;\n";
    datei << "        }\n";
    datei << "        th, td {\n";
    datei << "            border: 1px solid #ddd;\n";
    datei << "            padding: 8px 12px;\n";
    datei << "            text-align: center;\n";
    datei << "            min-width: 40px;\n";
    datei << "        }\n";
    datei << "        th {\n";
    datei << "            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n";
    datei << "            color: white;\n";
    datei << "            font-weight: bold;\n";
    datei << "        }\n";
    datei << "        td {\n";
    datei << "            background: white;\n";
    datei << "            transition: all 0.3s;\n";
    datei << "        }\n";
    datei << "        td:hover {\n";
    datei << "            background: #f0f0ff;\n";
    datei << "            transform: scale(1.1);\n";
    datei << "            box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);\n";
    datei << "            cursor: pointer;\n";
    datei << "        }\n";
    datei << "        .row-header {\n";
    datei << "            background: #f8f9fa !important;\n";
    datei << "            font-weight: bold;\n";
    datei << "            color: #667eea;\n";
    datei << "        }\n";
    datei << "        .heatmap-1 { background: #e8f5e9 !important; }\n";
    datei << "        .heatmap-2 { background: #c8e6c9 !important; }\n";
    datei << "        .heatmap-3 { background: #a5d6a7 !important; }\n";
    datei << "        .heatmap-4 { background: #81c784 !important; }\n";
    datei << "        .heatmap-5 { background: #66bb6a !important; color: white; }\n";
    datei << "        .info {\n";
    datei << "            background: #f8f9fa;\n";
    datei << "            padding: 15px;\n";
    datei << "            border-radius: 8px;\n";
    datei << "            margin-top: 20px;\n";
    datei << "            font-size: 13px;\n";
    datei << "        }\n";
    datei << "    </style>\n";
    datei << "</head>\n";
    datei << "<body>\n";
    datei << "    <div class=\"container\">\n";
    datei << "        <h1>🔢 Glatt-Dreieck (Smooth Numbers Triangle)</h1>\n";
    datei << "        <div class=\"subtitle\">T(n,k) = Anzahl der k-glatten Zahlen ≤ n</div>\n";
    datei << "        <table>\n";
    
    // Kopfzeile
    datei << "            <tr>\n";
    datei << "                <th>n\\k</th>\n";
    int max_k = 0;
    for (const auto& row : dreieck) {
        max_k = max(max_k, (int)row.size());
    }
    for (int k = 1; k <= max_k; k++) {
        datei << "                <th>" << k << "</th>\n";
    }
    datei << "            </tr>\n";
    
    // Datenzeilen mit Heatmap
    for (size_t n = 0; n < dreieck.size(); n++) {
        datei << "            <tr>\n";
        datei << "                <td class=\"row-header\">" << (n+1) << "</td>\n";
        
        for (size_t k = 0; k < dreieck[n].size(); k++) {
            int wert = dreieck[n][k];
            int prozent = (wert * 100) / (n + 1);
            string klasse = "";
            
            if (prozent >= 80) klasse = "heatmap-5";
            else if (prozent >= 60) klasse = "heatmap-4";
            else if (prozent >= 40) klasse = "heatmap-3";
            else if (prozent >= 20) klasse = "heatmap-2";
            else klasse = "heatmap-1";
            
            datei << "                <td class=\"" << klasse << "\" title=\"T(" 
                  << (n+1) << "," << (k+1) << ") = " << wert 
                  << " (" << prozent << "%)\">" << wert << "</td>\n";
        }
        datei << "            </tr>\n";
    }
    
    datei << "        </table>\n";
    datei << "        <div class=\"info\">\n";
    datei << "            <strong>Erklärung:</strong> T(n,k) zählt die Anzahl der Zahlen bis n, ";
    datei << "deren größter Primfaktor ≤ k ist.<br>\n";
    datei << "            <strong>Farbcodierung:</strong> Je dunkler die Farbe, desto höher der Anteil ";
    datei << "k-glatter Zahlen.<br>\n";
    datei << "            <strong>Interaktiv:</strong> Bewegen Sie die Maus über die Zellen für Details.\n";
    datei << "        </div>\n";
    datei << "    </div>\n";
    datei << "</body>\n";
    datei << "</html>\n";
    
    datei.close();
    cout << "✓ HTML Visualisierung exportiert nach: " << dateiname << endl;
}
