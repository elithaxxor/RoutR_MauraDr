import logging
import sqlite3
from datetime import datetime

class SQLiteHandler(logging.Handler):
    """Custom logging handler to store logs in SQLite."""
    def __init__(self, db):
        super().__init__()
        self.db = db
        self._initialize_database()

    def _initialize_database(self):
        """Create logs and schedules tables if they don't exist."""
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
            c.execute('''
                CREATE TABLE IF NOT EXISTS scan_schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    network_cidr TEXT NOT NULL,
                    intensity TEXT NOT NULL,
                    frequency TEXT NOT NULL,
                    time TEXT,  -- HH:MM for daily/weekly
                    created_at TEXT,
                    created_by TEXT,
                    UNIQUE(network_cidr)
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
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(console_handler)

    sqlite_handler = SQLiteHandler(db_path)
    sqlite_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(sqlite_handler)

    return logger
