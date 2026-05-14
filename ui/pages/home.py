import tkinter as tk
from config import *
from ui.components import make_label, make_button, make_card
from datetime import datetime

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
       super().__init__(parent, bg=COLORS["bg"])
       self.controller = controller
       self._build()

    def _build(self):
       # Header banner
       header = tk.Frame(self, bg=COLORS["primary"], pady=30)
       header.pack(fill="x")
       make_label(header, "Employee Attendance Tracker",
                  size=20, bold=True, color="white").pack()
       make_label(header, datetime.now().strftime("%A, %d %B %Y"),
                  size=12, color="#BFDBFE").pack(pady=(4, 0))
   # Main card
       card = make_card(self, padx=40, pady=40)
       card.pack(expand=True)

       make_label(card, "What would you like to do?",
                  size=14, bold=True).pack(pady=(0, 24))
       btn_frame = tk.Frame(card, bg=COLORS["card"])
       btn_frame.pack()
       make_button(btn_frame, "Mark Attendance",
                   lambda: self.controller.show_frame(EmployeeCheckPage),
                   width=22).grid(row=0, column=0, padx=10, pady=8)

       make_button(btn_frame, "View Today's Records",
                   lambda: self.controller.show_frame(ViewRecordsPage),
                   color=COLORS["success"], width=22).grid(row=0, column=1, padx=10, pady=8)

       make_label(card, f"Excel DB:  {DB_FILE}  |  Attendance:  {ATTENDANCE_FILE}",
                  size=9, color=COLORS["muted"]).pack(pady=(28, 0))
