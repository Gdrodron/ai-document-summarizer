"""
routes/upload.py

Handles document upload + AI analysis:
1. Validate and save the uploaded file
2. Extract text, run it through Gemini, parse the response
3. Compute stats (word count, char count, reading time)
4. Persist the analysis to history
5. Render the result page
"""

import os
import uuid

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from werkzeug.utils import secure_filename

from utils.ai import summarize_document
from utils.database import save_analysis
from utils.file_handler import allowed_file, extract_text
from utils.helpers import document_statistics, parse_keywords
from utils.parser import parse_ai_response

from . import main_bp


@main_bp.route("/upload", methods=["POST"])
def upload_document():

    if "document" not in request.files:
        flash("Please select a file.", "danger")
        return redirect(url_for("main.index"))

    file = request.files["document"]

    if file.filename == "":
        flash("No file selected.", "danger")
        return redirect(url_for("main.index"))

    if not allowed_file(file.filename, current_app.config["ALLOWED_EXTENSIONS"]):
        flash("Unsupported file type.", "danger")
        return redirect(url_for("main.index"))

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_filename)

    try:
        file.save(filepath)
        extension = filename.rsplit(".", 1)[1].lower()

        extracted_text = extract_text(filepath, extension)
        ai_response = summarize_document(extracted_text)
        parsed = parse_ai_response(ai_response)
        stats = document_statistics(extracted_text)
        keyword_list = parse_keywords(parsed.get("keywords", ""))

        save_analysis(
            filename=filename,
            summary=parsed["summary"],
            key_points=parsed["key_points"],
            action_items=parsed["action_items"],
            keywords=", ".join(keyword_list),
            word_count=stats["word_count"],
            character_count=stats["character_count"],
            reading_time=stats["reading_time"],
        )

        return render_template(
            "result.html",
            filename=filename,
            summary=parsed["summary"],
            key_points=parsed["key_points"],
            action_items=parsed["action_items"],
            keywords=keyword_list,
            word_count=stats["word_count"],
            character_count=stats["character_count"],
            reading_time=stats["reading_time"],
            extracted_text=extracted_text,
        )

    except Exception as error:
        current_app.logger.exception(error)
        flash("Failed to analyze document.", "danger")
        return redirect(url_for("main.index"))

    finally:
        # Always try to clean up the uploaded file, success or failure.
        # Wrapped in its own try/except: on Windows, a library that opened
        # this file (e.g. PyPDF2/python-docx) can still hold a lock on it
        # for a moment after returning. If os.remove() raised here
        # unguarded, it would silently replace a successful
        # render_template(...) response above with a 500 error -- a
        # raised exception inside `finally` overrides whatever `try`
        # already returned. Losing the temp file for a beat is harmless;
        # losing the user's result page is not.
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except OSError as cleanup_error:
            current_app.logger.warning(
                f"Could not delete temp upload {filepath}: {cleanup_error}"
            )