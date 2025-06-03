import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from datetime import datetime
from tkcalendar import DateEntry
from collections import defaultdict
from .common import change_number_to_thousand, change_to_float, change_to_string
class Revenue:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("💳 Doanh thu")
        self.window.geometry("800x500")
        self.build_ui()

    def setup_button_style(self, window):
        style = ttk.Style(window)
        style.configure("Rounded.TButton",
                        font=("Segoe UI", 11, "bold"),
                        foreground="white",
                        background="#5BC0EB",
                        padding=5,
                        borderwidth=1)
        style.map("Rounded.TButton",
                  background=[("active", "#4299c7")])

    def build_ui(self):
        title = ttk.Label(self.window, text= "Doanh thu", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=5)