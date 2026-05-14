import tkinter as tk
from database.excel_db import ExcelDB
from ui.pages.employee_check import EmployeeCheckPage
from ui.pages.mark_attendence import MarkAttendancePage
from ui.pages.home import HomePage
from ui.pages.confirmation import ConfirmationPage
from ui.pages.view_records import ViewRecordsPage
from config import COLORS

class EAT_App(tk.Tk):
    """Main application window — manages frames (pages)."""
    def __init__(self):
        super().__init__()
        self.db = ExcelDB()
        self.title("Employee Attendance Tracker")
        self.geometry("900x650")
        self.resizable(True, True)
        self.configure(bg=COLORS["bg"])

# Shared state passed between pages
        self.current_employee = None

# Container holds all frames stacked on top of each other
        container = tk.Frame(self, bg=COLORS["bg"])
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for PageClass in(HomePage, EmployeeCheckPage, MarkAttendancePage,
                        ConfirmationPage, ViewRecordsPage):
            frame = PageClass(parent=container, controller=self)
            self.frames[PageClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(HomePage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        if hasattr(frame, "on_show"):
            frame.on_show()
            frame.tkraise()