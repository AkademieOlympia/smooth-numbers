# Makefile für Smooth Numbers (Basis + Erweitert + EABC + Lean)

CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra

# Für jetzt ohne OpenMP (kann später aktiviert werden wenn libomp installiert ist)
CXXFLAGS_EXTENDED = -std=c++17 -O2 -Wall -Wextra

# Targets
TARGET_BASIC = smooth_numbers
TARGET_EXTENDED = smooth_numbers_extended
TARGET_EABC = eabc_analysis
TARGET_DICKMAN = dickman_bridge
TARGET_KLEIN = klein_bottle
TARGET_CHIRALITY = eabc_chirality
TARGET_ROBUSTNESS = chirality_robustness
TARGET_AUTOCORR = autocorrelation_analysis
TARGET_TRANSITION = transition_matrix
TARGET_GAP = gap_distribution
TARGET_RATIO = ratio_asymptotic

SOURCE_BASIC = smooth_numbers.cpp
SOURCE_EXTENDED = smooth_numbers_extended.cpp
SOURCE_EABC = eabc_analysis.cpp
SOURCE_DICKMAN = dickman_bridge.cpp
SOURCE_KLEIN = klein_bottle.cpp
SOURCE_CHIRALITY = eabc_chirality.cpp
SOURCE_ROBUSTNESS = chirality_robustness.cpp
SOURCE_AUTOCORR = autocorrelation_analysis.cpp
SOURCE_TRANSITION = transition_matrix.cpp
SOURCE_GAP = gap_distribution.cpp
SOURCE_RATIO = ratio_asymptotic.cpp

HEADERS = export.h parallel.h benchmark.h eabc_model.h

.PHONY: all basic extended eabc dickman klein chirality robustness autocorr transition gap ratio lean clean run run-extended run-eabc run-dickman run-klein run-chirality run-robustness run-autocorr run-transition run-gap run-ratio demo help

# Standardziel: Alle Versionen
all: basic extended eabc dickman klein chirality robustness autocorr transition gap ratio

# Basis-Version
basic: $(TARGET_BASIC)

$(TARGET_BASIC): $(SOURCE_BASIC)
	$(CXX) $(CXXFLAGS) -o $(TARGET_BASIC) $(SOURCE_BASIC)

# Erweiterte Version (ohne OpenMP auf diesem System)
extended: $(TARGET_EXTENDED)

$(TARGET_EXTENDED): $(SOURCE_EXTENDED) export.h parallel.h benchmark.h
	@echo "Hinweis: Kompiliere ohne OpenMP (install libomp für Parallelisierung)"
	$(CXX) $(CXXFLAGS_EXTENDED) -o $(TARGET_EXTENDED) $(SOURCE_EXTENDED)

# EABC/Bamberg-Modell Version
eabc: $(TARGET_EABC)

$(TARGET_EABC): $(SOURCE_EABC) eabc_model.h
	@echo "Kompiliere EABC/Bamberg-Modell Analyse..."
	$(CXX) $(CXXFLAGS) -o $(TARGET_EABC) $(SOURCE_EABC)

# Dickman-Funktion mit Lean-Verifikation
dickman: $(TARGET_DICKMAN)

$(TARGET_DICKMAN): $(SOURCE_DICKMAN)
	@echo "Kompiliere Dickman-de Bruijn Bridge (Lean-verifiziert)..."
	$(CXX) $(CXXFLAGS) -o $(TARGET_DICKMAN) $(SOURCE_DICKMAN)

# Klein-Flaschen-Topologie über EABC-Quadrupeln
klein: $(TARGET_KLEIN)

$(TARGET_KLEIN): $(SOURCE_KLEIN)
	@echo "Kompiliere Klein-Flaschen-Topologie..."
	$(CXX) $(CXXFLAGS) -o $(TARGET_KLEIN) $(SOURCE_KLEIN)

# EABC-Chiralitäts-Analyse (diskrete Topologie)
chirality: $(TARGET_CHIRALITY)

$(TARGET_CHIRALITY): $(SOURCE_CHIRALITY)
	@echo "Kompiliere EABC-Chiralitäts-Analyse (emergente Topologie)..."
	$(CXX) $(CXXFLAGS) -o $(TARGET_CHIRALITY) $(SOURCE_CHIRALITY)

# Chiralitäts-Robustheitstests
robustness: $(TARGET_ROBUSTNESS)

$(TARGET_ROBUSTNESS): $(SOURCE_ROBUSTNESS)
	@echo "Kompiliere Chiralitäts-Robustheitstests..."
	$(CXX) $(CXXFLAGS) -o $(TARGET_ROBUSTNESS) $(SOURCE_ROBUSTNESS)

# Autokorrelationsanalyse (DER ENTSCHEIDENDE TEST)
autocorr: $(TARGET_AUTOCORR)

$(TARGET_AUTOCORR): $(SOURCE_AUTOCORR)
	@echo "Kompiliere Autokorrelationsanalyse..."
	@echo "KRITISCHER TEST: Bleibt Bias nach Autokorrelationskorrektur?"
	$(CXX) $(CXXFLAGS) -o $(TARGET_AUTOCORR) $(SOURCE_AUTOCORR)

# Übergangsmatrix-Analyse (WICHTIGSTER THEORETISCHER SCHRITT)
transition: $(TARGET_TRANSITION)

$(TARGET_TRANSITION): $(SOURCE_TRANSITION)
	@echo "Kompiliere Übergangsmatrix-Analyse..."
	@echo "THEORETISCHER KERN: Erklärt P(a→b) den Chiralitätsbias?"
	$(CXX) $(CXXFLAGS) -o $(TARGET_TRANSITION) $(SOURCE_TRANSITION)

# Gap-Verteilungs-Analyse (DIE KAUSALE KETTE)
gap: $(TARGET_GAP)

$(TARGET_GAP): $(SOURCE_GAP)
	@echo "Kompiliere Gap-Verteilungs-Analyse..."
	@echo "DIE KAUSALE KETTE: Gap-Verteilung → Übergangsmatrix → EABC-Bias"
	$(CXX) $(CXXFLAGS) -o $(TARGET_GAP) $(SOURCE_GAP)

# Asymptotische R(X)-Analyse (DER KRITISCHSTE TEST)
ratio: $(TARGET_RATIO)

$(TARGET_RATIO): $(SOURCE_RATIO)
	@echo "Kompiliere R(X)-Asymptotik-Analyse..."
	@echo "DER KRITISCHSTE TEST: R(X) → 1, R(X) → c > 1, oder Oszillation?"
	$(CXX) $(CXXFLAGS) -o $(TARGET_RATIO) $(SOURCE_RATIO)

# Lean 4 Build
lean:
	@echo "Baue Lean 4 Formalisierung..."
	@if command -v lake >/dev/null 2>&1; then \
		lake build; \
	else \
		echo "Lean 4 nicht installiert. Siehe LEAN_INTEGRATION.md"; \
		echo "Installation: curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh"; \
	fi

# Lean Clean
lean-clean:
	@if command -v lake >/dev/null 2>&1; then \
		lake clean; \
	fi

# Ausführen
run: basic
	./$(TARGET_BASIC)

run-extended: extended
	./$(TARGET_EXTENDED)

run-eabc: eabc
	./$(TARGET_EABC)

run-dickman: dickman
	./$(TARGET_DICKMAN)

run-klein: klein
	./$(TARGET_KLEIN)

run-chirality: chirality
	./$(TARGET_CHIRALITY)

run-robustness: robustness
	./$(TARGET_ROBUSTNESS)

run-autocorr: autocorr
	./$(TARGET_AUTOCORR)

run-transition: transition
	./$(TARGET_TRANSITION)

run-gap: gap
	./$(TARGET_GAP)

run-ratio: ratio
	./$(TARGET_RATIO)

# Demo ausführen
demo: extended
	@echo "6" | ./$(TARGET_EXTENDED)

# EABC-Demo
demo-eabc: eabc
	@echo "7" | ./$(TARGET_EABC)

# Dickman-Demo
demo-dickman: dickman
	./$(TARGET_DICKMAN)

# Klein-Flaschen-Demo (geometrische Visualisierung)
demo-klein: klein
	./$(TARGET_KLEIN)

# Chiralitäts-Demo (emergente diskrete Topologie) - HISTORISCH
demo-chirality: chirality
	./$(TARGET_CHIRALITY)

# Robustheitstests (KRITISCHE ÜBERPRÜFUNG) - EMPFOHLEN ⭐
demo-robustness: robustness
	./$(TARGET_ROBUSTNESS)

# Autokorrelationsanalyse (DER ENTSCHEIDENDE TEST) - KRITISCH ⭐⭐⭐
demo-autocorr: autocorr
	@echo "═══════════════════════════════════════════════════════════"
	@echo "DER ENTSCHEIDENDE TEST"
	@echo "Bleibt nach Autokorrelationskorrektur ein Bias?"
	@echo "═══════════════════════════════════════════════════════════"
	./$(TARGET_AUTOCORR) 10000

# Übergangsmatrix-Analyse (WICHTIGSTER THEORETISCHER SCHRITT) - THEORIEKERN ⭐⭐⭐
demo-transition: transition
	@echo "═══════════════════════════════════════════════════════════"
	@echo "WICHTIGSTER THEORETISCHER SCHRITT"
	@echo "Erklärt die Markov-Struktur P(a→b) den Bias?"
	@echo "═══════════════════════════════════════════════════════════"
	./$(TARGET_TRANSITION) 100000

# Gap-Verteilungs-Analyse (DIE KAUSALE KETTE) - FINALE ERKLÄRUNG ⭐⭐⭐⭐
demo-gap: gap
	@echo "═══════════════════════════════════════════════════════════"
	@echo "DIE KAUSALE KETTE"
	@echo "Gap-Verteilung mod 12 → Übergangsmatrix → EABC-Bias"
	@echo "═══════════════════════════════════════════════════════════"
	./$(TARGET_GAP) 100000

# R(X)-Asymptotik-Analyse (DER KRITISCHSTE TEST) - ENTSCHEIDEND ⭐⭐⭐⭐⭐
demo-ratio: ratio
	@echo "═══════════════════════════════════════════════════════════"
	@echo "DER KRITISCHSTE TEST"
	@echo "R(X) = P(EABC) / P(ECBA)"
	@echo "Szenario 1: R(X) → 1 (Vorasymptotik)"
	@echo "Szenario 2: R(X) → c > 1 (stabile Asymmetrie)"
	@echo "Szenario 3: R(X) oszilliert (Prime Race)"
	@echo "═══════════════════════════════════════════════════════════"
	./$(TARGET_RATIO)

# Test mit vordefinierter Eingabe
test: extended
	@echo "Führe automatische Demo aus..."
	@./$(TARGET_EXTENDED) < <(echo -e "6\n0")

# Aufräumen
clean:
	rm -f $(TARGET_BASIC) $(TARGET_EXTENDED) $(TARGET_EABC) $(TARGET_DICKMAN) $(TARGET_KLEIN) $(TARGET_CHIRALITY) $(TARGET_ROBUSTNESS) $(TARGET_AUTOCORR) $(TARGET_TRANSITION) $(TARGET_GAP) $(TARGET_RATIO)
	rm -f *.json *.csv *.html
	rm -f test_input.txt

# Nur kompilierte Programme entfernen
clean-bin:
	rm -f $(TARGET_BASIC) $(TARGET_EXTENDED) $(TARGET_EABC) $(TARGET_DICKMAN) $(TARGET_KLEIN) $(TARGET_CHIRALITY) $(TARGET_ROBUSTNESS) $(TARGET_AUTOCORR) $(TARGET_TRANSITION) $(TARGET_GAP) $(TARGET_RATIO)

# Nur Export-Dateien entfernen
clean-exports:
	rm -f *.json *.csv *.html

# Vollständiges Clean (inkl. Lean)
clean-all: clean lean-clean

# Hilfe
help:
	@echo "Verfügbare Targets:"
	@echo "  make              - Kompiliert alle Versionen"
	@echo "  make basic        - Kompiliert nur die Basis-Version"
	@echo "  make extended     - Kompiliert die erweiterte Version"
	@echo "  make eabc         - Kompiliert EABC/Bamberg-Modell"
	@echo "  make dickman      - Kompiliert Dickman-Bridge (Lean-verifiziert)"
	@echo "  make klein        - Kompiliert Klein-Flaschen (geometrisch, historisch)"
	@echo "  make chirality    - Kompiliert Chiralitäts-Analyse (historisch)"
	@echo "  make robustness   - Kompiliert Robustheitstests ⭐"
	@echo "  make autocorr     - Kompiliert Autokorrelationsanalyse ⭐⭐⭐"
	@echo "  make transition   - Kompiliert Übergangsmatrix-Analyse ⭐⭐⭐ THEORIEKERN"
	@echo "  make gap          - Kompiliert Gap-Verteilungs-Analyse ⭐⭐⭐⭐ FINALE ERKLÄRUNG"
	@echo "  make ratio        - Kompiliert R(X)-Asymptotik-Analyse ⭐⭐⭐⭐⭐ KRITISCHSTER TEST"
	@echo "  make lean         - Baut Lean 4 Formalisierung"
	@echo "  make demo-ratio   - R(X)-Asymptotik (10K bis 1M) ⭐⭐⭐⭐⭐ KRITISCHSTER TEST"
	@echo "  make demo-gap     - Gap-Verteilung P(g mod 12|a) (100K Primzahlen) ⭐⭐⭐⭐"
	@echo "  make demo-transition - Übergangsmatrix P(a→b) (100K Primzahlen) ⭐⭐⭐"
	@echo "  make demo-autocorr- Autokorrelationsanalyse (10K Primzahlen) ⭐⭐⭐"
	@echo "  make demo-robustness - Robustheitstests ⭐"
	@echo "  make test         - Führt automatische Tests aus"
	@echo "  make clean        - Entfernt alle generierten Dateien"
	@echo "  make help         - Zeigt diese Hilfe an"
	@echo ""
	@echo "⭐⭐⭐⭐⭐ DER KRITISCHSTE TEST: make demo-ratio"
	@echo "  Misst R(X) = P(EABC) / P(ECBA) für X = 10⁴, 5×10⁴, 10⁵, 5×10⁵, 10⁶"
	@echo "  Entscheidet zwischen drei Szenarien:"
	@echo "    1. R(X) → 1 : Vorasymptotik-Effekt"
	@echo "    2. R(X) → c > 1 : Stabile Asymmetrie"
	@echo "    3. R(X) oszilliert : Prime-Race-Phänomen"
	@echo "  KRITISCH: Bestimmt die Interpretation des gesamten Projekts"
	@echo ""
	@echo "⭐⭐⭐⭐ FINALE ERKLÄRUNG: make demo-gap"
	@echo "  Berechnet Gap-Verteilung P(g mod 12 | p_n ≡ a)"
	@echo "  Zeigt kausale Kette: Gap-Verteilung → Übergangsmatrix → EABC-Bias"
	@echo "  Fundamentale Relation: b ≡ a + g (mod 12)"
	@echo "  EABC verwendet g ≡ {2,4}, ECBA verwendet g ≡ {8,10}"
	@echo "  FRAGE: Ist P(g≡2,4) > P(g≡8,10)?"
	@echo ""
	@echo "⭐⭐⭐ WICHTIGSTER THEORETISCHER SCHRITT: make demo-transition"
	@echo "  Berechnet Übergangsmatrix P(p_{n+1} ≡ b | p_n ≡ a)"
	@echo "  Testet Symmetrie: P(a→b) = P(b→a)?"
	@echo "  Analysiert zyklische Strukturen EABC vs ECBA"
	@echo "  FRAGE: Erklärt Markov-Dynamik den beobachteten Bias?"
	@echo ""
	@echo "⭐⭐⭐ DER ENTSCHEIDENDE TEST: make demo-autocorr"
	@echo "  Berechnet ρ(k) = Corr(χ_n, χ_{n+k})"
	@echo "  Vergleicht überlappende vs. nichtüberlappende Fenster"
	@echo "  Berechnet Z_eff nach Autokorrelationskorrektur"
	@echo "  FRAGE: Bleibt Bias nach Korrektur signifikant?"
	@echo ""
	@echo "⭐ ROBUSTHEITSTESTS: make demo-robustness"
	@echo "  Zeigt: Asymmetrie ist konstruktionsabhängig"
	@echo "  Zufällige Ordnung: P(EABC) ≈ P(ECBA)"
	@echo "  Konsekutive Ordnung: P(EABC) > P(ECBA)"
	@echo ""
	@echo "Für größere Datensätze:"
	@echo "  ./gap_distribution 1000000           # 1M Primzahlen ⭐⭐⭐⭐"
	@echo "  ./transition_matrix 1000000          # 1M Primzahlen"
	@echo "  ./autocorrelation_analysis 100000   # 100K Primzahlen"
	@echo ""
	@echo "Dokumentation:"
	@echo "  CHIRALITY_OBSERVABLES_v2.md  - Kern: Orientation Bias Observable ⭐⭐⭐"
	@echo "  ROBUSTNESS_TESTS.md          - Kritische Überprüfung ⭐"
	@echo "  EABC_MODEL.md                - EABC/Bamberg-Modell"
	@echo "  KLEIN_BOTTLE.md              - Historische Metapher"
	@echo ""
	@echo "OpenMP-Hinweis:"
	@echo "  Für Parallelisierung installieren Sie libomp:"
	@echo "    brew install libomp"
