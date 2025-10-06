import os
import sqlite3
from datetime import datetime
from typing import List, Tuple


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self) -> None:
        with self._get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS marks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    marks REAL NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_marks_date ON marks(substr(created_at, 1, 10))
                """
            )

    def insert_record(self, name: str, subject: str, marks: float) -> int:
        timestamp = datetime.now().isoformat(timespec="seconds")
        with self._get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO marks(student_name, subject, marks, created_at) VALUES (?, ?, ?, ?)",
                (name, subject, marks, timestamp),
            )
            return cur.lastrowid

    def get_records_by_date(self, date_str: str) -> List[Tuple[int, str, str, float, str]]:
        # date_str format: YYYY-MM-DD
        with self._get_conn() as conn:
            rows = conn.execute(
                """
                SELECT id, student_name, subject, marks, created_at
                FROM marks
                WHERE substr(created_at, 1, 10) = ?
                ORDER BY created_at ASC
                """,
                (date_str,),
            ).fetchall()
        return rows

    def get_all_dates(self) -> List[str]:
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT DISTINCT substr(created_at, 1, 10) AS date FROM marks ORDER BY date DESC"
            ).fetchall()
        return [r[0] for r in rows]
