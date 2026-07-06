from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def generate_pdf_report(filepath, filename, summary):

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>AI DOCUMENT REPORT</b>", styles["Title"]))
    elements.append(Paragraph(f"<b>Filename:</b> {filename}", styles["BodyText"]))
    elements.append(Paragraph("<br/>", styles["BodyText"]))

    elements.append(Paragraph("<b>AI Analysis</b>", styles["Heading2"]))
    elements.append(Paragraph(summary.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(elements)