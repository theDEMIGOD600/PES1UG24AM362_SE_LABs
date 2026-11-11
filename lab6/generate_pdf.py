import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    shots_dir = os.path.join(base_dir, "screenshots")
    pdf_path = os.path.join(base_dir, "Lab_6_Submission.pdf")

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=10,
        spaceAfter=6
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Heading3'],
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#1A202C'),
        backColor=colors.HexColor('#EDF2F7'),
        borderColor=colors.HexColor('#CBD5E0'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
        borderRadius=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#2D3748')
    )

    story = []

    # Title Banner
    story.append(Paragraph("Lab 6: Code and Branch Coverage Analysis", title_style))
    story.append(Paragraph("<b>Scenario:</b> Income Tax Calculator (<code>income_tax.py</code>) &nbsp;|&nbsp; <b>Course:</b> Software Engineering", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=10))

    # Section 1: Overview
    story.append(Paragraph("1. Executive Summary & Coverage Concepts", h2_style))
    story.append(Paragraph(
        "<b>Line Coverage</b> measures whether each statement in the module was executed at least once during test execution. "
        "<b>Branch Coverage</b> is a stricter metric that evaluates whether every control flow decision point "
        "(e.g., <code>if</code>, <code>elif</code>, <code>else</code>) evaluates to both <i>True</i> and <i>False</i> across all runs. "
        "High line coverage can mask untested execution paths; branch coverage guarantees thorough decision path testing.",
        body_style
    ))

    # Metric Table
    metrics_data = [
        ["Metric", "Initial Starter Test", "Target", "Achieved Result"],
        ["Line (Code) Coverage", "38% (24 missing statements)", ">= 90%", "100% (39/39 statements)"],
        ["Branch Coverage", "33% (7 missing partial branches)", ">= 90%", "100% (28/28 branches)"],
        ["Test Suite Size", "2 test cases", "Comprehensive", "27 test cases (All Passing)"]
    ]
    t_rows = [[Paragraph(c, table_header_style) for c in metrics_data[0]]]
    for row in metrics_data[1:]:
        t_rows.append([Paragraph(c, table_cell_style) for c in row])

    metric_table = Table(t_rows, colWidths=[130, 130, 100, 180])
    metric_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2B6CB0')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')]),
    ]))
    story.append(metric_table)
    story.append(Spacer(1, 8))

    # Section 2: Decision Branches Analyzed
    story.append(Paragraph("2. Decision Branch Breakdown in <code>income_tax.py</code>", h2_style))
    branch_data = [
        ["Function", "Decision Point", "Branch Conditions Tested", "Resolution / Boundary"],
        ["taxable_income", "gross < 0", "True -> ValueError('invalid income'); False -> proceeds", "gross = -1 and gross = 0"],
        ["taxable_income", "regime check", "'new' -> 75k ded; 'old' -> 50k+inv; else -> ValueError", "Tested 'new', 'old', 'flat_tax'"],
        ["taxable_income", "investments cap", "investments > 150k -> capped; <= 150k -> kept", "Tested 250k, 150k, 80k"],
        ["taxable_income", "taxable < 0", "True -> returns 0; False -> returns taxable", "gross < deduction vs gross > deduction"],
        ["tax_due", "taxable < 0", "True -> ValueError('invalid amount'); False -> proceeds", "taxable = -1"],
        ["tax_due", "age categories", "age >= 80 (500k exempt); age >= 60 (300k); else (250k)", "Boundary ages: 85, 80, 70, 60, 59, 25"],
        ["tax_due", "taxable <= exempt", "True -> returns 0; False -> calculates slab tax", "taxable < exempt, taxable == exempt"],
        ["tax_due", "slab <= 250k", "True -> slab * 5%; False -> 12500 + excess * 20%", "slab = 200k, slab = 250k, slab = 500k"],
        ["refund_status", "difference > 0", "True: on_time -> 'refund'; late -> 'refund delayed'", "tax_paid > tax_due with True/False"],
        ["refund_status", "difference < 0", "True: on_time -> 'pay balance'; late -> '...penalty'", "tax_paid < tax_due with True/False"],
        ["refund_status", "difference == 0", "Neither > 0 nor < 0 -> returns 'settled'", "tax_paid == tax_due with True/False"]
    ]
    t_rows2 = [[Paragraph(c, table_header_style) for c in branch_data[0]]]
    for row in branch_data[1:]:
        t_rows2.append([Paragraph(c, table_cell_style) for c in row])

    branch_table = Table(t_rows2, colWidths=[90, 100, 210, 140])
    branch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2B6CB0')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')]),
    ]))
    story.append(branch_table)

    # Page Break for Screenshots
    story.append(PageBreak())
    story.append(Paragraph("3. Terminal Execution & Coverage Screenshots", h2_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2B6CB0'), spaceAfter=8))

    # Screenshot 1: Code Coverage
    cc_img = os.path.join(shots_dir, "code_coverage_terminal_report.png")
    if os.path.exists(cc_img):
        story.append(Paragraph("<b>Artifact 1: Code (Line) Coverage Analysis — 100% Achieved</b>", h3_style))
        story.append(Image(cc_img, width=7.0*inch, height=4.1*inch))
        story.append(Spacer(1, 10))

    # Screenshot 2: Branch Coverage
    bc_img = os.path.join(shots_dir, "branch_coverage_terminal_report.png")
    if os.path.exists(bc_img):
        story.append(Paragraph("<b>Artifact 2: Branch Coverage Analysis — 100% Achieved (28/28 Branches)</b>", h3_style))
        story.append(Image(bc_img, width=7.0*inch, height=4.1*inch))
        story.append(Spacer(1, 10))

    doc.build(story)
    print(f"Generated PDF at: {pdf_path}")

if __name__ == '__main__':
    build_pdf()
