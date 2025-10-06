import sqlite3
from dataclasses import dataclass
from typing import List, Optional, Tuple
import os

DB_NAME = "marks.db"


@dataclass
class MarkEntry:
    id: Optional[int]
    date_iso: str
    student_name: str
    subject: str
    marks: float


def get_db_path(base_dir: Optional[str] = None) -> str:
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DB_NAME)


def init_db(base_dir: Optional[str] = None) -> None:
    db_path = get_db_path(base_dir)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_iso TEXT NOT NULL,
                student_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                marks REAL NOT NULL
            )
            """
        )
        conn.commit()


def add_mark(entry: MarkEntry, base_dir: Optional[str] = None) -> int:
    db_path = get_db_path(base_dir)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO marks (date_iso, student_name, subject, marks) VALUES (?, ?, ?, ?)",
            (entry.date_iso, entry.student_name, entry.subject, entry.marks),
        )
        conn.commit()
        return cur.lastrowid


def list_marks(date_iso: Optional[str] = None, base_dir: Optional[str] = None) -> List[MarkEntry]:
    db_path = get_db_path(base_dir)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        if date_iso:
            cur.execute(
                "SELECT id, date_iso, student_name, subject, marks FROM marks WHERE date_iso=? ORDER BY id DESC",
                (date_iso,),
            )
        else:
            cur.execute(
                "SELECT id, date_iso, student_name, subject, marks FROM marks ORDER BY id DESC"
            )
        rows = cur.fetchall()
    return [
        MarkEntry(id=row[0], date_iso=row[1], student_name=row[2], subject=row[3], marks=float(row[4]))
        for row in rows
    ]


def delete_mark(mark_id: int, base_dir: Optional[str] = None) -> None:
    db_path = get_db_path(base_dir)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM marks WHERE id=?", (mark_id,))
        conn.commit()


def clear_all(base_dir: Optional[str] = None) -> None:
    db_path = get_db_path(base_dir)
    with sqlite3.connect(db_path) as conn:
        conn.execute("DELETE FROM marks")
        conn.commit()
