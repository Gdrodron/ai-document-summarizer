import sqlite3

DATABASE = "analysis.db"


def get_connection():
    """Return a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA journal_mode=WAL")
    return connection


def initialize_database():
    """Create the analysis table if it doesn't exist."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                summary TEXT,
                key_points TEXT,
                action_items TEXT,
                keywords TEXT,
                word_count INTEGER,
                character_count INTEGER,
                reading_time INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_analysis(
    filename,
    summary,
    key_points,
    action_items,
    keywords,
    word_count,
    character_count,
    reading_time,
):
    """Save an AI analysis to the database."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO analysis (
                filename,
                summary,
                key_points,
                action_items,
                keywords,
                word_count,
                character_count,
                reading_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                filename,
                summary,
                key_points,
                action_items,
                keywords,
                word_count,
                character_count,
                reading_time,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_all_analysis():
    """Return all saved analyses."""

    connection = get_connection()

    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM analysis
            ORDER BY created_at DESC
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def delete_analysis(record_id):
    """Delete an analysis by ID."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM analysis WHERE id = ?",
            (record_id,),
        )

        connection.commit()

    finally:
        connection.close()


def get_analysis(record_id):
    """Return a single analysis by ID."""

    connection = get_connection()

    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM analysis
            WHERE id = ?
            """,
            (record_id,),
        )

        return cursor.fetchone()

    finally:
        connection.close()