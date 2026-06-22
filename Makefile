# Makefile für Smooth Numbers

CXX = g++
CXXFLAGS = -std=c++11 -O2 -Wall -Wextra
TARGET = smooth_numbers
SOURCE = smooth_numbers.cpp

.PHONY: all clean run

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)

help:
	@echo "Verfügbare Targets:"
	@echo "  make          - Kompiliert das Programm"
	@echo "  make run      - Kompiliert und führt das Programm aus"
	@echo "  make clean    - Entfernt kompilierte Dateien"
	@echo "  make help     - Zeigt diese Hilfe an"
