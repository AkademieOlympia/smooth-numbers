# Installation und Schnellstart

## Installation

### Voraussetzungen

- Python 3.9 oder höher
- pip (Python Package Installer)

### Schritt-für-Schritt

```bash
# 1. Repository klonen oder Verzeichnis öffnen
cd eabc-qubit

# 2. Virtuelle Umgebung erstellen (empfohlen)
python3 -m venv venv

# 3. Virtuelle Umgebung aktivieren
source venv/bin/activate       # Linux/macOS
# oder
venv\Scripts\activate          # Windows

# 4. Abhängigkeiten installieren
pip install --upgrade pip
pip install -r requirements.txt

# 5. Package im Development-Modus installieren
pip install -e .

# 6. Installation testen
python -c "import src; print('✓ Installation erfolgreich!')"
```

## Schnellstart

### 1. Demo-Skript ausführen

Das Demo-Skript führt eine vollständige Analyse mit einem kleinen System (N=500) durch:

```bash
python demo.py
```

**Ausgabe**:
- System-Parameter
- Spektrumsberechnung
- Level Spacing Distribution
- χ²-Fit gegen Poisson, GOE, GUE
- Interpretation der Ergebnisse
- Plots in `figures/`

**Dauer**: ~30 Sekunden

### 2. Interaktive Analyse (Jupyter Notebook)

```bash
# Jupyter starten
jupyter notebook

# Öffne: notebooks/01_basic_setup.ipynb
```

Das Notebook führt durch:
1. Hamiltonian-Konstruktion
2. Spektrumsberechnung
3. Spektrales Unfolding
4. Level Spacing Distribution
5. Visualisierung und Interpretation

### 3. Python-Skript

Minimales Beispiel:

```python
from src.hamiltonian import EABCHamiltonian
from src.spectral import spectral_unfolding
from src.level_spacing import compute_level_spacing, fit_level_statistics

# System konstruieren
N = 1000
H = EABCHamiltonian(N, alpha=1.0, beta=0.5, gamma=1.5)

# Spektrum berechnen
eigenvalues = H.compute_spectrum(k=500)

# Unfolding
unfolded = spectral_unfolding(eigenvalues)

# Level Spacings
spacings = compute_level_spacing(unfolded)

# Statistik
results = fit_level_statistics(spacings)
print(f"Beste Fit: {min(results, key=results.get)}")
```

## Tests ausführen

```bash
# Alle Tests
pytest tests/ -v

# Einzelner Test
pytest tests/test_hamiltonian.py -v

# Mit Coverage
pytest tests/ --cov=src --cov-report=html
```

## Häufige Probleme

### Problem: `ModuleNotFoundError: No module named 'sympy'`

**Lösung**: Abhängigkeiten wurden nicht installiert.

```bash
pip install -r requirements.txt
```

### Problem: `ImportError: No module named 'src'`

**Lösung**: Package nicht im Development-Modus installiert.

```bash
pip install -e .
```

### Problem: Jupyter Kernel findet Package nicht

**Lösung**: Kernel mit venv verknüpfen.

```bash
python -m ipykernel install --user --name=eabc-qubit
```

Dann in Jupyter: Kernel → Change Kernel → eabc-qubit

### Problem: `eigsh` konvergiert nicht

**Lösung**: System zu klein oder k zu groß.

- Erhöhe N (mindestens N > 100)
- Reduziere k (maximal k < 0.5 * dim(H))
- Setze `which='SM'` für mittlere Eigenwerte

### Problem: Plots werden nicht angezeigt

**Lösung**: Backend-Problem.

```python
import matplotlib
matplotlib.use('TkAgg')  # oder 'Qt5Agg'
import matplotlib.pyplot as plt
```

## Deinstallation

```bash
# Virtuelle Umgebung deaktivieren
deactivate

# Umgebung löschen
rm -rf venv

# Package deinstallieren (falls global installiert)
pip uninstall eabc-qubit
```

## Nächste Schritte

Nach erfolgreicher Installation:

1. **Demo ausführen**: `python demo.py`
2. **Notebook durcharbeiten**: `notebooks/01_basic_setup.ipynb`
3. **Parameter variieren**: Ändere α, β, γ in eigenen Skripten
4. **Große Systeme**: Teste mit N = 5000 oder N = 10000
5. **Dokumentation lesen**: `docs/theory.md`

## Support

Bei Problemen:

1. Prüfe `requirements.txt` - alle Pakete installiert?
2. Prüfe Python-Version: `python --version` (≥ 3.9?)
3. Lies die Fehlerausgabe sorgfältig
4. Teste mit kleinerem N (z.B. N=50)

---

**Viel Erfolg bei der Exploration der EABC-Qubit-Physik!**
