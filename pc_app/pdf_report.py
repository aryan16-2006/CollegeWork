from typing import Optional
import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from data_store import list_marks


def _ensure_reports_dir(base_dir: Optional[str] = None) -> str:
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


def generate_daily_pdf(date_iso: Optional[str] = None, base_dir: Optional[str] = None) -> str:
    """Generate a daily marks PDF and return its file path."""
    if not date_iso:
        date_iso = date.today().isoformat()

    reports_dir = _ensure_reports_dir(base_dir)
    output_path = os.path.join(reports_dir, f"marks_{date_iso}.pdf")

    entries = list_marks(date_iso=date_iso, base_dir=base_dir)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(f"Daily Marks Report - {date_iso}", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 12))

    if not entries:
        story.append(Paragraph("No entries found for this date.", styles["BodyText"]))
        doc.build(story)
        return output_path

    data = [["ID", "Student", "Subject", "Marks"]]
    for e in entries:
        data.append([str(e.id), e.student_name, e.subject, f"{e.marks:g}"])

    table = Table(data, hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.beige]),
            ]
        )
    )

    story.append(table)

    doc.build(story)
    return output_path
