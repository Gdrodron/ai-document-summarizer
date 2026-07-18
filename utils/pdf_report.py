from xml.sax.saxutils import escape

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph


def generate_pdf_report(filepath, filename, summary):

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("<b>AI DOCUMENT REPORT</b>", styles["Title"]))
    elements.append(Paragraph(f"<b>Filename:</b> {escape(filename)}", styles["BodyText"]))
    elements.append(Paragraph("<br/>", styles["BodyText"]))

    elements.append(Paragraph("<b>AI Analysis</b>", styles["Heading2"]))
    # IMPORTANT: escape special XML/HTML characters (&, <, >) in the AI-generated
    # summary BEFORE inserting <br/> tags, otherwise reportlab's Paragraph parser
    # throws a "not well-formed" error and the route returns 500. This was
    # happening whenever the summary contained characters like &, <, or >.
    safe_summary = escape(summary).replace("\n", "<br/>")
    elements.append(Paragraph(safe_summary, styles["BodyText"]))

    doc.build(elements)