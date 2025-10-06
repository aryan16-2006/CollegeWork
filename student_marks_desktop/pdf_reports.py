import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Make locally vendored dependencies importable (works without a virtualenv)
VENDOR_DIR = Path(__file__).resolve().parent / "vendor"
if VENDOR_DIR.exists():
    sys.path.insert(0, str(VENDOR_DIR))

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


class PdfReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_daily_report(self, date_str: str, records: List[Tuple[int, str, str, float, str]]) -> str:
        # File path
        filename = f"marks_report_{date_str}.pdf"
        path = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(path, pagesize=A4, title=f"Marks Report - {date_str}")
        styles = getSampleStyleSheet()
        elements = []

        title = Paragraph(f"<b>Daily Marks Report - {date_str}</b>", styles["Title"])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Table data
        data = [["ID", "Student Name", "Subject", "Marks", "Time"]]
        for rec in records:
            rec_id, name, subject, marks, created_at = rec
            time_part = created_at[11:16] if len(created_at) >= 16 else created_at
            data.append([str(rec_id), name, subject, f"{marks:.2f}", time_part])

        table = Table(data, hAlign='LEFT')
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (3, 1), (3, -1), "RIGHT"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.beige]),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ]
            )
        )
        elements.append(table)

        # Summary
        elements.append(Spacer(1, 12))
        total = sum(float(rec[3]) for rec in records) if records else 0.0
        count = len(records)
        avg = total / count if count else 0.0
        summary = Paragraph(
            f"<b>Total Records:</b> {count} &nbsp;&nbsp; <b>Average Marks:</b> {avg:.2f}",
            styles["Normal"],
        )
        elements.append(summary)

        doc.build(elements)
        return path
