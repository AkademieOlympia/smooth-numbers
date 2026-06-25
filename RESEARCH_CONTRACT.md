# RESEARCH_CONTRACT

Stand: 2026-06-24

Verbindlicher Claim-Vertrag fuer dieses Repository.

## 1) Claim-Klassen (verpflichtend)

Jede zentrale Aussage muss explizit eine Klasse tragen:

- `LEAN_PROVED`
- `MATH_PROVED_NOT_FORMALIZED`
- `EMPIRICAL_ROBUST`
- `EMPIRICAL_PRELIMINARY`
- `HYPOTHESIS`
- `SPECULATIVE`

Ohne Klasse darf eine Aussage nicht als Ergebnis im Haupttext erscheinen.

## 2) Was darf wie behauptet werden

### A) Satz/Beweis-Claim

Ein "Satz ist bewiesen" ist nur erlaubt, wenn:

1. Die Aussage als Lean-Theorem vorliegt.
2. `lake build` erfolgreich durchlaeuft.
3. Die Referenzdatei und Theoremnamen angegeben sind.

Sonst ist die Formulierung auf "Statement/Stub/Hypothese" zu begrenzen.

### B) Mathematischer Hintergrund-Claim

Eine Aussage darf als mathematisch begruendet (`MATH_PROVED_NOT_FORMALIZED`) gefuehrt werden, wenn:

1. Es sich um bekannte Standardtheorie oder klar begruendete Mathematik handelt.
2. Sie nicht als Lean-formal bewiesen ausgegeben wird.
3. Dokumentiert ist, dass die Lean-Formalisierung noch aussteht.

### C) Empirischer Claim

Ein empirischer Claim muss enthalten:

1. Skriptpfad,
2. Output-Pfade,
3. Datensatz-/Skalenangaben,
4. klare Metrik und Entscheidungsregel.

Formulierungspflicht:

- `EMPIRICAL_ROBUST`: "robuster empirischer Befund im aktuellen Testdesign"
- `EMPIRICAL_PRELIMINARY`: "vorlaeufiger Befund, weitere Robustheitschecks offen"

### D) Hypothesen-Claim

Hypothesen muessen:

1. eine ID haben (z. B. `H18-B`),
2. falsifizierbar sein,
3. einen naechsten konkreten Test haben.

## 3) No-Overclaim-Policy

Nicht erlaubt:

- Empirie als Beweis zu formulieren.
- Statement/Stub/Axiom als "bewiesen" zu verkaufen.
- Spekulative Architekturideen als theoretische Resultate auszugeben.
- einzelne In-Sample-Treffer als robuste Entdeckung darzustellen.

Pflichtformulierungen bei Unsicherheit:

- "nicht gestuetzt"
- "offen"
- "vorlaeufig"
- "nur als Hypothese"

## 4) Lean-First-Prinzip

Wenn eine Aussage Kernarchitektur oder zentrale Mechanik betrifft:

1. zuerst Lean-Formalisierungsstatus pruefen,
2. dann Claim-Klasse setzen,
3. erst danach narrative Interpretation.

Prioritaetsregel:

- bei Konflikt zwischen Doku-Text und Lean-Code gilt Lean-Status,
- bis zur Klaerung wird defensiv auf niedrigere Evidenzklasse gesetzt.

## 5) Dokumentationspflicht pro Aenderung

Jede inhaltliche Aenderung mit Claim-Relevanz muss diese Dateien konsistent halten:

- `PROJECT_TRUTH_MAP.md`
- `LEAN_SECURED_CORE.md`
- `HYPOTHESES_REGISTER.md`

Wenn sich eine Einstufung aendert, muss der "naechste notwendige Schritt" aktualisiert werden.

## 6) Freigaberegel fuer Reviewer-feste Aussagen

Eine Aussage ist reviewer-fest nur dann:

1. Klasse ist gesetzt,
2. Evidenzquelle ist referenziert,
3. Gegenbezeichnung (z. B. Stub/Axiom) ist ausgeschlossen,
4. Sprache bleibt defensiv und scope-klar.

Kurzcheck vor Merge:

- "Ist das Lean-belegt, mathematisch belegt, empirisch robust, oder nur Hypothese?"
- "Ist diese Formulierung staerker als die Evidenz?"
- "Ist der naechste Test klar?"
