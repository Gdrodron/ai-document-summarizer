"""
routes/__init__.py

Single source of truth for the shared Flask Blueprint.
Every route module (main, download, history, errors) imports main_bp
from here and attaches its routes with @main_bp.route(...).

Do NOT create another Blueprint("main", ...) anywhere else in this
package -- Flask will raise a "blueprint name already registered" /
duplicate endpoint error if you do.
"""

from flask import Blueprint

main_bp = Blueprint("main", __name__)

# Import route modules AFTER creating the blueprint, so their
# @main_bp.route(...) decorators register against this single instance.
from . import main      # noqa: F401  (index)
from . import upload    # noqa: F401  (file upload + AI analysis)
from . import download  # noqa: F401  (all download endpoints)
from . import history   # noqa: F401  (history list / view / delete)
from . import errors    # noqa: F401  (404 / 500 handlers)