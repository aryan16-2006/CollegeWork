import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import date
from data_store import init_db, add_mark, list_marks, delete_mark, MarkEntry
from pdf_report import generate_daily_pdf


class MarksApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Marks Manager (PC MVP)")
        self.geometry("800x500")
        self.resizable(True, True)

        init_db()

        self._build_ui()
        self._load_today()

    def _build_ui(self):
        # Top frame: form inputs
        form = ttk.LabelFrame(self, text="Add Entry")
        form.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_var = tk.StringVar(value=date.today().isoformat())
        self.date_entry = ttk.Entry(form, textvariable=self.date_var, width=16)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Student Name").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form, textvariable=self.name_var, width=24)
        self.name_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Subject").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.subject_var = tk.StringVar()
        self.subject_entry = ttk.Entry(form, textvariable=self.subject_var, width=18)
        self.subject_entry.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(form, text="Marks").grid(row=0, column=6, padx=5, pady=5, sticky=tk.W)
        self.marks_var = tk.StringVar()
        self.marks_entry = ttk.Entry(form, textvariable=self.marks_var, width=10)
        self.marks_entry.grid(row=0, column=7, padx=5, pady=5)

        add_btn = ttk.Button(form, text="Add", command=self._on_add)
        add_btn.grid(row=0, column=8, padx=5, pady=5)

        # Filters and actions
        actions = ttk.Frame(self)
        actions.pack(fill=tk.X, padx=10)

        ttk.Label(actions, text="Filter by Date").pack(side=tk.LEFT, padx=(0, 6))
        self.filter_date_var = tk.StringVar(value=date.today().isoformat())
        ttk.Entry(actions, textvariable=self.filter_date_var, width=16).pack(side=tk.LEFT)

        ttk.Button(actions, text="Apply Filter", command=self._apply_filter).pack(side=tk.LEFT, padx=6)
        ttk.Button(actions, text="Show All", command=self._show_all).pack(side=tk.LEFT)

        self.pdf_btn = ttk.Button(actions, text="Generate PDF (today)", command=self._on_pdf)
        self.pdf_btn.pack(side=tk.RIGHT)

        # Table
        columns = ("id", "date", "student", "subject", "marks")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col, text, width in [
            ("id", "ID", 60),
            ("date", "Date", 100),
            ("student", "Student", 220),
            ("subject", "Subject", 160),
            ("marks", "Marks", 80),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=tk.W if col != "marks" else tk.E)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bottom actions
        bottom = ttk.Frame(self)
        bottom.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Button(bottom, text="Delete Selected", command=self._on_delete).pack(side=tk.LEFT)

    def _on_add(self):
        try:
            date_iso = self.date_var.get().strip()
            student_name = self.name_var.get().strip()
            subject = self.subject_var.get().strip()
            marks_str = self.marks_var.get().strip()

            if not (date_iso and student_name and subject and marks_str):
                messagebox.showwarning("Validation", "All fields are required.")
                return

            marks_val = float(marks_str)
            entry = MarkEntry(id=None, date_iso=date_iso, student_name=student_name, subject=subject, marks=marks_val)
            add_mark(entry)

            self._refresh_table(self._current_filter)
            # clear name/subject/marks for fast entry
            self.name_var.set("")
            self.subject_var.set("")
            self.marks_var.set("")
            self.name_entry.focus_set()
        except ValueError:
            messagebox.showerror("Invalid Input", "Marks must be a number.")

    def _on_delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item_id = selected[0]
        mark_id = int(self.tree.item(item_id, 'values')[0])
        if messagebox.askyesno("Confirm Delete", f"Delete record ID {mark_id}?"):
            delete_mark(mark_id)
            self._refresh_table(self._current_filter)

    def _apply_filter(self):
        filt = self.filter_date_var.get().strip()
        self._refresh_table(filt if filt else None)

    def _show_all(self):
        self._refresh_table(None)

    def _on_pdf(self):
        try:
            date_iso = date.today().isoformat()
            pdf_path = generate_daily_pdf(date_iso)
            messagebox.showinfo("PDF Generated", f"Saved to:\n{pdf_path}")
            # Try to open folder cross-platform
            folder = os.path.dirname(pdf_path)
            try:
                if hasattr(os, 'startfile'):
                    os.startfile(folder)  # type: ignore[attr-defined]
                else:
                    import subprocess, sys
                    if sys.platform.startswith('darwin'):
                        subprocess.Popen(['open', folder])
                    else:
                        subprocess.Popen(['xdg-open', folder])
            except Exception:
                pass
        except Exception as ex:
            messagebox.showerror("PDF Error", str(ex))

    def _load_today(self):
        self._current_filter = date.today().isoformat()
        self._refresh_table(self._current_filter)

    def _refresh_table(self, date_filter):
        self._current_filter = date_filter
        for item in self.tree.get_children():
            self.tree.delete(item)
        entries = list_marks(date_filter)
        for e in entries:
            self.tree.insert('', tk.END, values=(e.id, e.date_iso, e.student_name, e.subject, f"{e.marks:g}"))


if __name__ == "__main__":
    app = MarksApp()
    app.mainloop()
