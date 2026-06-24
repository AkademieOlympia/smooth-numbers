#!/usr/bin/env python3
"""
Erstellt einen wissenschaftstheoretischen Essay für Spectrum der Wissenschaft
über die 4D-Methodologie explorativer Mathematik.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def create_essay():
    """Erstellt das Essay-PDF."""
    
    # Ausgabepfad sicherstellen
    output_dir = "/Users/thomashoffbauer/Projects/smooth-numbers/catalan-normalform/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "spectrum_essay.pdf")
    
    # PDF-Dokument erstellen
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Story (Inhalt) sammeln
    story = []
    
    # Styles definieren
    styles = getSampleStyleSheet()
    
    # Benutzerdefinierte Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    author_style = ParagraphStyle(
        'Author',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        spaceAfter=40,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2a2a2a'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3a3a3a'),
        spaceAfter=10,
        spaceBefore=16,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        fontName='Helvetica'
    )
    
    quote_style = ParagraphStyle(
        'Quote',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        leftIndent=1*cm,
        rightIndent=1*cm,
        textColor=colors.HexColor('#444444'),
        fontName='Helvetica-Oblique',
        spaceAfter=12,
        spaceBefore=6
    )
    
    # Titel und Metadaten
    story.append(Paragraph("Jenseits des Beweises", title_style))
    story.append(Paragraph(
        "Wie explorative Mathematik die Grenzen wissenschaftlicher Erkenntnis neu vermisst",
        subtitle_style
    ))
    story.append(Paragraph("Thomas Hoffbauer", author_style))
    story.append(Spacer(1, 0.5*cm))
    
    # ===== EINLEITUNG =====
    story.append(Paragraph(
        "Im Sommer 1823 erreichte Carl Friedrich Gauß ein bemerkenswerter Brief. Der junge "
        "Mathematiker János Bolyai hatte eine Geometrie entwickelt, in der das Parallelenaxiom "
        "nicht galt – eine Idee, die zweitausend Jahre mathematischer Gewissheit in Frage stellte. "
        "Gauß' Antwort war verhalten enthusiastisch: Er selbst habe diese Gedanken schon vor "
        "Jahrzehnten gehabt, aber nie veröffentlicht, aus Furcht vor dem \"Geschrei der Böotier\".",
        body_style
    ))
    
    story.append(Paragraph(
        "Was Gauß fürchtete, war nicht die Widerlegung seiner Ideen – sondern ihre Unvollständigkeit. "
        "Die nicht-euklidische Geometrie war damals weder bewiesen noch widerlegt. Sie war etwas "
        "dazwischen: eine mathematische Exploration, deren Wert noch unklar war. In der strengen "
        "Dichotomie der reinen Mathematik – bewiesen oder nicht bewiesen – fand sich für solche "
        "Arbeiten kein Platz.",
        body_style
    ))
    
    story.append(Paragraph(
        "Fast zweihundert Jahre später steht die Mathematik vor einer ähnlichen Herausforderung. "
        "Computergestützte Experimente, maschinelles Lernen und datengetriebene Methoden erzeugen "
        "Muster und Vermutungen in nie dagewesenem Tempo. Doch die klassischen Kategorien der "
        "Wissenschaftstheorie – von Poppers Falsifikation über Kuhns Paradigmen bis zu Lakatos' "
        "Forschungsprogrammen – wurden für die Physik entwickelt, nicht für eine Disziplin, in der "
        "Wahrheit zeitlos und Beweis endgültig sein soll.",
        body_style
    ))
    
    story.append(Paragraph(
        "Ein aktuelles mathematisches Projekt, das sich selbst EABC nennt und die Verteilung von "
        "Primzahlen untersucht, hat über mehrere Monate eine Methodologie entwickelt, die einen "
        "neuen Ansatz verfolgt: Statt die klassische Dichotomie zu akzeptieren, schlägt sie vier "
        "orthogonale Dimensionen vor, entlang derer mathematischer Fortschritt gemessen werden kann. "
        "Diese Methodologie wirft grundlegende Fragen auf: Wie bewerten wir Wissen, das zwischen "
        "Vermutung und Beweis steht? Welche Rolle spielt Überraschung in der Wissenschaft? Und kann "
        "explorative Mathematik ebenso rigoros sein wie beweisgestützte?",
        body_style
    ))
    
    # ===== ABSCHNITT 1 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("1. Die Grenzen klassischer Kategorien", heading1_style))
    
    story.append(Paragraph(
        "Karl Popper revolutionierte die Wissenschaftstheorie mit einer simplen Einsicht: "
        "Wissenschaftliche Theorien können nie bewiesen, sondern nur widerlegt werden. Ein "
        "einzelner schwarzer Schwan genügt, um die Hypothese \"Alle Schwäne sind weiß\" zu Fall "
        "zu bringen. Diese Asymmetrie zwischen Verifikation und Falsifikation wurde zum "
        "Grundstein des modernen wissenschaftlichen Denkens.",
        body_style
    ))
    
    story.append(Paragraph(
        "In der Mathematik jedoch funktioniert Poppers Falsifikationismus nur bedingt. Ein "
        "mathematischer Beweis ist kein empirisches Experiment – er ist eine zeitlose logische "
        "Konstruktion. Der Satz des Pythagoras war vor dreitausend Jahren wahr und wird es in "
        "dreitausend Jahren noch sein. Neue Beobachtungen können ihn nicht widerlegen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Thomas Kuhn ergänzte Popper mit der Theorie wissenschaftlicher Revolutionen. "
        "Wissenschaft, so Kuhn, durchläuft Zyklen: Lange Phasen der \"Normalwissenschaft\", in "
        "denen Forscher Rätsel innerhalb eines bestehenden Paradigmas lösen, werden durch "
        "revolutionäre Umbrüche unterbrochen, in denen das gesamte Paradigma zusammenbricht und "
        "durch ein neues ersetzt wird. Die Entdeckung der Quantenmechanik war eine solche "
        "Revolution – eine fundamentale Neuordnung dessen, was Physiker unter \"Realität\" "
        "verstehen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Doch auch Kuhns Modell passt nicht perfekt zur Mathematik. Mathematische \"Revolutionen\" "
        "– wie die Entdeckung nicht-euklidischer Geometrie oder Cantors Mengenlehre – widerlegen "
        "das alte Paradigma nicht, sondern erweitern es. Die euklidische Geometrie wurde nicht "
        "falsch, als Bolyai und Lobatschewski hyperbolische Geometrien entdeckten. Sie wurde zu "
        "einem Spezialfall eines größeren Systems.",
        body_style
    ))
    
    story.append(Paragraph(
        "Imre Lakatos versuchte die Lücke zu schließen. Sein Konzept der \"Forschungsprogramme\" "
        "erkennt an, dass wissenschaftliche Theorien nicht isoliert existieren, sondern eingebettet "
        "sind in größere konzeptionelle Frameworks. Ein Forschungsprogramm besteht aus einem "
        "\"harten Kern\" unverrückbarer Prinzipien und einem \"Schutzgürtel\" veränderbarer "
        "Hilfshypothesen. Ein Programm ist progressiv, wenn es neue Phänomene vorhersagt; es ist "
        "degenerierend, wenn es nur noch ad-hoc-Erklärungen liefert.",
        body_style
    ))
    
    story.append(Paragraph(
        "Lakatos' Ansatz kommt der mathematischen Praxis näher. Die Entwicklung der Galoistheorie "
        "beispielsweise war ein progressives Forschungsprogramm: Sie begann mit der Frage nach "
        "Lösungsformeln für Polynomgleichungen und öffnete schließlich ein gesamtes Gebiet der "
        "abstrakten Algebra. Dennoch fehlt auch Lakatos eine Kategorie für jene Art von Mathematik, "
        "die weder progressiv noch degenerierend ist, sondern explorativ – Mathematik, die Strukturen "
        "untersucht, deren Wert noch unklar ist.",
        body_style
    ))
    
    # ===== ABSCHNITT 2 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("2. Die vier Dimensionen des mathematischen Fortschritts", heading1_style))
    
    story.append(Paragraph(
        "Das EABC-Projekt schlägt vor, mathematischen Fortschritt nicht entlang einer einzelnen "
        "Achse zu messen – bewiesen versus unbewiesen, revolutionär versus inkrementell – sondern "
        "entlang von vier unabhängigen Dimensionen:",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*cm))
    
    # Tabelle der vier Dimensionen
    table_data = [
        ['Dimension', 'Frage', 'Spektrum'],
        ['Evidenz', 'Wie sicher sind wir?', 'Beweis → Hypothese → Empirie → Interpretation → Spekulation'],
        ['Verständnis', 'Was verstehen wir?', 'Objekt → Struktur → Mechanismus'],
        ['Generativität', 'Was folgt daraus?', 'Lokal → Fruchtbar → Universell'],
        ['Überraschung', 'Wie unerwartet ist es?', 'Erwartbar → Interessant → Radikal überraschend']
    ]
    
    t = Table(table_data, colWidths=[3.5*cm, 4*cm, 9*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph(
        "Diese vier Dimensionen sind orthogonal: Eine Entdeckung kann auf einer Dimension stark "
        "und auf einer anderen schwach sein. Historische Beispiele illustrieren dies eindrücklich:",
        body_style
    ))
    
    story.append(Paragraph("Cantors Mengenlehre (1874)", heading2_style))
    
    story.append(Paragraph(
        "Georg Cantors Beweis, dass es verschiedene \"Größen\" von Unendlichkeit gibt, war "
        "mathematisch rigoros – die Evidenz war hoch. Doch die Idee widersprach so radikal der "
        "Intuition, dass selbst führende Mathematiker wie Leopold Kronecker sie als \"Krankheit\" "
        "bezeichneten. Die Überraschung war extrem hoch, während die unmittelbare Generativität "
        "gering schien. Erst Jahrzehnte später wurde klar, dass Cantor die Grundlagen der gesamten "
        "Mathematik neu geordnet hatte.",
        body_style
    ))
    
    story.append(Paragraph("Fourier-Analyse (1822)", heading2_style))
    
    story.append(Paragraph(
        "Joseph Fouriers Entdeckung, dass periodische Funktionen als Summen von Sinus- und "
        "Kosinuswellen dargestellt werden können, war unmittelbar generativ. Sie revolutionierte "
        "Physik, Signalverarbeitung und schließlich die gesamte angewandte Mathematik. Die "
        "Überraschung war moderat – die Idee schien zunächst ein technisches Werkzeug zu sein. "
        "Doch das Verständnis, das sie lieferte, war fundamental: Komplexe zeitliche Muster können "
        "in einfache Frequenzkomponenten zerlegt werden.",
        body_style
    ))
    
    story.append(Paragraph("Gödels Unvollständigkeitssatz (1931)", heading2_style))
    
    story.append(Paragraph(
        "Kurt Gödel bewies, dass kein formales System, das die Arithmetik umfasst, sowohl "
        "vollständig als auch widerspruchsfrei sein kann. Die Evidenz war unanfechtbar, die "
        "Überraschung radikal, das Verständnis tiefgreifend – doch die unmittelbare Generativität "
        "war gering. Gödels Satz öffnete kein neues Forschungsfeld, sondern schloss eines: Er "
        "zeigte, dass Hilberts Programm, die Mathematik vollständig zu formalisieren, prinzipiell "
        "unmöglich war. Dennoch gilt der Satz als eine der größten Leistungen der Mathematik des "
        "20. Jahrhunderts.",
        body_style
    ))
    
    story.append(Paragraph(
        "Diese Beispiele zeigen: Die Bewertung mathematischen Fortschritts erfordert eine "
        "Mehrdimensionalität, die klassische wissenschaftstheoretische Kategorien nicht erfassen. "
        "Ein Ergebnis kann wertvoll sein, weil es überraschend ist (Cantor), weil es generativ "
        "ist (Fourier) oder weil es das Verständnis vertieft (Gödel) – unabhängig davon, ob es "
        "sofort anwendbar oder intuitiv ist.",
        body_style
    ))
    
    # ===== ABSCHNITT 3 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("3. Evidenz als Spektrum: Die A-B-C-D-Hierarchie", heading1_style))
    
    story.append(Paragraph(
        "Die erste und vielleicht wichtigste Dimension ist die Evidenz. Hier schlägt die "
        "explorative Methodologie eine fünfstufige Hierarchie vor:",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "<b>Stufe A (Beweis):</b> Mathematisch rigoros bewiesen, zeitlos wahr. Beispiel: "
        "Der Satz des Pythagoras.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Stufe B (Hypothese):</b> Präzise formuliert und im Prinzip testbar, aber noch nicht "
        "getestet. Beispiel: Eine neue Vermutung über Primzahlverteilungen.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Stufe B+ (Empirie):</b> Empirisch getestet und gestützt. Beispiel: Eine Hypothese, "
        "die in Millionen von Fällen bestätigt wurde und deren Vorhersagekraft quantifiziert ist.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Stufe C (Interpretation):</b> Eine Deutung empirischer Befunde oder bewiesener "
        "Strukturen. Beispiel: \"Diese Struktur könnte mit Catalan-Zahlen zusammenhängen.\"",
        body_style
    ))
    story.append(Paragraph(
        "<b>Stufe D (Spekulation):</b> Eine noch ungetestete Idee oder Erweiterung. Beispiel: "
        "\"Vielleicht gibt es eine Verbindung zu Quaternionen.\"",
        body_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph(
        "Entscheidend ist die Regel: <b>Interpretationen (C) und Spekulationen (D) dürfen nur "
        "auf Evidenz (A, B+) aufbauen, nicht umgekehrt.</b> Diese Regel schützt vor einem "
        "klassischen Fehler explorativer Forschung: dass narrative Deutungen die Rolle von "
        "Evidenz übernehmen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Historisch war diese Trennung nicht immer klar. Die Atomtheorie im 19. Jahrhundert "
        "beispielsweise begann als Interpretation chemischer Reaktionsmuster (Stufe C), wurde "
        "durch kinetische Gastheorie und Brownsche Bewegung empirisch gestützt (Stufe B+) und "
        "schließlich durch Quantenmechanik mathematisch fundiert (Stufe A). Doch in der "
        "Zwischenzeit gab es heftige Debatten, weil Interpretation und Evidenz vermischt wurden.",
        body_style
    ))
    
    story.append(Paragraph(
        "Das EABC-Projekt illustriert die Hierarchie konkret. Eine zentrale Beobachtung des "
        "Projekts ist die Korrespondenz zwischen seiner EABC-Klassifikation von Primzahlen und "
        "dem Spaltungsverhalten dieser Primzahlen in zwei klassischen zahlentheoretischen "
        "Strukturen: den Gaußschen Zahlen ℤ[i] und den Eisenstein-Zahlen ℤ[ω].",
        body_style
    ))
    
    story.append(Paragraph(
        "Jede Primzahl p > 3 fällt in eine von vier Klassen modulo 12: 1, 5, 7 oder 11. Diese "
        "Klassifikation scheint zunächst willkürlich. Doch sie kodiert präzise, wie p sich in "
        "zwei verschiedenen Erweiterungen der ganzen Zahlen verhält:",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "• Primzahlen ≡ 1 (mod 12) spalten sowohl in ℤ[i] als auch in ℤ[ω]",
        body_style
    ))
    story.append(Paragraph(
        "• Primzahlen ≡ 5 (mod 12) spalten nur in ℤ[i]",
        body_style
    ))
    story.append(Paragraph(
        "• Primzahlen ≡ 7 (mod 12) spalten nur in ℤ[ω]",
        body_style
    ))
    story.append(Paragraph(
        "• Primzahlen ≡ 11 (mod 12) bleiben in beiden Körpern unteilbar",
        body_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph(
        "Diese Korrespondenz ist <b>Stufe A</b> – sie folgt aus dem Chinesischen Restsatz und "
        "klassischen Spaltungssätzen der algebraischen Zahlentheorie. Die EABC-Klassifikation "
        "ist damit keine projektspezifische Konstruktion, sondern ein Objekt der klassischen "
        "Mathematik.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die Frage jedoch, ob diese zahlentheoretische Information etwas über andere "
        "Eigenschaften von Zahlen aussagt – etwa über ihre kombinatorischen Strukturen – ist "
        "<b>Stufe B</b>: eine testbare Hypothese. Das Projekt hat diese Hypothese empirisch "
        "geprüft und festgestellt, dass ein bestimmtes Konzentrationsmaß H(n), das auf der "
        "EABC-Klassifikation basiert, tatsächlich zusätzliche Varianz erklärt – ein Effekt von "
        "ΔR² = 0.22, reproduzierbar über Millionen von Datenpunkten. Das ist <b>Stufe B+</b>.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die Deutung, warum dieser Zusammenhang besteht – ob er mit Catalan-Zahlen, geometrischen "
        "Strukturen oder anderen mathematischen Objekten zusammenhängt – ist <b>Stufe C</b>. "
        "Und die Spekulation, ob er sich auf Quaternionen oder Oktonionen verallgemeinern lässt, "
        "ist <b>Stufe D</b>.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die Hierarchie erzwingt Disziplin: Jede neue Interpretation muss auf Evidenz aufbauen, "
        "nicht auf anderen Interpretationen. Das unterscheidet explorative Mathematik von bloßer "
        "Spekulation.",
        body_style
    ))
    
    # ===== ABSCHNITT 4 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("4. Überraschung als wissenschaftlicher Wert", heading1_style))
    
    story.append(Paragraph(
        "Die vierte Dimension – Überraschung – ist die am meisten vernachlässigte in der "
        "Wissenschaftstheorie. Popper, Kuhn und Lakatos sprechen von Falsifikation, Paradigmen "
        "und Forschungsprogrammen, aber nicht von Überraschung. Dabei ist Überraschung historisch "
        "oft der Indikator für die tiefsten Entdeckungen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Als Giuseppe Peano 1890 eine stetige Kurve konstruierte, die ein Quadrat vollständig "
        "ausfüllt, war die Reaktion der mathematischen Community ungläubig. Eine eindimensionale "
        "Linie kann nicht zweidimensional sein – so schien es. Peanos Konstruktion war radikal "
        "überraschend, weil sie eine fundamentale Intuition über Dimension zerstörte. Sie führte "
        "zur Entwicklung der Topologie als eigenständiger Disziplin.",
        body_style
    ))
    
    story.append(Paragraph(
        "Das EABC-Projekt berichtet von zwei überraschenden Befunden. Der erste betrifft die "
        "sogenannte Gap-Dynamik: die Verteilung der Abstände zwischen aufeinanderfolgenden "
        "Primzahlen. Die naive Erwartung wäre, dass diese Abstände (modulo 12) symmetrisch "
        "verteilt sind. Doch die Daten zeigen eine klare Asymmetrie: Abstände, die kongruent "
        "zu 2 oder 4 modulo 12 sind, treten häufiger auf als jene, die kongruent zu 8 oder 10 "
        "sind.",
        body_style
    ))
    
    story.append(Paragraph(
        "Diese Asymmetrie ist überraschend, weil sie eine Ordnung im scheinbaren Chaos der "
        "Primzahlen offenlegt. Noch überraschender ist ein zweiter Befund: Primzahlen sind "
        "\"geregelter\" als zufällige Modelle, aber \"weniger geregelt\" als Poisson-Prozesse. "
        "Das widerspricht der verbreiteten Intuition, dass Primzahlen entweder \"zufällig\" "
        "oder \"hochstrukturiert\" sein sollten. Sie sind beides – und dazwischen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Überraschung hat wissenschaftlichen Wert, weil sie auf fehlerhafte Intuitionen hinweist. "
        "Eine überraschende Entdeckung sagt: \"Die Welt ist anders, als du dachtest.\" Das ist "
        "nicht dasselbe wie Falsifikation im Popperschen Sinne – keine Theorie wurde widerlegt. "
        "Es ist vielmehr eine Korrektur impliziter Annahmen, die nie explizit formuliert wurden.",
        body_style
    ))
    
    story.append(Paragraph(
        "In Lakatos' Terminologie könnte man sagen: Überraschung ist ein Signal, dass der "
        "\"Schutzgürtel\" eines Forschungsprogramms revidiert werden muss. Doch sie ist mehr als "
        "das. Eine radikale Überraschung – wie Cantors Unendlichkeiten oder Gödels Unvollständigkeit – "
        "hinterfragt den \"harten Kern\" selbst.",
        body_style
    ))
    
    # ===== ABSCHNITT 5 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("5. Informationsgewinn statt Objektfindung", heading1_style))
    
    story.append(Paragraph(
        "Ein zentrales Prinzip der explorativen Methodologie lautet: <b>Eine Struktur ist erst "
        "dann wissenschaftlich relevant, wenn sie Information komprimiert.</b> Das verschiebt "
        "den Fokus von der Existenz eines mathematischen Objekts zu seinem Informationsgehalt.",
        body_style
    ))
    
    story.append(Paragraph(
        "In der Physik ist dieser Gedanke selbstverständlich. Eine Theorie, die jedes Experiment "
        "\"erklärt\", indem sie für jeden Datenpunkt einen eigenen Parameter einführt, ist "
        "wertlos. Sie komprimiert keine Information – sie rekapituliert sie nur. Die Newtonschen "
        "Bewegungsgesetze hingegen komprimieren die Bewegung von Planeten, Äpfeln und Kanonenkugeln "
        "in drei einfache Gleichungen.",
        body_style
    ))
    
    story.append(Paragraph(
        "In der Mathematik ist die Rolle von Informationskompression subtiler. Die Fourier-"
        "Transformation komprimiert keine empirischen Daten – sie transformiert sie in einen "
        "anderen Darstellungsraum, in dem bestimmte Muster einfacher sichtbar werden. Eine "
        "periodische Funktion, die im Zeitbereich kompliziert aussieht, wird im Frequenzbereich "
        "zu einer Handvoll scharfer Peaks.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die explorative Methodologie unterscheidet zwei Arten von Informationsgewinn:",
        body_style
    ))
    
    story.append(Paragraph(
        "<b>Prädiktiver Informationsgewinn:</b> Eine neue Struktur erklärt zusätzliche Varianz "
        "in beobachteten Daten. Das ist messbar durch Kennzahlen wie ΔR² (Änderung des "
        "Bestimmtheitsmaßes), AIC (Akaike-Informationskriterium) oder Kreuzvalidierung. Für das "
        "EABC-Projekt bedeutet dies: Erklärt die EABC-Klassifikation etwas, das einfachere "
        "Modelle nicht erklären? Die Antwort ist ja: ΔR² = 0.22.",
        body_style
    ))
    
    story.append(Paragraph(
        "<b>Struktureller Informationsgewinn:</b> Eine neue Struktur vereinfacht ein Problem oder "
        "verbindet es mit etablierter Theorie. Das ist schwerer zu quantifizieren, aber historisch "
        "oft wichtiger. Die Galoistheorie zum Beispiel lieferte keinen \"prädiktiven\" Gewinn – "
        "sie sagte nicht voraus, welche Gleichungen lösbar sind (das wusste man bereits empirisch). "
        "Aber sie erklärte, warum bestimmte Gleichungen unlösbar sind, indem sie das Problem in die "
        "Sprache der Gruppentheorie übersetzte.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die EABC-Klassifikation liefert beide Arten. Strukturell verbindet sie eine "
        "projektspezifische Idee mit der klassischen Theorie der Gaußschen und Eisenstein-Zahlen. "
        "Prädiktiv erklärt sie zusätzliche Varianz in kombinsatorischen Strukturen. Das ist selten: "
        "Die meisten mathematischen Ideen sind entweder strukturell oder prädiktiv stark, nicht "
        "beides.",
        body_style
    ))
    
    story.append(Paragraph(
        "Das Prinzip des Informationsgewinns schützt vor einer Versuchung der explorativen "
        "Mathematik: dem Objekt-Fetischismus. Es reicht nicht, ein interessantes mathematisches "
        "Objekt zu finden. Die entscheidende Frage ist: Komprimiert dieses Objekt Information? "
        "Vereinfacht es etwas? Erklärt es etwas? Wenn nicht, ist es wissenschaftlich irrelevant, "
        "egal wie elegant seine Definition ist.",
        body_style
    ))
    
    # ===== ABSCHNITT 6 =====
    story.append(PageBreak())
    story.append(Paragraph("6. Explorative Mathematik als Forschungsprogramm", heading1_style))
    
    story.append(Paragraph(
        "Wie verhält sich explorative Mathematik zu Lakatos' Konzept der Forschungsprogramme? "
        "Lakatos unterschied zwischen progressiven und degenerierenden Programmen. Ein Programm "
        "ist progressiv, wenn es neue, überprüfbare Vorhersagen macht. Es ist degenerierend, wenn "
        "es nur noch ad-hoc-Anpassungen vornimmt, um empirische Anomalien zu erklären.",
        body_style
    ))
    
    story.append(Paragraph(
        "Das EABC-Projekt begann spekulativ. Frühe Phasen (2024-2025) waren geprägt von "
        "geometrisch-metaphorischen Deutungen: Klein-Flaschen, Chiralität, Quaternionen. Diese "
        "Interpretationen waren anregend, aber nicht testbar. In Lakatos' Terminologie war das "
        "ein degenerierendes Programm: Es erzeugte Narrative, aber keine Vorhersagen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die reife Phase (2026) vollzog eine methodische Transformation. Das Projekt führte die "
        "A-B-C-D-Hierarchie ein und machte ΔR² zum zentralen Prüfstein. Interpretationen wurden "
        "erst nach empirischer Evidenz zugelassen. Spekulationen wurden explizit als Stufe D "
        "markiert. Plötzlich war das Programm progressiv: Es machte testbare Vorhersagen – etwa, "
        "dass die Gap-Asymmetrie auch modulo 30 erscheinen sollte – und prüfte sie systematisch.",
        body_style
    ))
    
    story.append(Paragraph(
        "Diese Transformation ist lehrreich. Sie zeigt, dass ein Forschungsprogramm von "
        "degenerierend zu progressiv werden kann, wenn es seine Methodologie verschärft. Doch "
        "sie zeigt auch eine Grenze von Lakatos' Modell: Die Progressivität eines Programms hängt "
        "nicht nur von seinen Vorhersagen ab, sondern von der Qualität seiner Methodologie.",
        body_style
    ))
    
    story.append(Paragraph(
        "Ein Programm kann viele Vorhersagen machen und dennoch degenerierend sein, wenn diese "
        "Vorhersagen auf schwacher Evidenz basieren. Umgekehrt kann ein Programm wenige Vorhersagen "
        "machen und dennoch progressiv sein, wenn es tiefes Verständnis liefert. Die 4D-Methodologie "
        "erfasst diese Nuancen, die Lakatos' binäre Unterscheidung verpasst.",
        body_style
    ))
    
    story.append(Paragraph(
        "Lakatos' größte Einsicht war, dass Forschungsprogramme durch ihren \"harten Kern\" und "
        "ihren \"Schutzgürtel\" definiert sind. Der harte Kern der explorativen Methodologie besteht "
        "aus drei Prinzipien:",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph(
        "1. <b>Information statt Objekt:</b> Eine Struktur ist erst dann relevant, wenn sie "
        "Information komprimiert.",
        body_style
    ))
    story.append(Paragraph(
        "2. <b>Evidenz vor Interpretation:</b> Interpretationen dürfen nur auf empirischer "
        "Evidenz aufbauen, nicht umgekehrt.",
        body_style
    ))
    story.append(Paragraph(
        "3. <b>Mehrdimensionale Bewertung:</b> Fortschritt wird entlang von Evidenz, Verständnis, "
        "Generativität und Überraschung gemessen.",
        body_style
    ))
    story.append(Spacer(1, 0.2*cm))
    
    story.append(Paragraph(
        "Diese Prinzipien bilden einen \"harten Kern\", der nicht verhandelbar ist. Der "
        "\"Schutzgürtel\" besteht aus spezifischen Hypothesen – etwa über Gap-Asymmetrie oder "
        "Catalan-Strukturen – die getestet, revidiert oder verworfen werden können, ohne den "
        "Kern zu gefährden.",
        body_style
    ))
    
    # ===== ABSCHNITT 7 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("7. Historische Präzedenzfälle: Fourier und Galois", heading1_style))
    
    story.append(Paragraph(
        "Die explorative Methodologie ist nicht neu – sie beschreibt, retrospektiv betrachtet, "
        "wie viele große mathematische Ideen tatsächlich entstanden sind. Zwei historische "
        "Beispiele illustrieren dies:",
        body_style
    ))
    
    story.append(Paragraph("Joseph Fourier und die Wärmeleitungsgleichung (1822)", heading2_style))
    
    story.append(Paragraph(
        "Als Fourier seine Théorie analytique de la chaleur veröffentlichte, stieß er auf "
        "heftigen Widerstand. Seine Behauptung, dass jede periodische Funktion als Summe von "
        "Sinus- und Kosinuswellen dargestellt werden könne, erschien absurd. Wie konnte eine "
        "eckige Funktion – etwa eine Sägezahnwelle – durch glatte Wellen approximiert werden?",
        body_style
    ))
    
    story.append(Paragraph(
        "Fouriers Arbeit war zunächst <b>explorativ</b>. Er hatte keine vollständige Theorie der "
        "Konvergenz (die Evidenz war lückenhaft), aber er hatte etwas anderes: eine Methode, die "
        "<b>funktionierte</b>. Seine Fourier-Reihen lösten Probleme, die zuvor unlösbar schienen. "
        "Der strukturelle Informationsgewinn war enorm – und das genügte, um das Programm "
        "progressiv zu machen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Erst im Laufe des 19. Jahrhunderts wurde die Theorie vollständig fundiert. Dirichlet, "
        "Riemann und Lebesgue fanden die fehlenden Konvergenzbedingungen. Die Fourier-Analyse "
        "wurde von Stufe B+ (empirisch gestützt) zu Stufe A (bewiesen). Doch die Generativität – "
        "die Anwendungen in Physik, Signalverarbeitung, Quantenmechanik – entstand bereits in der "
        "explorativen Phase.",
        body_style
    ))
    
    story.append(Paragraph("Évariste Galois und die Gruppentheorie (1832)", heading2_style))
    
    story.append(Paragraph(
        "Évariste Galois starb mit 20 Jahren in einem Duell. In der Nacht vor seinem Tod schrieb "
        "er fieberhaft eine Zusammenfassung seiner mathematischen Ideen. Diese Notizen – chaotisch, "
        "unvollständig, kaum lesbar – enthielten die Grundlagen der modernen Algebra.",
        body_style
    ))
    
    story.append(Paragraph(
        "Galois' Idee war radikal: Die Lösbarkeit einer Polynomgleichung hängt nicht von der "
        "Gleichung selbst ab, sondern von den Symmetrien ihrer Lösungen. Diese Symmetrien bilden "
        "eine algebraische Struktur – eine Gruppe. Ob die Gleichung durch Radikale lösbar ist, "
        "wird durch Eigenschaften dieser Gruppe bestimmt.",
        body_style
    ))
    
    story.append(Paragraph(
        "Galois' Arbeit war zunächst unverständlich. Sie wurde 14 Jahre lang ignoriert, bis Liouville "
        "sie 1846 veröffentlichte. Selbst dann dauerte es Jahrzehnte, bis ihre Bedeutung erkannt "
        "wurde. Das Problem war nicht die Evidenz – Galois' Beweise waren korrekt. Das Problem war "
        "das Verständnis: Seine Ideen waren so weit ihrer Zeit voraus, dass niemand den "
        "konzeptionellen Sprung nachvollziehen konnte.",
        body_style
    ))
    
    story.append(Paragraph(
        "In der 4D-Terminologie war Galois' Arbeit stark auf allen vier Achsen: hohe Evidenz "
        "(korrekte Beweise), tiefes Verständnis (Symmetrien als Schlüssel), extreme Generativität "
        "(Geburt der abstrakten Algebra) und hohe Überraschung (Gruppe als zentrales Konzept). "
        "Doch ihre Akzeptanz erforderte eine kulturelle Transformation – einen kleinen Kuhn'schen "
        "Paradigmenwechsel.",
        body_style
    ))
    
    # ===== ABSCHNITT 8 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("8. Die Rolle numerischer Experimente", heading1_style))
    
    story.append(Paragraph(
        "Moderne explorative Mathematik ist untrennbar mit numerischen Experimenten verbunden. "
        "Computer ermöglichen es, Millionen von Fällen zu testen, Muster zu erkennen und "
        "Hypothesen zu generieren. Doch diese Methode ist umstritten.",
        body_style
    ))
    
    story.append(Paragraph(
        "Kritiker argumentieren, dass numerische Evidenz keine mathematische Wahrheit liefert. "
        "Die Primzahlvermutung von Riemann ist für die ersten 10 Billionen Nullstellen der "
        "Zeta-Funktion bestätigt – doch das ist kein Beweis. Ein einziges Gegenbeispiel würde "
        "genügen, um sie zu widerlegen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Diese Kritik ist berechtigt, aber sie verkennt die Rolle numerischer Experimente. Sie "
        "liefern keine Beweise, aber sie liefern etwas anderes: <b>Evidenz der Stufe B+</b>. "
        "Eine Hypothese, die in Milliarden von Fällen bestätigt ist, ist nicht bewiesen – aber "
        "sie ist auch nicht belanglos.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die explorative Methodologie erkennt dies an. Sie unterscheidet explizit zwischen Stufe A "
        "(Beweis) und Stufe B+ (empirische Evidenz). Eine B+-Aussage ist weniger sicher als eine "
        "A-Aussage – aber sie ist immer noch wertvoll, wenn sie prädiktiven oder strukturellen "
        "Informationsgewinn liefert.",
        body_style
    ))
    
    story.append(Paragraph(
        "Ein Beispiel: Die Gap-Asymmetrie im EABC-Projekt ist nicht bewiesen. Aber sie ist über "
        "Millionen von Primzahlen reproduzierbar, und sie erklärt zusätzliche Varianz mit einem "
        "messbaren Effekt. Das macht sie zu einer robusten Stufe-B+-Aussage. Interpretationen "
        "(Stufe C) dürfen darauf aufbauen – solange klar bleibt, dass sie auf empirischer, nicht "
        "logischer Gewissheit beruhen.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die Geschichte der Mathematik zeigt, dass viele große Vermutungen Jahrzehnte oder "
        "Jahrhunderte als Stufe B+ existierten, bevor sie zu Stufe A wurden. Fermats letzter Satz "
        "war 358 Jahre lang eine Vermutung, bevor Andrew Wiles ihn 1994 bewies. In dieser Zeit "
        "war die Vermutung nicht wertlos – sie trieb die Entwicklung der algebraischen Zahlentheorie "
        "voran. Ihr Wert lag nicht in ihrer Beweisbarkeit, sondern in ihrer Generativität.",
        body_style
    ))
    
    # ===== ABSCHNITT 9 =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("9. Implikationen für die Wissenschaftstheorie", heading1_style))
    
    story.append(Paragraph(
        "Die explorative Methodologie wirft grundlegende Fragen für die Wissenschaftstheorie auf. "
        "Wenn Mathematik – die \"reinste\" Wissenschaft – eine Evidenzhierarchie jenseits von "
        "Beweis und Widerlegung benötigt, was bedeutet das für empirische Wissenschaften?",
        body_style
    ))
    
    story.append(Paragraph(
        "Popper trennte Wissenschaft von Pseudowissenschaft durch Falsifizierbarkeit. Eine Theorie "
        "ist wissenschaftlich, wenn sie im Prinzip widerlegt werden kann. Doch das EABC-Projekt "
        "zeigt eine Nuance: Nicht alle wissenschaftlichen Aussagen sind binär (wahr/falsch). Manche "
        "sind graduell (mehr oder weniger evident, mehr oder weniger informativ).",
        body_style
    ))
    
    story.append(Paragraph(
        "Die 4D-Methodologie schlägt vor, dass wissenschaftlicher Fortschritt ein "
        "mehrdimensionaler Raum ist. Eine Theorie kann auf einer Dimension schwach sein (niedrige "
        "Evidenz) und dennoch wertvoll (hohe Generativität oder Überraschung). Darwins "
        "Evolutionstheorie hatte 1859 geringe direkte Evidenz – Fossilien waren spärlich, Genetik "
        "unbekannt – aber enorme Erklärungskraft und Generativität. Erst im 20. Jahrhundert wurde "
        "die Evidenz überwältigend.",
        body_style
    ))
    
    story.append(Paragraph(
        "Kuhn beschrieb Wissenschaft als Abfolge von Normalwissenschaft und Revolutionen. Doch die "
        "explorative Methodologie zeigt eine dritte Phase: <b>explorative Wissenschaft</b>. In "
        "dieser Phase existieren Ideen, die weder \"Normal\" (etabliertes Paradigma) noch "
        "\"revolutionär\" (Paradigmenwechsel) sind. Sie sind explorativ: noch nicht vollständig "
        "fundiert, aber bereits fruchtbar.",
        body_style
    ))
    
    story.append(Paragraph(
        "Lakatos' Forschungsprogramme kommen dem am nächsten. Doch auch Lakatos fehlte eine "
        "explizite Rolle für Überraschung und eine quantitative Metrik für Informationsgewinn. "
        "Die 4D-Methodologie ergänzt Lakatos, indem sie diese Lücken füllt.",
        body_style
    ))
    
    story.append(Paragraph(
        "Eine tiefere Implikation betrifft die Natur mathematischer Wahrheit. In der klassischen "
        "Sicht ist Mathematik die Wissenschaft zeitloser Wahrheiten. Ein bewiesener Satz war immer "
        "wahr, auch bevor er bewiesen wurde. Doch diese Sicht verbirgt den prozessualen Charakter "
        "mathematischer Erkenntnis. Ideen entwickeln sich. Sie beginnen als vage Intuitionen "
        "(Stufe D), werden zu testbaren Hypothesen (Stufe B), sammeln empirische Evidenz (Stufe B+) "
        "und werden schließlich bewiesen (Stufe A) – oder widerlegt.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die explorative Methodologie macht diesen Prozess explizit. Sie akzeptiert, dass Mathematik "
        "nicht nur aus bewiesenen Sätzen besteht, sondern auch aus robusten Vermutungen, "
        "überraschenden Mustern und generativen Strukturen. Sie erweitert den Raum dessen, was als "
        "\"mathematisches Wissen\" gilt, ohne die Strenge zu opfern.",
        body_style
    ))
    
    # ===== SCHLUSS =====
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("10. Jenseits des Beweises", heading1_style))
    
    story.append(Paragraph(
        "Im Jahr 1913 erhielt G.H. Hardy einen merkwürdigen Brief aus Indien. Ein unbekannter "
        "Angestellter namens Srinivasa Ramanujan behauptete, Hunderte neuer mathematischer Formeln "
        "entdeckt zu haben – ohne Beweise. Hardy war zunächst skeptisch. Cranks schickten ihm "
        "ständig angebliche \"Entdeckungen\". Doch als er Ramanujans Formeln studierte, erkannte "
        "er ihren Wert. \"Sie müssen wahr sein\", schrieb er später, \"denn wenn sie es nicht wären, "
        "hätte niemand die Phantasie, sie zu erfinden.\"",
        body_style
    ))
    
    story.append(Paragraph(
        "Ramanujan arbeitete explorativ. Viele seiner Formeln waren nicht bewiesen – manche sind es "
        "bis heute nicht. Dennoch revolutionierten sie die Zahlentheorie. Ihr Wert lag nicht in "
        "ihrer Evidenz, sondern in ihrer Generativität und Überraschung. Sie öffneten Türen zu "
        "neuen mathematischen Landschaften.",
        body_style
    ))
    
    story.append(Paragraph(
        "Das EABC-Projekt ist kein Ramanujan-Moment – es beansprucht keine revolutionären Durchbrüche. "
        "Aber es ist ein Fallbeispiel für eine methodische Innovation: die systematische Trennung "
        "von Evidenz, Verständnis, Generativität und Überraschung. Es zeigt, dass explorative "
        "Mathematik ebenso rigoros sein kann wie beweisgestützte, wenn sie sich an klare Prinzipien "
        "hält.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die Transformation von einer Suche nach interessanten Objekten zu einer Messung von "
        "Informationsgewinn ist subtil, aber fundamental. Sie verschiebt die Frage von \"Was haben "
        "wir gefunden?\" zu \"Welche zusätzliche Information liefert das, was wir gefunden haben?\" "
        "Diese Frage ist empirisch beantwortbar, reproduzierbar und falsifizierbar – selbst in der "
        "Mathematik.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die klassischen Kategorien der Wissenschaftstheorie – Poppers Falsifikation, Kuhns Paradigmen, "
        "Lakatos' Forschungsprogramme – wurden für eine Welt entworfen, in der Theorien entweder "
        "wahr oder falsch, progressiv oder degenerierend, revolutionär oder inkrementell sind. Doch "
        "die Wirklichkeit wissenschaftlicher Praxis ist reicher. Ideen existieren in einem "
        "mehrdimensionalen Raum, in dem Evidenz, Verständnis, Generativität und Überraschung "
        "unabhängige Werte haben.",
        body_style
    ))
    
    story.append(Paragraph(
        "Die 4D-Methodologie ist ein Versuch, diesen Raum zu kartieren. Sie ist weder perfekt noch "
        "vollständig. Die Achsen sind teilweise subjektiv, die Übergänge zwischen Stufen fließend. "
        "Doch sie bietet etwas, das die klassischen Kategorien nicht bieten: einen systematischen "
        "Rahmen für die Bewertung explorativer Forschung, der ihre Stärken anerkennt, ohne ihre "
        "Grenzen zu verschleiern.",
        body_style
    ))
    
    story.append(Paragraph(
        "Gauß fürchtete das Geschrei der Böotier. Bolyai veröffentlichte seine nicht-euklidische "
        "Geometrie dennoch – unsicher, spekulativ, aber fruchtbar. Heute ist sie Grundlage der "
        "Allgemeinen Relativitätstheorie. Nicht jede explorative Idee wird Bestand haben. Aber die "
        "Methode, mit der wir sie bewerten – nicht als bewiesen oder widerlegt, sondern als mehr "
        "oder weniger evident, mehr oder weniger fruchtbar, mehr oder weniger überraschend – könnte "
        "der Weg sein, wie Wissenschaft im 21. Jahrhundert funktioniert.",
        body_style
    ))
    
    story.append(Paragraph(
        "Jenseits des Beweises liegt nicht das Chaos der Spekulation. Es liegt ein Spektrum "
        "strukturierter Unsicherheit, das ebenso rigoros erforscht werden kann wie die Welt der "
        "bewiesenen Sätze. Die Frage ist nicht, ob wir diesen Raum betreten sollen – wir sind "
        "bereits dort. Die Frage ist, ob wir ihn mit Methoden ausstatten, die seiner Komplexität "
        "gerecht werden.",
        body_style
    ))
    
    story.append(Spacer(1, 1*cm))
    
    # Fußnote / Box
    story.append(Paragraph(
        "<b>Über den Autor:</b> Thomas Hoffbauer forscht an der Schnittstelle von Zahlentheorie, "
        "Kombinatorik und explorativer Mathematik. Das EABC-Projekt ist ein mehrjähriges "
        "Forschungsprogramm zur Untersuchung von Primzahlstrukturen und deren Verbindung zu "
        "kombinatorischen Objekten.",
        quote_style
    ))
    
    # PDF erstellen
    doc.build(story)
    
    return output_path

if __name__ == "__main__":
    output_path = create_essay()
    print(f"Essay erstellt: {output_path}")
