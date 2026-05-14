import tkinter as tk
from config import COLORS
from ui.components import make_label, make_button, make_card
from config import ATTENDANCE_FILE

class ConfirmationPage(tk.Frame):
    """Flowchart step: Display Confirmation → End"""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLORS["bg"])
        self.controller = controller
        self._build()

    def _build(self):
        header = tk.Frame(self, bg=COLORS["success"], pady=20)
        header.pack(fill="x")
        make_label(header, "Attendance Saved!", size=16, bold=True, color="white").pack()

        card = make_card(self, padx=50, pady=40)
        card.pack(expand=True)

        make_label(card, "Attendance recorded successfully.",
                   size=13, color=COLORS["success"], bold=True).pack()

        # Summary box
        summary = make_card(card, padx=24, pady=20)
        summary.pack(fill="x", pady=(20, 0))

        fields = [
            ("Record ID", "record_id"),
            ("Employee ID", "emp_id"),
            ("Name", "emp_name"),
            ("Department", "emp_dept"),
            ("Date", "date"),
            ("Time", "time"),
            ("Status", "status"),
            ]
        for row_i, (label, key) in enumerate(fields):
            make_label(summary, f"{label}:", size=11,
                       color=COLORS["muted"]).grid(row=row_i, column=0, sticky="w", pady=3)
            val_lbl = make_label(summary, "—", size=11, bold=True)
            val_lbl.grid(row=row_i, column=1, sticky="w", padx=(20, 0), pady=3)
            setattr(self, f"val_{key}", val_lbl)

        make_label(card, f"Saved to: {ATTENDANCE_FILE}",
                   size=9, color=COLORS["muted"]).pack(pady=(12, 0))

    # Buttons
        btn_row = tk.Frame(card, bg=COLORS["card"])
        btn_row.pack(pady=(28, 0))

        make_button(btn_row, "Mark Another ↩",
                        lambda: self.controller.show_frame(EmployeeCheckPage),
                        width=18).grid(row=0, column=0, padx=8)
        make_button(btn_row, "View Records",
                        lambda: self.controller.show_frame(ViewRecordsPage),
                        color=COLORS["success"], width=18).grid(row=0, column=1, padx=8)
        make_button(btn_row, "￼ Home",
                        lambda: self.controller.show_frame(HomePage),
                        color=COLORS["muted"], width=12).grid(row=0, column=2, padx=8)

    def set_data(self, emp: dict, status: str, record_id: int):
        now = datetime.now()
        status_colors = {"Present": COLORS["success"],
                         "Absent": COLORS["danger"],
                         "Late": COLORS["warning"]}
        self.val_record_id.config(text=f"#{record_id}")
        self.val_emp_id.config(text=emp["id"])
        self.val_emp_name.config(text=emp["name"])
        self.val_emp_dept.config(text=emp["department"])
        self.val_date.config(text=now.strftime("%Y-%m-%d"))
        self.val_time.config(text=now.strftime("%H:%M:%S"))
        self.val_status.config(text=status,
                        fg=status_colors.get(status, COLORS["text"]))
