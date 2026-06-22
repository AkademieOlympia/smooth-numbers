# Makefile für Smooth Numbers (Basis + Erweitert + EABC)

CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra

# Für jetzt ohne OpenMP (kann später aktiviert werden wenn libomp installiert ist)
CXXFLAGS_EXTENDED = -std=c++17 -O2 -Wall -Wextra

# Targets
TARGET_BASIC = smooth_numbers
TARGET_EXTENDED = smooth_numbers_extended
TARGET_EABC = eabc_analysis

SOURCE_BASIC = smooth_numbers.cpp
SOURCE_EXTENDED = smooth_numbers_extended.cpp
SOURCE_EABC = eabc_analysis.cpp

HEADERS = export.h parallel.h benchmark.h eabc_model.h

.PHONY: all basic extended eabc clean run run-extended run-eabc demo help

# Standardziel: Alle Versionen
all: basic extended eabc

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

# Ausführen
run: basic
	./$(TARGET_BASIC)

run-extended: extended
	./$(TARGET_EXTENDED)

run-eabc: eabc
	./$(TARGET_EABC)

# Demo ausführen
demo: extended
	@echo "6" | ./$(TARGET_EXTENDED)

# EABC-Demo
demo-eabc: eabc
	@echo "7" | ./$(TARGET_EABC)

# Test mit vordefinierter Eingabe
test: extended
	@echo "Führe automatische Demo aus..."
	@./$(TARGET_EXTENDED) < <(echo -e "6\n0")

# Aufräumen
clean:
	rm -f $(TARGET_BASIC) $(TARGET_EXTENDED) $(TARGET_EABC)
	rm -f *.json *.csv *.html
	rm -f test_input.txt

# Nur kompilierte Programme entfernen
clean-bin:
	rm -f $(TARGET_BASIC) $(TARGET_EXTENDED) $(TARGET_EABC)

# Nur Export-Dateien entfernen
clean-exports:
	rm -f *.json *.csv *.html

# Hilfe
help:
	@echo "Verfügbare Targets:"
	@echo "  make              - Kompiliert alle Versionen"
	@echo "  make basic        - Kompiliert nur die Basis-Version"
	@echo "  make extended     - Kompiliert die erweiterte Version"
	@echo "  make eabc         - Kompiliert EABC/Bamberg-Modell"
	@echo "  make run          - Kompiliert und führt Basis-Version aus"
	@echo "  make run-extended - Kompiliert und führt erweiterte Version aus"
	@echo "  make run-eabc     - Kompiliert und führt EABC-Analyse aus"
	@echo "  make demo         - Führt vollständige Demo aus"
	@echo "  make demo-eabc    - Führt EABC/Bamberg-Demo aus"
	@echo "  make test         - Führt automatische Tests aus"
	@echo "  make clean        - Entfernt alle generierten Dateien"
	@echo "  make clean-bin    - Entfernt nur kompilierte Programme"
	@echo "  make clean-exports- Entfernt nur Export-Dateien"
	@echo "  make help         - Zeigt diese Hilfe an"
	@echo ""
	@echo "OpenMP-Hinweis:"
	@echo "  Für Parallelisierung installieren Sie libomp:"
	@echo "    brew install libomp"
