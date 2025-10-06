from datetime import datetime
from pdf_reports import PdfReportGenerator

# Simple manual test to generate a PDF with sample data
if __name__ == "__main__":
    generator = PdfReportGenerator(output_dir="reports")
    today = datetime.now().date().isoformat()
    sample_records = [
        (1, "Alice Johnson", "Math", 88.5, f"{today}T09:15:00"),
        (2, "Bob Smith", "Science", 74.0, f"{today}T10:05:00"),
        (3, "Charlie Nguyen", "English", 92.0, f"{today}T11:20:00"),
    ]
    path = generator.generate_daily_report(date_str=today, records=sample_records)
    print(f"Generated: {path}")
