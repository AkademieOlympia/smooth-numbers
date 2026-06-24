# Forschungsprioritäten: Smooth Numbers Projekt

**Stand:** 24. Juni 2026  
**Basis:** Wissenschaftliche Reife und Erkenntnisgewinn

---

## Das zentrale Motto (erweiterte Version)

$$\boxed{
\begin{align*}
&\text{Das Projekt untersucht zusätzliche Informationsstufen} \\[2mm]
&\text{und akzeptiert eine neue Stufe nur, wenn sie zusätzliche Varianz erklärt.}
\end{align*}
}$$

Dies verbindet die **philosophische Idee** unmittelbar mit dem **empirischen Prüfstandard** $\Delta R^2_X > \eta$.

**Siehe:** `catalan-normalform/RESEARCH_PHILOSOPHY.md` für die vollständige Entwicklung von Objekten über Strukturen zu Informationsstufen.

---

## Methodischer Durchbruch

Das Projekt hat sich von einer **Sammlung interessanter Ideen** zu einem **hierarchisch testbaren Forschungsprogramm** entwickelt.

**Kernprinzip:**

$$\boxed{\text{Erklärt } X \text{ zusätzliche Varianz gegenüber den bereits vorhandenen Ebenen?}}$$

---

## Reifegrad-Klassifikation

### Ebene A: Etabliert (Reife 8-9/10)

**Gap-Übergangsdynamik modulo 12:**
- Mechanismus: $a_n \to g_n \to a_{n+1}$
- Observable: $P(g \bmod 12 \mid a)$
- Empirisch: Robuste Asymmetrie beobachtet
- **Status:** Publikationsreif

**Modulo-30-Programm:**
- Test: Überlebt die Asymmetrie feinere Unterteilung?
- Entscheidet: Echter Effekt vs. Artefakt
- **Status:** Vorbereitet, höchste Priorität

---

### Ebene B: Plausible Struktur (Reife 5-7/10)

**EABC-Koordinatisierung:**

$$n \mapsto \bigl(\Omega(n), (v_2, v_3), v_{\text{fac}}, ||v_{\text{fac}}||^2\bigr)$$

- **Ω(n):** Komplexitätskoordinate (Anzahl Primfaktoren)
- **(v₂, v₃):** Faserkoordinate (2- und 3-adische Richtung)
- **v_fac = (e,a,b,c):** Richtungskoordinate (EABC-Verteilung für p > 3)
- **||v||² oder H:** Konzentrations/Intensitätskoordinate

**Status:** Definiert, testbar, noch nicht empirisch validiert

**M0-M4-Modellkaskade:**
- Systematische Varianzdekomposition
- Jede Ebene wird gegen vorherige getestet
- **Status:** Implementierung vorbereitet (E02)

---

### Ebene C: Offene Hypothesen (Reife 3-4/10)

**Catalan-Hierarchie:**
- Kanonisierung $\kappa: n \to T(n)$
- Catalan-Magic $M_C(n)$
- **Status:** Formalisiert (Lean), noch nicht empirisch getestet

**H0.5 (Schalenstabilität):**
- Zahlen gleicher Schale haben ähnliche Bäume
- **Status:** Hypothese definiert, Test steht aus

**H0.6 (Konzentrations-Dominanz):**
- $H(n) = ||v||^2/\Omega_{\text{EABC}}^2$ erklärt $M_C$
- **Status:** Hypothese definiert, Test steht aus

---

### Ebene D: Spekulation (Reife 1-2/10)

**Tamari-Geometrie:**
- Rotationen, spektrale Eigenschaften
- **Status:** Theoretische Vorbereitung

**Quaternionen/Oktonionen:**
- Hurwitz-Algebren als algebraischer Rahmen
- **Status:** Analogie, noch keine Mechanismus

**Hurwitz-Assoziatoren:**
- $[a,b,c]$ in $\mathbb{O}$
- **Status:** Spekulative Erweiterung

---

## Prioritätenliste

### **Priorität 1: Modulo-30-Test** (2-3 Wochen)

**Ziel:** Entscheidung über Gap-Asymmetrie

**Frage:**

$$P(g \bmod 30 \mid a) \stackrel{?}{\approx} P(g \bmod 12 \mid a \bmod 12)$$

**Falls ja:** Effekt ist strukturell, nicht EABC-Artefakt  
**Falls nein:** EABC war die eigentliche Quelle

**Deliverable:** Paper-ready Gap-Dynamik-Analyse

**Risiko:** Niedrig (beide Resultate sind publizierbar)

---

### **Priorität 2: E02 Modellkaskade M0-M4 mit M0b** (3-4 Wochen)

**Ziel:** Empirische Validierung der SVN-Koordinaten

**Kritische Tests:**

1. **M0b vs. M0:** $\Delta_{\Omega^2}$ — Sind nichtlineare $\Omega$-Effekte relevant?
2. **M3 vs. M2:** $\Delta_{\text{norm}}$ — Liefert die Norm Zusatzinformation?
3. **M3* vs. M2:** $\Delta_H$ — Ist dimensionslose Konzentration $H$ besser als rohe Norm?
4. **M4 vs. M3:** $\Delta_{\text{dir}}$ — Ist die Vektorrichtung wichtiger als Konzentration?

**Deliverable:** Varianzdekomposition $M_C = f(\Omega, \Omega^2, (v_2, v_3), H, \text{Residuen})$

**Risiko:** Mittel (benötigt Kanonisierung)

---

### **Priorität 3: Konzentrationsgröße H analysieren** (1-2 Wochen)

**Ziel:** Mathematische Interpretation der Norm

**Ansatz:**

$$H(n) = \frac{||v_{\text{fac}}||^2}{\Omega_{\text{EABC}}^2} = \sum_i p_i^2$$

wobei $p_i$ die normierten Anteile sind.

**Verbindungen:**
- Simpson-Index (Ökologie)
- Herfindahl-Hirschman-Index (Ökonomie)
- Rényi-Entropie Ordnung 2 (Informationstheorie)

**Deliverable:** Konzentrations-Dokument (✅ bereits erstellt)

**Risiko:** Niedrig (rein analytisch)

---

### **Priorität 4: Nur bei positiven Signalen**

**Falls $\Delta_{\text{norm}} > 0.10$ oder $\Delta_H > 0.10$:**

Dann erst:
- Catalan-Hierarchie ausbauen
- Tamari-Geometrie entwickeln
- Hurwitz-Erweiterung prüfen

**Begründung:**

Diese Ebenen können nur relevant werden, wenn M0-M4 überhaupt ein starkes Signal zeigen.

**Ohne robuste Norm-Kopplung** sind Catalan/Tamari/Hurwitz wissenschaftlich nicht gerechtfertigt.

---

## Wissenschaftliche Haltung

**Vor Priorität 1+2:**
> "Wir haben interessante Hypothesen über Primzahlen und Faktorisierungsstrukturen."

**Nach Priorität 1+2:**

**Szenario A (beide positiv):**
> "Wir haben einen empirisch validierten Mechanismus für Gap-Asymmetrie und eine belastbare Grobkörnungsstruktur für Faktorisierungen."

**Szenario B (Priorität 1 positiv, 2 negativ):**
> "Gap-Dynamik ist strukturell, aber Catalan-Magic ist trivial. Fokus auf Gaps."

**Szenario C (Priorität 1 negativ, 2 positiv):**
> "Gap-Asymmetrie ist EABC-Artefakt, aber SVN-Koordinaten funktionieren. Fokus auf Faktorisierungsgeometrie."

**Szenario D (beide negativ):**
> "Beide Haupthypothesen sind falsifiziert. Pivot zu anderen EABC-Aspekten (z.B. additive Strukturen, Fibonacci-Zeta)."

**Alle vier Szenarien sind wissenschaftlich wertvoll.**

---

## Zeitplan (nächste 8-10 Wochen)

| Woche | Aufgabe | Deliverable |
|-------|---------|-------------|
| 1-2 | **Modulo-30-Test** | Gap-Analyse mod 30 |
| 2 | **M0b-Erweiterung** | E02 mit nichtlinearer Kontrolle |
| 3-4 | **E02 Implementierung** | Erste M0-M4-Resultate |
| 4 | **Go/No-Go Entscheidung** | Fortsetzung oder Pivot |
| 5-6 | Falls Go: H0.5, H0.6 testen | Schalenstabilität, Konzentration |
| 7-8 | Falls starkes Signal: Catalan | E01 Tamari-Baseline |
| 9-10 | Integration | Preprint-Vorbereitung |

---

## Erfolgskriterien

### Minimalerfolg (Publikation möglich):

- Modulo-30-Analyse abgeschlossen (unabhängig vom Resultat)
- M0-M4-Kaskade durchgeführt
- Klare Aussage über $\Delta_{\text{norm}}$ und $\Delta_H$

### Starker Erfolg (hochrangige Publikation):

- Modulo-30: Asymmetrie überlebt
- E02: $\Delta_H > 0.10$
- Mechanistische Erklärung für Gap-Dynamik
- Belastbare Grobkörnungsstruktur

### Durchbruch (mehrere Papers):

- Beide Haupthypothesen bestätigt
- Catalan-Residuen sind eigenständig
- Hurwitz-Erweiterung zeigt Signale
- Vereinheitlichung von Gap-Dynamik und Faktorisierungsgeometrie

---

## Die wichtigste Erkenntnis

Das Projekt hat den Übergang geschafft:

$$\boxed{\text{Von Theorie über Objekte} \longrightarrow \text{zu Theorie über Informationsstufen}}$$

Die Architektur:

$$\Omega \to (v_2, v_3) \to v_{\text{fac}} \to ||v||^2 \to T(n)$$

ist ein **kumulatives Forschungsprogramm**, in dem jede neue Idee am selben Standard gemessen wird:

$$\text{Erklärt sie zusätzliche Varianz?}$$

**Das ist der methodische Kern.**

---

## Zusammenfassung

| Priorität | Aufgabe | Zeitaufwand | Risiko | Erkenntnis |
|-----------|---------|-------------|--------|------------|
| **1** | **Modulo-30-Test** | **2-3 Wochen** | **Niedrig** | **Hoch** |
| **2** | **E02 (M0-M4 + M0b)** | **3-4 Wochen** | **Mittel** | **Hoch** |
| **3** | **Konzentration H** | **1-2 Wochen** | **Niedrig** | **Mittel** |
| 4 | Catalan/Tamari/Hurwitz | 6-8 Wochen | Hoch | Abhängig von 1-3 |

**Die nächsten 6-8 Wochen entscheiden über die wissenschaftliche Tragfähigkeit des gesamten Projekts.**
