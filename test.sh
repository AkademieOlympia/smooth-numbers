#!/bin/bash
# Testskript für Smooth Numbers

echo "Test 1: Automatische Demonstration"
echo "===================================="
echo ""

# Erstelle eine Eingabedatei für den interaktiven Teil
echo "4" > test_input.txt
echo "15" >> test_input.txt

# Führe das Programm aus
./smooth_numbers < test_input.txt

# Aufräumen
rm -f test_input.txt

echo ""
echo "===================================="
echo "Test abgeschlossen!"
