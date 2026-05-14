import tkinter as tk
from config import COLORS
from ui.components import make_label, make_button, make_card

class MarkAttendancePage(tk.Frame):
  """Flowchart step: Mark Attendance(Present / Absent / Late) → Save to Excel"""
  def __init__(self, parent, controller):
     super().__init__(parent, bg=COLORS["bg"])
     self.controller = controller
     self.status_var = tk.StringVar(value="Present")
     self._build()

  def _build(self):
      header = tk.Frame(self, bg=COLORS["primary"], pady=20)
      header.pack(fill="x")
      make_label(header, "Mark Attendance", size=16, bold=True, color="white").pack()

      card = make_card(self, padx=50, pady=30)
      card.pack(expand=True)

     # Employee info panel
      info_card = make_card(card, padx=20, pady=16)
      info_card.pack(fill="x", pady=(0, 24))

      make_label(info_card, "Employee Details", size=10,
      color=COLORS["muted"]).grid(row=0, column=0, columnspan=2, sticky="w")

      labels = [("Name", "name"), ("Department", "department"), ("Position", "position")]
      for i, (lbl, key) in enumerate(labels, start=1):
         make_label(info_card, f"{lbl}:", size=11,
                    color=COLORS["muted"]).grid(row=i, column=0, sticky="w", pady=2)

         lbl_widget = make_label(info_card, "—", size=11, bold=True)
         lbl_widget.grid(row=i, column=1, sticky="w", padx=(12, 0), pady=2)
         setattr(self, f"lbl_{key}", lbl_widget)

         self.lbl_id = make_label(info_card, "", size=10, color=COLORS["muted"])
         self.lbl_id.grid(row=len(labels)+1, column=0, columnspan=2, sticky="w", pady=(4, 0))
      # Separator
         tk.Frame(card, bg=COLORS["border"], height=1).pack(fill="x", pady=(0, 20))

      # Status selection
         make_label(card, "Select Attendance Status", size=12, bold=True).pack(anchor="w")

         status_row = tk.Frame(card, bg=COLORS["card"])
         status_row.pack(pady=(12, 0), anchor="w")

         status_colors = {
            "Present": ("#16A34A", COLORS["present"]),
            "Absent": ("#DC2626", COLORS["absent"]),
            "Late": ("#D97706", COLORS["late"]),
              }
         for s, (fg, bg) in status_colors.items():
            rb = tk.Radiobutton(
               status_row, text=s, variable=self.status_var, value=s,
               font=("Helvetica", 12, "bold"),
                 fg=fg, bg=COLORS["card"],
                 activebackground=COLORS["card"],
                 selectcolor=bg,
                 indicatoron=True,
                 cursor="hand2",
                 )
            rb.pack(side="left", padx=16)

        # Date/time display
         self.datetime_label = make_label(card, "", size=10, color=COLORS["muted"])
         self.datetime_label.pack(pady=(16, 0))

        # Button
         btn_row = tk.Frame(card, bg=COLORS["card"])
         btn_row.pack(pady=(24, 0))

         make_button(btn_row, "Save Attendance", self._save,
                     color=COLORS["success"], width=20).grid(row=0, column=0, padx=8)
         make_button(btn_row, "← Back", self._go_back,
                     color=COLORS["muted"], width=14).grid(row=0, column=1, padx=8)

  def on_show(self):
         emp = self.controller.current_employee
         if not emp:
            return

         self.lbl_name.config(text=emp.get("name", "—"))
         self.lbl_department.config(text=emp.get("department", "—"))
         self.lbl_position.config(text=emp.get("position", "—"))
         self.lbl_id.config(text=f"ID: {emp.get('id', '')}")
         self.status_var.set("Present")
         self._refresh_time()

  def _refresh_time(self):
         now = datetime.now().strftime("%A, %d %B %Y  —  %H:%M:%S")
         self.datetime_label.config(text=f"{now}")
         self.after(1000, self._refresh_time)

  def _save(self):
     """Flowchart step: Save to Excel → Show Confirmation."""
     emp = self.controller.current_employee
     status = self.status_var.get()
     try:
           record_id = self.controller.db.save_attendance(emp, status)
     except RuntimeError as e:
          messagebox.showerror("Save Error", str(e))
          return

         # Pass data to confirmation page
     confirm_page = self.controller.frames[ConfirmationPage]
     confirm_page.set_data(emp, status, record_id)
     self.controller.show_frame(ConfirmationPage)

  def _go_back(self):
     self.controller.current_employee = None
     self.controller.show_frame(EmployeeCheckPage)
