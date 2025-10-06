import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from db import Database
from pdf_reports import PdfReportGenerator


class MarksApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Marks Manager")
        self.geometry("800x600")

        # Ensure directories exist
        os.makedirs("data", exist_ok=True)
        os.makedirs("reports", exist_ok=True)

        # Initialize services
        self.database = Database(db_path=os.path.join("data", "marks.db"))
        self.pdf_generator = PdfReportGenerator(output_dir="reports")

        # Build UI
        self._create_widgets()
        self._load_records_for_today()

    def _create_widgets(self):
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Form
        form = ttk.LabelFrame(container, text="Add Record")
        form.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(form, text="Student Name").grid(row=0, column=0, sticky=tk.W, padx=6, pady=6)
        self.entry_name = ttk.Entry(form)
        self.entry_name.grid(row=0, column=1, sticky=tk.EW, padx=6, pady=6)

        ttk.Label(form, text="Subject").grid(row=0, column=2, sticky=tk.W, padx=6, pady=6)
        self.entry_subject = ttk.Entry(form)
        self.entry_subject.grid(row=0, column=3, sticky=tk.EW, padx=6, pady=6)

        ttk.Label(form, text="Marks").grid(row=0, column=4, sticky=tk.W, padx=6, pady=6)
        self.entry_marks = ttk.Entry(form)
        self.entry_marks.grid(row=0, column=5, sticky=tk.EW, padx=6, pady=6)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)
        form.columnconfigure(5, weight=1)

        add_btn = ttk.Button(form, text="Add", command=self._handle_add)
        add_btn.grid(row=0, column=6, padx=6, pady=6)

        # Table
        table_frame = ttk.LabelFrame(container, text="Today's Records")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "subject", "marks", "timestamp")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Student Name")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("marks", text="Marks")
        self.tree.heading("timestamp", text="Date/Time")
        self.tree.column("id", width=60, anchor=tk.CENTER)
        self.tree.column("name", width=160)
        self.tree.column("subject", width=120)
        self.tree.column("marks", width=80, anchor=tk.E)
        self.tree.column("timestamp", width=160)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Actions
        actions = ttk.Frame(container)
        actions.pack(fill=tk.X, pady=(6, 0))

        refresh_btn = ttk.Button(actions, text="Refresh", command=self._load_records_for_today)
        refresh_btn.pack(side=tk.LEFT)

        gen_pdf_btn = ttk.Button(actions, text="Generate Today's PDF", command=self._generate_pdf)
        gen_pdf_btn.pack(side=tk.LEFT, padx=(6, 0))

        open_reports_btn = ttk.Button(actions, text="Open Reports Folder", command=lambda: self._open_path("reports"))
        open_reports_btn.pack(side=tk.RIGHT)

    def _handle_add(self):
        name = self.entry_name.get().strip()
        subject = self.entry_subject.get().strip()
        marks_text = self.entry_marks.get().strip()

        if not name or not subject or not marks_text:
            messagebox.showwarning("Validation", "Please fill all fields.")
            return
        try:
            marks = float(marks_text)
        except ValueError:
            messagebox.showwarning("Validation", "Marks must be a number.")
            return

        self.database.insert_record(name=name, subject=subject, marks=marks)
        self.entry_name.delete(0, tk.END)
        self.entry_subject.delete(0, tk.END)
        self.entry_marks.delete(0, tk.END)
        self._load_records_for_today()

    def _load_records_for_today(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        today = datetime.now().date().isoformat()
        records = self.database.get_records_by_date(today)
        for rec in records:
            self.tree.insert("", tk.END, values=(rec[0], rec[1], rec[2], rec[3], rec[4]))

    def _generate_pdf(self):
        today = datetime.now().date().isoformat()
        records = self.database.get_records_by_date(today)
        if not records:
            messagebox.showinfo("PDF", "No records for today.")
            return
        pdf_path = self.pdf_generator.generate_daily_report(date_str=today, records=records)
        messagebox.showinfo("PDF", f"Report saved to: {pdf_path}")
        self._open_path(pdf_path)

    def _open_path(self, target_path: str) -> None:
        abs_path = os.path.abspath(target_path)
        try:
            if sys.platform.startswith("win"):
                os.startfile(abs_path)  # type: ignore[attr-defined]
            elif sys.platform == "darwin":
                subprocess.run(["open", abs_path], check=False)
            else:
                subprocess.run(["xdg-open", abs_path], check=False)
        except Exception:
            # Fall back to showing the path
            messagebox.showinfo("Open", f"Saved to: {abs_path}")


if __name__ == "__main__":
    app = MarksApp()
    app.mainloop()
