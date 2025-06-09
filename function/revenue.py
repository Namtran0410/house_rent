import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from datetime import datetime
from turtle import color, window_width
from tkcalendar import DateEntry
from collections import defaultdict

from function import transaction
from .common import *
field_count = 0
class Revenue:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("💳 Doanh thu")
        self.window.geometry("800x500")
        self.build_ui()
        self.load_data()
        
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

        ttk.Button(btn_frame, text="➕ Chi phí phát sinh", command=self.add_expensed).pack(side="left", padx=5)

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
    
    #1 Chi phí thêm của tháng
    def add_expensed(self): 
        add_expensed_window = tk.Toplevel(self.window)
        add_expensed_window.title("Add chi phí phát sinh")
        add_expensed_window.geometry("300x300")
        add_expensed_window.grab_set()

        self.setup_button_style(add_expensed_window)

        # Form tổng
        form_frame = ttk.Frame(add_expensed_window, padding=10)
        form_frame.pack(fill="both", expand=True)

        # Frame chứa các label/entry + nút thêm
        self.button_add_frame = tk.Frame(form_frame)
        self.button_add_frame.pack(fill="both", expand=True, anchor="nw")

        # Frame chứa nút Lưu dưới cùng
        save_btn_frame = ttk.Frame(add_expensed_window)
        save_btn_frame.pack(side="bottom", pady=10)

        # Nút Lưu (tạo 1 lần duy nhất)
        ttk.Button(save_btn_frame, text="Lưu", command=lambda: print("Lưu dữ liệu"))\
            .pack(anchor="center")

        # Đếm số dòng
        self.field_count = 0
        def add_field():
            self.field_count += 1
            ttk.Label(self.button_add_frame, text=f"Label {self.field_count}")\
                .grid(row=self.field_count, column=0, padx=5, pady=2, sticky="w")
            ttk.Entry(self.button_add_frame, width=25)\
                .grid(row=self.field_count, column=1, padx=5, pady=2)

        # Nút thêm nhãn (ở hàng 0)
        ttk.Button(self.button_add_frame, text="➕Thêm nhãn", command=add_field)\
            .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

            
    # add vào treeview
    def load_data(self):
        # Load các dữ liệu từ file Json 
        #1: lấy data từ transaction và lọc theo tháng - tháng và doanh thu
        revenue_per_months = revenue_per_month("data/transaction.json")  #[{'6': 945000}, {'7': 295000}]

        #2 lấy chi phí ban đầu : số điện ban đầu, số nước ban đầu
        usage_per_months = expense_per_month("data/transaction.json", "data/setting.json") # [{'6': 130000}, {'7': 30000}]

        #3: lấy data cho treeview
        revenue_month_format= [{'month': int(k), 'revenue': v} for d in revenue_per_months for k, v in d.items()]
        usage_per_months_format= [{'month': int(k), 'expense': v} for d in usage_per_months for k, v in d.items()]

        #4: merge 2 list    
        merged_data = []
        for i in range(1, 13):
            month_data = {'month': i}
            for data in revenue_month_format:
                if data['month'] == i:
                    month_data['revenue'] = data['revenue']
                    break
                else:
                    month_data['revenue'] = 0 
            for data in usage_per_months_format:
                if data['month'] == i:
                    month_data['expense'] = data['expense']
                    break
                else: 
                    month_data['expense'] = 0 
            merged_data.append(month_data)
            month_data['profit'] = month_data['revenue'] - month_data['expense']

            self.tree.insert("", "end", values=(month_data['month'], change_number_to_thousand(month_data['expense'])
            , "Chi phí thêm", change_number_to_thousand(month_data['revenue']), 
            change_number_to_thousand((month_data['profit'])), "Tăng giảm"))

#TODO: Lọc theo năm 





























































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