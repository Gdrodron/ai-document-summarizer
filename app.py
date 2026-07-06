import os

from flask import (
    Flask,
    Response,
    redirect,
    render_template,
    request,
    send_file,
)
from werkzeug.utils import secure_filename

from utils.ai import summarize_document
from utils.database import (
    delete_analysis,
    get_all_analysis,
    get_analysis,
    initialize_database,
    save_analysis,
)
from utils.docx_reader import extract_docx
from utils.parser import parse_ai_response
from utils.pdf_reader import extract_pdf
from utils.pdf_report import generate_pdf_report
from utils.txt_reader import extract_txt


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create the SQLite database
initialize_database()


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@app.route("/")
def index():
    return render_template("index.html")


# ----------------------#
#     FILE UPLOAD       #
# ----------------------#

@app.route("/upload", methods=["POST"])
def upload():

    if "document" not in request.files:
        return "No file selected.", 400

    file = request.files["document"]

    if file.filename == "":
        return "No file selected.", 400

    if not allowed_file(file.filename):
        return (
            "Invalid file type. Please upload a PDF, DOCX, or TXT file.",
            400,
        )

    filename = secure_filename(file.filename)
    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename,
    )

    file.save(filepath)

    extension = filename.rsplit(".", 1)[1].lower()

    try:

        if extension == "pdf":
            extracted_text = extract_pdf(filepath)

        elif extension == "docx":
            extracted_text = extract_docx(filepath)

        elif extension == "txt":
            extracted_text = extract_txt(filepath)

        else:
            return "Unsupported file type.", 400

        # Generate AI Analysis
        ai_response = summarize_document(extracted_text)

        # Parse AI Response
        parsed = parse_ai_response(ai_response)

        # ----------------------
        # Document Statistics
        # ----------------------

        word_count = len(extracted_text.split())
        character_count = len(extracted_text)
        reading_time = max(1, round(word_count / 200))

        # ----------------------
        # Keywords
        # ----------------------

        keyword_list = [
            keyword.strip()
            for keyword in parsed["keywords"].split(",")
            if keyword.strip()
        ]

        # ----------------------
        # Save Analysis
        # ----------------------

        save_analysis(
            filename=filename,
            summary=parsed["summary"],
            key_points=parsed["key_points"],
            action_items=parsed["action_items"],
            keywords=", ".join(keyword_list),
            word_count=word_count,
            character_count=character_count,
            reading_time=reading_time,
        )

    except Exception as e:
        return f"Error processing document: {str(e)}", 500

    return render_template(
        "result.html",
        filename=filename,
        extracted_text=extracted_text,
        summary=parsed["summary"],
        key_points=parsed["key_points"],
        action_items=parsed["action_items"],
        keywords=keyword_list,
        word_count=word_count,
        character_count=character_count,
        reading_time=reading_time,
    )

# ----------------------#
#     HISTORY PAGE      #
# ----------------------#

@app.route("/history")
def history():
    """Display all saved document analyses."""

    analyses = get_all_analysis()

    return render_template(
        "history.html",
        analyses=analyses,
    )


# ----------------------#
#   DELETE ANALYSIS     #
# ----------------------#

@app.route("/delete/<int:record_id>")
def delete(record_id):
    """Delete an analysis record."""

    delete_analysis(record_id)

    return redirect("/history")


@app.route("/view/<int:record_id>")
def view(record_id):
    """Display a saved analysis."""

    analysis = get_analysis(record_id)

    if analysis is None:
        return "Analysis not found.", 404

    return render_template(
        "view.html",
        analysis=analysis,
    )

# ----------------------#
#   DOWNLOAD SUMMARY    #
# ----------------------#

@app.route("/download-summary", methods=["POST"])
def download_summary():

    summary = request.form.get("summary", "")

    return Response(
        summary,
        mimetype="text/plain",
        headers={
            "Content-Disposition":
                "attachment; filename=ai_summary.txt"
        },
    )


# ----------------------#
#    DOWNLOAD PDF       #
# ----------------------#

@app.route("/download-pdf", methods=["POST"])
def download_pdf():

    filename = request.form.get("filename", "document")
    summary = request.form.get("summary", "")

    pdf_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        "AI_Report.pdf",
    )

    generate_pdf_report(
        pdf_path,
        filename,
        summary,
    )

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="AI_Report.pdf",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))