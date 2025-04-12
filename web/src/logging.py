import logging
import sqlite3
from datetime import datetime

"""
This module configures logging with both console and SQLite handlers, using different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
"""

class SQLiteHandler(logging.Handler):
    """Custom logging handler to store logs in SQLite."""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._initialize_database()

    def _initialize_database(self):
        """Create logs table if it doesn't exist."""
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    level TEXT,
                    message TEXT
                )
            ''')
            conn.commit()

    def emit(self, record):
        """Write log record to SQLite."""
        try:
            with sqlite3.connect(self.db) as conn:
                c = conn.cursor()
                timestamp = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
                level = record.levelname
                message = self.format(record)
                c.execute(
                    "INSERT INTO logs (timestamp, level, message) VALUES (?, ?, ?)",
                    (timestamp, level, message)
                )
                conn.commit()
        except Exception as e:
            print(f"[DB LOG FAILURE] {e}")

def setup_logger(db_path):
    """Configure and return a logger with console and SQLite handlers."""
    logger = logging.getLogger("SMBLogger")
    logger.setLevel(logging.DEBUG)  # Capture all log levels

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(console_handler)

    # SQLite handler
    sqlite_handler = SQLiteHandler(db_path)
    sqlite_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(sqlite_handler)

    return logger
