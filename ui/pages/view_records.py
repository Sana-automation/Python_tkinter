
import tkinter as tk
from config import COLORS
from ui.components import make_label, make_button
from datetime import datetime
from tkinter import ttk, messagebox

class ViewRecordsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=COLORS["primary"], pady=20)
        header.pack(fill="x")
        make_label(header, "Today's Attendance Records",
                   size=16, bold=True, color="white").pack()
        self.date_label = make_label(header, "", size=11, color="#BFDBFE")
        self.date_label.pack(pady=(4, 0))
  # Toolbar
        toolbar = tk.Frame(self, bg=COLORS["bg"], pady=8)
        toolbar.pack(fill="x", padx=20)
        make_button(toolbar, "⟳ Refresh", self.on_show, width=12).pack(side="left", padx=4)
        make_button(toolbar, "Home",
                    lambda: self.controller.show_frame(HomePage),
                    color=COLORS["muted"], width=10).pack(side="right", padx=4)

   # Treeview
        tree_frame = tk.Frame(self, bg=COLORS["bg"])
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        cols = ("ID", "Emp ID", "Name", "Department", "Time", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=14)

        widths = [60, 80, 180, 150, 90, 90]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Helvetica", 11))
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))

        self.tree.tag_configure("Present", background=COLORS["present"])
        self.tree.tag_configure("Absent", background=COLORS["absent"])
        self.tree.tag_configure("Late", background=COLORS["late"])

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

  # Summary bar
        self.summary_label = make_label(self, "", size=10, color=COLORS["muted"])
        self.summary_label.pack(pady=(0, 10))

    def on_show(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.date_label.config(text=today)

        self.tree.delete(*self.tree.get_children())
        records = self.controller.db.get_today_attendance()

        present = absent = late = 0
        for rec in records:
            status = rec.get("status", "")
            if status == "Present": present += 1
            elif status == "Absent": absent += 1
            elif status == "Late": late += 1

        self.tree.insert("", "end", values=(
            rec.get("record_id", ""),
            rec.get("emp_id", ""),
            rec.get("name", ""),
            rec.get("department", ""),
            rec.get("time", ""),
            status,
            ), tags=(status,))


        total = len(records)
        self.summary_label.config(
            text=f"Total: {total}| Present: {present} "
                 f"Absent: {absent}Late: {late}")
