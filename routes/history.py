from flask import abort, flash, redirect, render_template, url_for

from utils.database import delete_analysis, get_all_analysis, get_analysis

from . import main_bp


# ======================
# HISTORY LIST
# ======================

@main_bp.route("/history")
def view_history():
    return render_template("history.html", analyses=get_all_analysis())


# ======================
# VIEW ONE RECORD
# ======================

@main_bp.route("/view/<int:record_id>")
def view_analysis(record_id):
    analysis = get_analysis(record_id)

    if analysis is None:
        abort(404)

    return render_template("view.html", analysis=analysis)


# ======================
# DELETE ONE RECORD
# ======================

@main_bp.route("/delete/<int:record_id>", methods=["POST"])
def delete_analysis_record(record_id):
    analysis = get_analysis(record_id)

    if analysis is None:
        flash("Analysis not found.", "warning")
        return redirect(url_for("main.view_history"))

    delete_analysis(record_id)
    flash("Deleted successfully.", "success")

    return redirect(url_for("main.view_history"))