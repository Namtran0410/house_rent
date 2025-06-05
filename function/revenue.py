import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from datetime import datetime
from turtle import window_width
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

        self.columns = ("Tháng", "Chi phí ban đầu", "Chi phí thêm", "Doanh thu", "Lợi nhuận", "Tăng giảm")
        self.tree = ttk.Treeview(self.window, columns = self.columns, show="headings", height=15, selectmode="extended")
        self.tree.pack(fill= "both", expand= True, padx=10, pady=10)

        col_widths = {
            "Tháng": 100,
            "Chi phí ban đầu": 80,
            "Chi phí thêm": 80,
            "Doanh thu": 80,
            "Lợi nhuận": 80,
            "Tăng giảm": 100
        }
        for col in self.columns:
            if col == "Tháng":
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_tree_by_date(c, False))
            else:
                self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width= col_widths[col])
    
        self.tree.insert("", "end", values=("06/2025", "1000", "500", "3000", "1500", "+50%"))

    def sort_tree_by_date(self, col, reverse):
        # Lấy dữ liệu từ tree
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]

        # Chuyển chuỗi "6/3/25" thành datetime
        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, "%m/%d/%y")  # nếu định dạng là mm/dd/yy
            except ValueError:
                return datetime.min  # fallback nếu lỗi

        # Sort theo ngày
        items.sort(key=lambda t: parse_date(t[0]), reverse=reverse)

        # Reorder treeview
        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

        # Đảo ngược chiều sort khi click lại
        self.tree.heading(col, command=lambda: self.sort_tree_by_date(col, not reverse))