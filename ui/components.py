import tkinter as tk
from config import COLORS

def make_card(parent, **kwargs) -> tk.Frame:
    return tk.Frame(parent, bg=COLORS["card"],
                    relief="flat", bd=0,
                    highlightbackground=COLORS["border"],
                    highlightthickness=1, **kwargs)

def make_label(parent, text, size=12, bold=False, color=None, **kwargs):
    return tk.Label(parent, text=text,
                    font=("Helvetica", size, "bold" if bold else "normal"),
                    fg=color or COLORS["text"],
                    bg=parent.cget("bg"), **kwargs)

def make_button(parent, text, command, color=None, width=16, **kwargs):
    btn_color = color or COLORS["primary"]
    btn = tk.Button(parent, text=text, command=command,
                    bg=btn_color, fg="white",
                    font=("Helvetica", 11, "bold"),
                    relief="flat", bd=0, cursor="hand2",
                    width=width, pady=8, **kwargs)
    btn.bind("<Enter>", lambda e: btn.config(bg=COLORS["primary_dark"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=btn_color))
    return btn

def make_entry(parent, textvariable=None, width=30, **kwargs):
    entry = tk.Entry(parent, textvariable=textvariable,
                     font=("Helvetica", 12),
                     relief="flat", bd=0,
                     bg=COLORS["bg"],
                     fg=COLORS["text"],
                     highlightbackground=COLORS["border"],
                     highlightthickness=1,
                     width=width, **kwargs)
    return entry