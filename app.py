import os
import logging

from dotenv import load_dotenv

# Load variables from .env into the environment BEFORE anything else
# reads os.environ (Config, API keys, DEBUG flag, etc.). Without this,
# your .env file is silently ignored.
load_dotenv()

from flask import Flask

from config import Config

from routes.main import main_bp
from routes.errors import errors_bp

from utils.database import initialize_database


# =========================
# LOGGING
# =========================

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# =========================
# APPLICATION FACTORY
# =========================

def create_app():

    app = Flask(__name__)

    # -------------------------
    # Configuration
    # -------------------------

    app.config.from_object(Config)

    # -------------------------
    # Upload folder
    # -------------------------

    upload_folder = app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    # -------------------------
    # Database
    # -------------------------
    # Fail fast: if the database can't initialize, the app can't
    # actually do anything (every route depends on it), so don't
    # let it start in a broken state.

    try:
        initialize_database()
        app.logger.info("Database initialized successfully.")

    except Exception as error:
        app.logger.critical(f"Database initialization failed: {error}")
        raise

    # -------------------------
    # Blueprints
    # -------------------------

    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    return app


# =========================
# GUNICORN ENTRY POINT
# =========================

app = create_app()


# =========================
# LOCAL DEVELOPMENT
# =========================

if __name__ == "__main__":

    debug_mode = os.environ.get("DEBUG", "False").lower() == "true"

    if debug_mode:
        # Werkzeug's debugger allows arbitrary code execution. Binding
        # to 0.0.0.0 with debug on is safe only on a trusted local
        # network (e.g. Docker on your own machine) - never do this
        # on a publicly reachable host.
        logger.warning(
            "Running with debug=True and host=0.0.0.0. "
            "Do not expose this port to the public internet."
        )

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=debug_mode,
    )

    # Test deploy