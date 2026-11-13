import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def build_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    shots_dir = os.path.join(base_dir, "screenshots")
    pdf_path = os.path.join(base_dir, "PES1UG24AM362_Dhruvanth_LAB7.pdf")
    pdf_alt = os.path.join(base_dir, "Lab_7_Submission.pdf")

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
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=5
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1A202C'),
        backColor=colors.HexColor('#EDF2F7'),
        borderColor=colors.HexColor('#CBD5E0'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=3,
        spaceAfter=6,
        borderRadius=4
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor('#2D3748')
    )

    story = []

    # Title Banner
    story.append(Paragraph("Lab 7: Fuzzing for Input Validation Bugs", title_style))
    story.append(Paragraph("<b>Student:</b> Dhruvanth &nbsp;|&nbsp; <b>SRN:</b> PES1UG24AM362 &nbsp;|&nbsp; <b>Scenario:</b> Income Tax Parser (<code>income_tax_parser.py</code>)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=8))

    # Section 1: Overview
    story.append(Paragraph("1. Executive Summary & Fuzz Testing Methodology", h2_style))
    story.append(Paragraph(
        "Fuzz testing (fuzzing) is a dynamic software testing technique where automated property-based testing tools "
        "inject random, malformed, unexpected, or boundary inputs into software to discover crashes, unhandled exceptions, and security vulnerabilities. "
        "In this lab, the <b>Hypothesis</b> library was utilized to test the input validation boundaries of the Income Tax Parser module.",
        body_style
    ))

    # Bug Breakdown Table
    story.append(Paragraph("2. Bugs Discovered via Hypothesis Fuzzing & Defensive Fixes", h2_style))
    bug_data = [
        ["Function", "Failing Input (Fuzzer)", "Unhandled Exception", "Root Cause", "Defensive Fix Implemented"],
        [
            "clean_pan(pan)",
            "None, empty, non-string",
            "AttributeError",
            "Assumed input is non-empty string; calling .strip() on None crashes.",
            "Added explicit type & None check (isinstance(pan, str)); returns safe empty string if invalid."
        ],
        [
            "parse_amount(text)",
            "None, '', 'Rs ', 'abc'",
            "ValueError / AttributeError",
            "Calling int() on empty string after removing currency symbols or on None.",
            "Added None check, string validation, regex fallback for digits, and returns 0 on parse failure."
        ],
        [
            "parse_tax_slab(line)",
            "None, ':', '', 'abc'",
            "ValueError / AttributeError",
            "Unpacking limits, rate with .split(':') and low, high with .split('-') without validating parts count.",
            "Validates presence of delimiters (':' and '-'), checks split lengths, and wraps int conversion safely."
        ]
    ]

    t_rows = [[Paragraph(c, table_header_style) for c in bug_data[0]]]
    for row in bug_data[1:]:
        t_rows.append([Paragraph(c, table_cell_style) for c in row])

    bug_table = Table(t_rows, colWidths=[90, 85, 100, 130, 135])
    bug_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2B6CB0')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')]),
    ]))
    story.append(bug_table)
    story.append(Spacer(1, 8))

    # Section 3: Reflection Questions
    story.append(Paragraph("3. Answers to Reflection Questions", h2_style))

    story.append(Paragraph("<b>Q1: What types of unexpected inputs or edge cases did Hypothesis generate that manual testing typically misses?</b>", body_style))
    story.append(Paragraph(
        "<b>Answer:</b> Hypothesis systematically generated minimal shrinking counterexamples that human testers typically overlook, including: "
        "(1) <code>NoneType</code> values representing uninitialized or null variables, "
        "(2) Empty strings (<code>''</code>) that produce empty tokens after delimiter stripping, "
        "(3) Single delimiter characters like <code>':'</code> or <code>'-'</code> that break naive tuple unpacking, and "
        "(4) Non-ASCII / Unicode text strings that bypass standard ASCII sanitization routines. Manual unit testing usually assumes well-formed formats.",
        callout_style
    ))

    story.append(Paragraph("<b>Q2: How does property-based fuzzing differ from traditional unit testing in uncovering input validation bugs?</b>", body_style))
    story.append(Paragraph(
        "<b>Answer:</b> Traditional unit testing relies on example-based assertions where developers test specific, anticipated inputs (e.g., 'Rs 12,50,000'). "
        "In contrast, property-based fuzzing defines general system invariants (properties) — such as <i>'this parser function must never raise an unhandled crash or exception regardless of input'</i> — "
        "and automatically generates hundreds of randomized variations across the entire input domain. Furthermore, Hypothesis utilizes <b>shrinking</b> to automatically reduce failing inputs to the smallest, simplest reproducible bug.",
        callout_style
    ))

    story.append(Paragraph("<b>Q3: How did the defensive programming fixes improve the overall robustness and security of the module?</b>", body_style))
    story.append(Paragraph(
        "<b>Answer:</b> Applying defensive programming (type verification with <code>isinstance</code>, delimiter length pre-validation, safe exception boundaries, and fallback defaults) prevents Denial of Service (DoS) attacks caused by uncaught exceptions crashing server processes. It ensures the application fails gracefully, maintains system availability, and avoids exposing internal implementation stack traces to users.",
        callout_style
    ))

    # Page Break for Screenshots SS1 and SS2
    story.append(PageBreak())
    story.append(Paragraph("4. Fuzz Testing Execution Screenshots", h2_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#2B6CB0'), spaceAfter=8))

    ss1_img = os.path.join(shots_dir, "SS1_buggy_run.png")
    if os.path.exists(ss1_img):
        story.append(Paragraph("<b>Screenshot 1 (SS1): <code>python income_tax_parser.py</code> run on the buggy module</b>", h3_style))
        story.append(Image(ss1_img, width=7.0*inch, height=3.6*inch))
        story.append(Spacer(1, 10))

    ss2_img = os.path.join(shots_dir, "SS2_buggy_tests_failing.png")
    if os.path.exists(ss2_img):
        story.append(Paragraph("<b>Screenshot 2 (SS2): <code>pytest test_income_tax_parser.py</code> with Hypothesis tests failing on buggy module</b>", h3_style))
        story.append(Image(ss2_img, width=7.0*inch, height=4.2*inch))

    # Page Break for Screenshots SS3 and SS4
    story.append(PageBreak())
    ss3_img = os.path.join(shots_dir, "SS3_fixed_run.png")
    if os.path.exists(ss3_img):
        story.append(Paragraph("<b>Screenshot 3 (SS3): <code>python income_tax_parser.py</code> run on the fixed & hardened module</b>", h3_style))
        story.append(Image(ss3_img, width=7.0*inch, height=3.6*inch))
        story.append(Spacer(1, 10))

    ss4_img = os.path.join(shots_dir, "SS4_fixed_tests_passing.png")
    if os.path.exists(ss4_img):
        story.append(Paragraph("<b>Screenshot 4 (SS4): <code>pytest test_income_tax_parser.py</code> with all Hypothesis fuzz tests passing</b>", h3_style))
        story.append(Image(ss4_img, width=7.0*inch, height=3.4*inch))

    doc.build(story)
    
    # Save a copy as Lab_7_Submission.pdf
    import shutil
    shutil.copyfile(pdf_path, pdf_alt)
    print(f"Generated PDF at: {pdf_path} and {pdf_alt}")

if __name__ == '__main__':
    build_pdf()
