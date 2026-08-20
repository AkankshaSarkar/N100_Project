from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from xml.sax.saxutils import escape

BASE_DIR = Path(__file__).resolve().parent
MD_FILE = BASE_DIR / "analyst_guide.md"
PDF_FILE = BASE_DIR / "analyst_guide.pdf"

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    fontSize=20,
    leading=26,
    alignment=TA_CENTER,
    spaceAfter=20,
)

h1_style = ParagraphStyle(
    "H1Custom",
    parent=styles["Heading1"],
    fontSize=16,
    leading=20,
    spaceBefore=12,
    spaceAfter=8,
)

h2_style = ParagraphStyle(
    "H2Custom",
    parent=styles["Heading2"],
    fontSize=13,
    leading=17,
    spaceBefore=10,
    spaceAfter=6,
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=9.5,
    leading=14,
    spaceAfter=7,
)

bullet_style = ParagraphStyle(
    "BulletCustom",
    parent=body_style,
    leftIndent=15,
    firstLineIndent=-8,
)

doc = SimpleDocTemplate(
    str(PDF_FILE),
    pagesize=A4,
    rightMargin=18 * mm,
    leftMargin=18 * mm,
    topMargin=18 * mm,
    bottomMargin=18 * mm,
)

text = MD_FILE.read_text(encoding="utf-8")
lines = text.splitlines()

story = []

for line in lines:
    line = line.strip()

    if not line:
        story.append(Spacer(1, 5))
        continue

    # Main headings
    if line.startswith("# "):
        content = line[2:].strip()
        story.append(Paragraph(escape(content), title_style))

    # Section headings
    elif line.startswith("## "):
        content = line[3:].strip()
        story.append(Paragraph(escape(content), h1_style))

    # Sub-section headings
    elif line.startswith("### "):
        content = line[4:].strip()
        story.append(Paragraph(escape(content), h2_style))

    # Bullet points
    elif line.startswith("- ") or line.startswith("* "):
        content = line[2:].strip()
        story.append(
            Paragraph("• " + escape(content), bullet_style)
        )

    # Numbered list
    elif len(line) > 2 and line[0].isdigit() and line[1] in ".)":
        story.append(
            Paragraph(escape(line), bullet_style)
        )

    # Normal text
    else:
        story.append(
            Paragraph(escape(line), body_style)
        )

doc.build(story)

print(f"PDF created successfully: {PDF_FILE}")