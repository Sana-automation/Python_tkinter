import tkinter as tk
from config import COLORS
from ui.components import make_label, make_button, make_entry, make_card

class EmployeeCheckPage(tk.Frame):
    """
    Flowchart step: Enter Employee ID → Check if ID Exists
    If No → Show Error message (stay on page)
    If Yes → Proceed to Mark Attendance
    """
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller
        self.emp_id_var = tk.StringVar()
        self.error_var = tk.StringVar()
        self._build()

    def _build(self):
        # Header
        header = tk.Frame(self, bg=COLORS["primary"], pady=20)
        header.pack(fill="x")
        make_label(header, "Enter Employee ID", size=16, bold=True, color="white").pack()

        # Card
        card = make_card(self, padx=50, pady=40)
        card.pack(expand=True)

        make_label(card, "Employee ID", size=11, color=COLORS["muted"]).pack(anchor="w")

        entry_frame = tk.Frame(card, bg=COLORS["card"])
        entry_frame.pack(fill="x", pady=(4, 0))

        self.id_entry = make_entry(entry_frame, textvariable=self.emp_id_var, width=28)
        self.id_entry.pack(side="left")
        self.id_entry.bind("<Return>", lambda e: self._check_id())

        make_label(card, "(e.g. E001, E002 … E005)",
                   size=9, color=COLORS["muted"]).pack(anchor="w", pady=(4, 0))

        # Error label (hidden until needed)
        self.error_label = make_label(card, "", size=10, color=COLORS["danger"])
        self.error_label.pack(pady=(8, 0))

        # Buttons
        btn_row = tk.Frame(card, bg=COLORS["card"])
        btn_row.pack(pady=(20, 0))

        make_button(btn_row, "Check ID →", self._check_id).grid(row=0, column=0, padx=6)
        make_button(btn_row, "← Back", lambda: self.controller.show_frame(HomePage),
                    color=COLORS["muted"]).grid(row=0, column=1, padx=6)

        # Quick employee list hint
        hint = make_card(card, padx=20, pady=12)
        hint.pack(pady=(24, 0), fill="x")
        make_label(hint, "Sample Employee IDs:  E001 · E002 · E003 · E004 · E005",
                   size=10, color=COLORS["muted"]).pack()

    def on_show(self):
        self.emp_id_var.set("")
        self.error_var.set("")
        self.error_label.config(text="")
        self.id_entry.focus()

    def _check_id(self):
        """Flowchart decision: does ID exist?"""
        emp_id = self.emp_id_var.get().strip()
        if not emp_id:
            self.error_label.config(text="￼  Please enter an Employee ID.")
            return

        try:
            employee = self.controller.db.get_employee(emp_id)
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e))
            return

        # ── Flowchart: ID NOT found → show error ──
        if employee is None:
            self.error_label.config(
                text=f"✗  Employee ID '{emp_id}' not found. Please try again.")
            self.id_entry.focus()
            return

        # ── Flowchart: ID found → check duplicate ──
        existing = self.controller.db.has_attendance_today(emp_id)
        if existing:
            result = messagebox.askyesno(
                "Already Marked",
                f"{employee['name']} already has attendance marked as "
                f"'{existing}' today.\n\nDo you want to continue to update it?")
            if not result:
                return

        # ── Pass employee to next page ──
        self.controller.current_employee = employee
        self.controller.show_frame(MarkAttendancePage)

