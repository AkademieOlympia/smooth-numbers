# scherzing - 7-Tage-Toolchain fuer einen deutschsprachigen Kurzroman

Dieses Projekt liefert eine sofort nutzbare, lokale Schreib-Toolchain fuer einen wissenschaftlich-dichten Techno-Thriller in deutscher Sprache.  
Ziel: In 7 Tagen vom Expose zum finalen Manuskript.

## Quickstart (heute starten)

1. In das Projekt wechseln:
   - `cd scherzing`
2. Tagesziel ansehen:
   - `make day1`
3. Expose und Figuren ausfuellen:
   - `roman/00_expose.md`
   - `roman/01_figuren.md`
4. Erstes Kapitel anlegen:
   - `roman/kapitel/kapitel_01.md`
5. Fortschritt pruefen:
   - `make status`
   - `make words`
6. Gesamtmanuskript bauen:
   - `make build`

## Projektstruktur

- `plan/7-tage-plan.md` - Tag-fuer-Tag-Meilensteine
- `roman/` - Expose, Figuren, Kapitelplan, Kapiteldateien
- `prompts/` - Prompt-Vorlagen fuer KI-gestuetzte Schreibarbeit
- `tools/` - Lokale Python-Skripte (ohne Zusatzpakete)
- `manuskript_final.md` - Build-Ausgabe aus allen Kapiteln

## Täglicher Workflow (ca. 90-150 Minuten)

1. **Ziel setzen (10 Min):**
   - `make dayX` fuer den aktuellen Tag
   - Tagesziel als 3 konkrete Aufgaben notieren
2. **Schreiben (45-90 Min):**
   - Kapiteldatei bearbeiten
   - Bei Bedarf Prompt aus `prompts/` verwenden
3. **Qualitaetssicherung (20-30 Min):**
   - `prompts/spannungspruefung.md`
   - `prompts/stilkonsistenz.md`
   - `prompts/plausibilitaetscheck.md`
4. **Abschluss (5-10 Min):**
   - `make words`
   - `make status`
   - Notiz: Was ist morgen der erste Satz/Abschnitt?

## Befehle

- `make status` - Soll/Ist-Fortschritt fuer den aktuellen Tag
- `make words` - Wortzahl je Kapitel + gesamt
- `make build` - Kapitel zu `manuskript_final.md` zusammenfuehren
- `make day1` ... `make day7` - Tagesziele anzeigen

## Zielkriterien fuer Tag 7

- Vollstaendiger Handlungsbogen mit klarem Anfang, Konflikt, Aufloesung
- Alle 7 Kapitel in `roman/kapitel/` vorhanden und ueberarbeitet
- Durchgehende Stilfuehrung: praezise, technisch plausibel, spannungsorientiert
- Finales Manuskript erfolgreich gebaut (`make build`)
- Zielwortzahl erreicht (Richtwert 16.000-28.000 Woerter)

## Stilrichtlinien (allgemein, keine Autorenimitation)

- Wissenschaftlich dicht: konkrete Verfahren, Systeme, Limits, Konsequenzen
- Techno-Thriller-Rhythmus: kurze Entscheidungszyklen unter Zeitdruck
- Klare Kausalitaet: jede technische Entscheidung veraendert die Lage
- Fachbegriffe nur mit funktionalem Nutzen, nicht als Dekoration
- Szenen mit messbarem Fortschritt: Information, Risiko oder Verlust
