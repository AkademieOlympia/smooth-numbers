#!/usr/bin/env python3
"""
Erstellt ein professionelles Start-Dokument für das Catalan-Normalform-Projekt
mit Zielprojektion und Forschungsplan.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime

def create_header_footer(canvas_obj, doc):
    """Erstellt Kopf- und Fußzeile"""
    canvas_obj.saveState()
    
    # Fußzeile
    canvas_obj.setFont('Helvetica', 9)
    canvas_obj.setFillColor(colors.grey)
    footer_text = f"Catalan-Normalform Projekt | {datetime.now().strftime('%B %Y')}"
    canvas_obj.drawCentredString(A4[0]/2, 1.5*cm, footer_text)
    
    # Seitenzahl
    page_num = canvas_obj.getPageNumber()
    canvas_obj.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Seite {page_num}")
    
    canvas_obj.restoreState()

def create_start_document():
    """Erstellt das Start-Dokument"""
    
    filename = "output/pdf/catalan_normalform_start.pdf"
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#555555'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Oblique'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )
    
    box_style = ParagraphStyle(
        'BoxStyle',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.HexColor('#1a1a1a'),
        alignment=TA_CENTER,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    # Story (Inhalt)
    story = []
    
    # --- Titelseite ---
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Spektrale Catalan-Geometrie", title_style))
    story.append(Paragraph("der EABC-Arithmetik", title_style))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Mathematisch präzises Forschungsprogramm", subtitle_style))
    story.append(Spacer(1, 1*cm))
    
    # Info-Box
    info_data = [
        ['Projekttyp:', 'Grundlagenforschung Zahlentheorie'],
        ['Status:', 'Initialisierung'],
        ['Laufzeit:', '6-12 Monate (geplant)'],
        ['Methodik:', 'Hypothesengetrieben, falsifizierbar'],
        ['Datum:', datetime.now().strftime('%d.%m.%Y')]
    ]
    
    info_table = Table(info_data, colWidths=[4*cm, 10*cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(info_table)
    story.append(PageBreak())
    
    # --- Executive Summary ---
    story.append(Paragraph("1. Executive Summary", heading1_style))
    
    story.append(Paragraph(
        "Die bisherige EABC-Theorie klassifiziert Zahlen <b>lokal</b> über Restklassen "
        "und Primfaktoren. Die Catalan-Erweiterung fügt eine <b>globale</b> Ebene hinzu: "
        "die hierarchische Verschaltung dieser Faktoren.",
        body_style
    ))
    
    story.append(Spacer(1, 0.5*cm))
    
    # Zentrale Box
    central_box = Table(
        [['Arithmetische Komplexität = Faktorinhalt + Faktorarchitektur']],
        colWidths=[14*cm]
    )
    central_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 13),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(central_box)
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph(
        "Das Projekt ist <b>falsifizierbar</b>: Jede Hypothese besitzt ein Nullmodell, "
        "eine Teststatistik und ein Signifikanzkriterium.",
        body_style
    ))
    
    # --- Zentrale Forschungsfrage ---
    story.append(Paragraph("2. Zentrale Forschungsfrage", heading1_style))
    
    question_box = Table(
        [[Paragraph(
            "Bleibt nach Entfernung der trivialen Ω(n)- und Kanonisierungs-Effekte "
            "ein arithmetischer Rest in der Catalan-Hierarchie?",
            box_style
        )]],
        colWidths=[14*cm]
    )
    question_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f4f8')),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3498db')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(question_box)
    
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Formal: M<sub>C</sub><super>res</super>(n) ≠ 0 und korreliert mit "
        "EABC-/Spektralobservablen?",
        body_style
    ))
    
    # --- Hypothesen-Übersicht ---
    story.append(PageBreak())
    story.append(Paragraph("3. Zehn Hypothesen", heading1_style))
    
    hypotheses_data = [
        ['Nr.', 'Hypothese', 'Testbar'],
        ['H1', 'Kanonische Stabilität', 'Korrelationstest'],
        ['H2', 'Ensemble-Baseline', 'Varianzzerlegung'],
        ['H3', 'EABC-Kopplung', 'Mutual Information'],
        ['H4', 'Spektrale Korrelation', 'Permutationstest'],
        ['H5', 'Chaos-Korrelation', 'Brody-Parameter'],
        ['H6', 'Collatz-Korrelation', 'Residualanalyse'],
        ['H7', 'Skalengesetz', 'Potenzgesetz-Fit'],
        ['H8', 'Krümmung', 'Ollivier-Ricci'],
        ['H9', 'Tensor-Spektrum', 'IPR-Extremum'],
        ['H10', 'Null-Modell (Kontrolle)', 'R²-Test'],
    ]
    
    hyp_table = Table(hypotheses_data, colWidths=[1.5*cm, 8*cm, 4.5*cm])
    hyp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(hyp_table)
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "<b>Wichtig:</b> H10 (Null-Modell) ist der härteste Test. "
        "Falls bestätigt, sind H1-H9 falsifiziert und die Theorie ist trivial.",
        body_style
    ))
    
    # --- Experimenteller Fahrplan ---
    story.append(PageBreak())
    story.append(Paragraph("4. Experimenteller Fahrplan", heading1_style))
    
    experiments_data = [
        ['Phase', 'Experiment', 'Ziel', 'Dauer'],
        ['1', 'Tamari-Baseline', 'Reine Catalan-Geometrie verstehen', '2 Wochen'],
        ['2', 'Kanonisierungstest', 'Robustheit der Observable prüfen', '1 Woche'],
        ['3', 'Residualisierung', 'Trivialen Omega(n)-Effekt entfernen', '1 Woche'],
        ['4', 'EABC-Information', 'Lokale-globale Kopplung messen', '2 Wochen'],
        ['5', 'Spektralvergleich', 'Korrelation mit bekannten Observablen', '2 Wochen'],
    ]
    
    exp_table = Table(experiments_data, colWidths=[1.5*cm, 4.5*cm, 6*cm, 2*cm])
    exp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(exp_table)
    
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "<b>Gesamtdauer:</b> 8 Wochen (Kernexperimente)",
        body_style
    ))
    
    # --- Zielprojektion ---
    story.append(Paragraph("5. Zielprojektion", heading1_style))
    
    story.append(Paragraph("5.1 Kurzfristig (2 Monate)", heading2_style))
    story.append(Paragraph(
        "• Implementierung der Tamari-Graph-Konstruktion (k=2,...,12)<br/>"
        "• Berechnung von Ensemble-Baselines<br/>"
        "• Erste Kanonisierungstests an 10⁶ Zahlen<br/>"
        "• Entscheidung über H10 (Null-Modell)",
        body_style
    ))
    
    story.append(Paragraph("5.2 Mittelfristig (6 Monate)", heading2_style))
    story.append(Paragraph(
        "• Vollständige Tests von H1-H9<br/>"
        "• Spektrale Analyse des gekoppelten Operators<br/>"
        "• Integration mit EABC-Qubit-Hamiltonians<br/>"
        "• Preprint-Einreichung auf arXiv",
        body_style
    ))
    
    story.append(Paragraph("5.3 Langfristig (12 Monate)", heading2_style))
    story.append(Paragraph(
        "• Journal-Publikation (Ziel: J. Number Theory oder Discrete Math.)<br/>"
        "• Erweiterung auf weitere Faktorstrukturen<br/>"
        "• Verbindung zu algebraischer Kombinatorik",
        body_style
    ))
    
    # --- Erfolgskriterien ---
    story.append(PageBreak())
    story.append(Paragraph("6. Erfolgskriterien", heading1_style))
    
    success_data = [
        ['Szenario', 'Bedingung', 'Bewertung'],
        ['Voller Erfolg', 'H10 falsifiziert, ≥3 von H1-H9 bestätigt', 'Publikationswürdig'],
        ['Teilerfolg', 'H10 falsifiziert, 1-2 von H1-H9 bestätigt', 'Weiteres Studium'],
        ['Null-Resultat', 'H10 bestätigt (R² > 0.95)', 'Ehrlich berichten'],
        ['Negative Kontrolle', 'Keine Korrelationen signifikant', 'Konzept verwerfen'],
    ]
    
    success_table = Table(success_data, colWidths=[3*cm, 7*cm, 4*cm])
    success_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(success_table)
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "<b>Transparenz:</b> Auch ein Null-Resultat ist wissenschaftlich wertvoll "
        "und wird als negatives Kontrollergebnis publiziert.",
        body_style
    ))
    
    # --- Ressourcen ---
    story.append(Paragraph("7. Benötigte Ressourcen", heading1_style))
    
    story.append(Paragraph("7.1 Rechenkapazität", heading2_style))
    story.append(Paragraph(
        "• Graph-Konstruktion für k ≤ 12: moderate CPU (wenige Stunden)<br/>"
        "• Ensemble-Berechnung 10⁶ Zahlen: moderate CPU (Tage)<br/>"
        "• Spektralanalyse: Linear Algebra, gut parallelisierbar",
        body_style
    ))
    
    story.append(Paragraph("7.2 Software", heading2_style))
    story.append(Paragraph(
        "• Python (NumPy, SciPy, NetworkX) für Graph-Analyse<br/>"
        "• C++ für rechenintensive Primfaktorisierungen<br/>"
        "• Visualisierung: Matplotlib, optional Graphviz",
        body_style
    ))
    
    story.append(Paragraph("7.3 Zeitinvestition", heading2_style))
    story.append(Paragraph(
        "• Implementierung: ~100 Stunden<br/>"
        "• Datenanalyse: ~60 Stunden<br/>"
        "• Dokumentation/Paper: ~40 Stunden<br/>"
        "• <b>Gesamt: ~200 Stunden (ca. 6 Monate Teilzeit)</b>",
        body_style
    ))
    
    # --- Risiken ---
    story.append(PageBreak())
    story.append(Paragraph("8. Risiken und Mitigation", heading1_style))
    
    risks_data = [
        ['Risiko', 'Wahrscheinlichkeit', 'Mitigation'],
        [
            'H10 bestätigt (trivial)',
            'Mittel (40%)',
            'Bereits eingeplant, ehrlich berichten'
        ],
        [
            'Zu hohe Rechenkomplexität',
            'Niedrig (20%)',
            'Reduktion auf k ≤ 10, Sampling'
        ],
        [
            'Keine signifikanten Korrelationen',
            'Mittel (30%)',
            'Als negatives Resultat publizieren'
        ],
        [
            'Implementierungsfehler',
            'Niedrig (10%)',
            'Unit-Tests, Code-Review, Reproduzierbarkeit'
        ],
    ]
    
    risks_table = Table(risks_data, colWidths=[5*cm, 3*cm, 6*cm])
    risks_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(risks_table)
    
    # --- Nächste Schritte ---
    story.append(Paragraph("9. Unmittelbare nächste Schritte", heading1_style))
    
    next_steps_data = [
        ['Priorität', 'Aufgabe', 'Deadline'],
        ['1', 'Tamari-Graph k=2,...,6 implementieren', 'Woche 1'],
        ['2', 'Ensemble-Magic berechnen', 'Woche 1'],
        ['3', 'Kanonisierungstest an 10⁴ Zahlen', 'Woche 2'],
        ['4', 'Erste Visualisierungen', 'Woche 2'],
        ['5', 'H10 testen (Null-Modell)', 'Woche 3'],
        ['6', 'Go/No-Go Entscheidung', 'Woche 3'],
    ]
    
    next_table = Table(next_steps_data, colWidths=[2*cm, 9*cm, 3*cm])
    next_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(next_table)
    
    # --- Kontakt/Referenzen ---
    story.append(PageBreak())
    story.append(Paragraph("10. Referenzen und Kontext", heading1_style))
    
    story.append(Paragraph(
        "<b>Projektverzeichnis:</b> catalan-normalform/<br/>"
        "<b>Basis-Theorie:</b> ../README.md (EABC-Hauptprojekt)<br/>"
        "<b>Verwandtes Projekt:</b> ../eabc-qubit/ (Quanten-Hamiltonians)",
        body_style
    ))
    
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Kernliteratur:", heading2_style))
    story.append(Paragraph(
        "• Stanley, R. P. (2015). <i>Catalan Numbers</i>. Cambridge UP.<br/>"
        "• Ollivier, Y. (2009). Ricci curvature of Markov chains. <i>J. Funct. Anal.</i><br/>"
        "• Chung, F. (1997). <i>Spectral Graph Theory</i>. AMS.<br/>"
        "• Hardy & Ramanujan (1917). Normal number of prime factors.",
        body_style
    ))
    
    story.append(Spacer(1, 1*cm))
    
    # Schluss-Box
    final_box = Table(
        [['Erst wenn H10 falsifiziert ist, wird aus der Idee eine Theorie.']],
        colWidths=[14*cm]
    )
    final_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ]))
    story.append(final_box)
    
    # Build PDF
    doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
    print(f"PDF erstellt: {filename}")
    return filename

if __name__ == "__main__":
    create_start_document()
