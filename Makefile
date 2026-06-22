# Makefile für Smooth Numbers (Basis + Erweitert)

CXX = g++
CXXFLAGS = -std=c++11 -O2 -Wall -Wextra

# Für jetzt ohne OpenMP (kann später aktiviert werden wenn libomp installiert ist)
CXXFLAGS_EXTENDED = -std=c++11 -O2 -Wall -Wextra

# Targets
TARGET_BASIC = smooth_numbers
TARGET_EXTENDED = smooth_numbers_extended

SOURCE_BASIC = smooth_numbers.cpp
SOURCE_EXTENDED = smooth_numbers_extended.cpp

HEADERS = export.h parallel.h benchmark.h

.PHONY: all basic extended clean run run-extended benchmark help

# Standardziel: Beide Versionen
all: basic extended

# Basis-Version
basic: $(TARGET_BASIC)

$(TARGET_BASIC): $(SOURCE_BASIC)
	$(CXX) $(CXXFLAGS) -o $(TARGET_BASIC) $(SOURCE_BASIC)

# Erweiterte Version (ohne OpenMP auf diesem System)
extended: $(TARGET_EXTENDED)

$(TARGET_EXTENDED): $(SOURCE_EXTENDED) $(HEADERS)
	@echo "Hinweis: Kompiliere ohne OpenMP (install libomp für Parallelisierung)"
	$(CXX) $(CXXFLAGS_EXTENDED) -o $(TARGET_EXTENDED) $(SOURCE_EXTENDED)

# Ausführen
run: basic
	./$(TARGET_BASIC)

run-extended: extended
	./$(TARGET_EXTENDED)

# Demo ausführen
demo: extended
	@echo "6" | ./$(TARGET_EXTENDED)

# Test mit vordefinierter Eingabe
test: extended
	@echo "Führe automatische Demo aus..."
	@./$(TARGET_EXTENDED) < <(echo -e "6\n0")

# Aufräumen
clean:
	rm -f $(TARGET_BASIC) $(TARGET_EXTENDED)
	rm -f *.json *.csv *.html
	rm -f test_input.txt

# Nur kompilierte Programme entfernen
clean-bin:
	rm -f $(TARGET_BASIC) $(TARGET_EXTENDED)

# Nur Export-Dateien entfernen
clean-exports:
	rm -f *.json *.csv *.html

# Hilfe
help:
	@echo "Verfügbare Targets:"
	@echo "  make              - Kompiliert beide Versionen"
	@echo "  make basic        - Kompiliert nur die Basis-Version"
	@echo "  make extended     - Kompiliert die erweiterte Version"
	@echo "  make run          - Kompiliert und führt Basis-Version aus"
	@echo "  make run-extended - Kompiliert und führt erweiterte Version aus"
	@echo "  make demo         - Führt vollständige Demo aus"
	@echo "  make test         - Führt automatische Tests aus"
	@echo "  make clean        - Entfernt alle generierten Dateien"
	@echo "  make clean-bin    - Entfernt nur kompilierte Programme"
	@echo "  make clean-exports- Entfernt nur Export-Dateien"
	@echo "  make help         - Zeigt diese Hilfe an"
	@echo ""
	@echo "OpenMP-Hinweis:"
	@echo "  Für Parallelisierung installieren Sie libomp:"
	@echo "    brew install libomp"
