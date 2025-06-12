from email import message
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
        btn_frame.pack(fill="x", padx=10, pady=5, anchor="w") 

        # Nút "Chọn năm" với biểu tượng filter
        ttk.Label(btn_frame, text="🔍 Chọn năm", width=15, anchor="w").pack(side="left")
        self.choos_year_variable = tk.StringVar()
        choose_year_button = ttk.Combobox(btn_frame, textvariable= self.choos_year_variable, values= self.get_year())
        choose_year_button.current(0)
        choose_year_button.pack(side="left")

        # Nút "Chi phí phát sinh"
        ttk.Button(btn_frame, text="➕ Chi phí phát sinh", command=self.add_expensed).pack(side="left", padx=20)

        self.columns = ("Tháng", "Chi phí ban đầu", "Chi phí tổng", "Doanh thu", "Lợi nhuận", "Tăng giảm")
        self.tree = ttk.Treeview(self.window, columns = self.columns, show="headings", height=15, selectmode="extended")
        self.tree.pack(fill= "both", expand= True, padx=10, pady=10)
        choose_year_button.bind("<<ComboboxSelected>>", self.update_treeview_by_year)

        col_widths = {
            "Tháng": 100,
            "Chi phí ban đầu": 80,
            "Chi phí tổng": 80,
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
        selected = self.tree.selection()
        if not selected: 
            messagebox.showerror("Lỗi", "Vui lòng chọn giao dịch để sửa")
            return

        self.selected_data = self.tree.item(selected, "values")

        add_expensed_window = tk.Toplevel(self.window)
        add_expensed_window.title("Add chi phí phát sinh")
        add_expensed_window.geometry("300x400")
        add_expensed_window.grab_set()

        self.setup_button_style(add_expensed_window)

        form_frame = ttk.Frame(add_expensed_window, padding=10)
        form_frame.pack(fill="both", expand=True)

        self.button_add_frame = tk.Frame(form_frame)
        self.button_add_frame.pack(fill="both", expand=True, anchor="nw")

        save_btn_frame = ttk.Frame(add_expensed_window)
        save_btn_frame.pack(side="bottom", pady=10)

        ttk.Button(save_btn_frame, text="Lưu", command=self.calculate_expensed).pack(anchor="center")

        self.expensed_electric_var = tk.StringVar()
        ttk.Label(self.button_add_frame, text=f"Tổng số điện")\
            .grid(row=1, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(self.button_add_frame, width=25, textvariable=self.expensed_electric_var)\
            .grid(row=1, column=1, padx=5, pady=2)

        self.expensed_water_var = tk.StringVar()
        ttk.Label(self.button_add_frame, text=f"Tổng số nước")\
            .grid(row=2, column=0, padx=5, pady=2, sticky="w")
        ttk.Entry(self.button_add_frame, width=25, textvariable=self.expensed_water_var)\
            .grid(row=2, column=1, padx=5, pady=2)

        self.field_count = 2
        self.field_vars = []

        def add_field(value=""):
            self.field_count += 1
            var = tk.StringVar(value=value)
            ttk.Label(self.button_add_frame, text=f"Label {self.field_count}")\
                .grid(row=self.field_count, column=0, padx=5, pady=2, sticky="w")
            ttk.Entry(self.button_add_frame, width=25, textvariable=var)\
                .grid(row=self.field_count, column=1, padx=5, pady=2)
            self.field_vars.append(var)

        ttk.Button(self.button_add_frame, text="➕Thêm nhãn", command=add_field)\
            .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        # Load saved data if exists
        expensed_file = 'data/expensed.json'
        loaded_record = None

        if os.path.exists(expensed_file):
            with open(expensed_file, "r", encoding="utf-8") as f:
                try:
                    loaded_data = json.load(f)
                    for item in loaded_data:
                        if item.get("month") == self.selected_data[0]:
                            loaded_record = item
                            break
                except json.JSONDecodeError:
                    pass

        if loaded_record:
            self.expensed_electric_var.set(loaded_record.get("total_electric", ""))
            self.expensed_water_var.set(loaded_record.get("total_water", ""))

            for i, val in enumerate(loaded_record.get("total_other_expensed", []), start=3):
                add_field(str(val))

    def calculate_expensed(self):
        with open('data/setting.json', "r", encoding="utf-8") as f:
            data = json.load(f)

        base_price_electric = int(data[0]['electric_base_price'])
        base_price_water = int(data[0]['water_base_price'])

        if self.selected_data:
            self.expendsed_month = self.selected_data[0]
            self.total_price_electric = int(self.expensed_electric_var.get()) * base_price_electric
            self.total_price_water = int(self.expensed_water_var.get()) * base_price_water
            self.total_other_expensed = sum(int(var.get()) for var in self.field_vars if var.get().isdigit())
            self.total_expensed = self.total_price_electric + self.total_price_water + self.total_other_expensed

            other_expense_values = [int(var.get()) for var in self.field_vars if var.get().isdigit()]

            data_expensed = {
                "month": self.expendsed_month,
                "total_electric": self.expensed_electric_var.get(),
                "total_water": self.expensed_water_var.get(),
                "total_other_expensed": other_expense_values,
                "total_expensed": self.total_expensed
            }

            expensed_file = 'data/expensed.json'
            if os.path.exists(expensed_file):
                with open(expensed_file, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                    except:
                        existing_data = []
            else:
                existing_data = []

            existing_data = [d for d in existing_data if d["month"] != self.expendsed_month]
            existing_data.append(data_expensed)

            with open(expensed_file, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Đã lưu chi phí phát sinh")
            
    # add vào treeview
    def load_data(self):
        # Load các dữ liệu từ file Json 
        year = self.choos_year_variable.get()
        if not year:
            return  # Không có năm được chọn thì thoát luôn
        #1: lấy data từ transaction và lọc theo tháng - tháng và doanh thu
        revenue_per_months = revenue_per_month("data/transaction.json", year)  #[{'6': 945000}, {'7': 295000}]

        #2 lấy chi phí ban đầu : số điện ban đầu, số nước ban đầu
        usage_per_months = expense_per_month("data/transaction.json", "data/setting.json", year) # [{'6': 130000}, {'7': 30000}]

        #3: lấy data cho treeview
        revenue_month_format= [{'month': int(k), 'revenue': v} for d in revenue_per_months for k, v in d.items()]
        usage_per_months_format= [{'month': int(k), 'expense': v} for d in usage_per_months for k, v in d.items()]

        #4: merge 2 list  
        previous_profit = 0    
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

            month_data['profit'] = month_data['revenue'] - month_data['expense']
            status = self.get_status(month_data['profit'], previous_profit)
            previous_profit = month_data['profit']

            self.tree.insert("", "end", values=(
                month_data['month'],
                change_number_to_thousand(month_data['expense']),
                self.add_expensed_content(),
                change_number_to_thousand(month_data['revenue']),
                change_number_to_thousand(month_data['profit']),
                status
            ))

    def get_year(self):
        list_year = []
        file_path = "data/transaction.json"
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists(file_path):
            data= []
        else: 
            with open(file_path, "r", encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    if 'time' in item:
                        year = item['time'].split("/")[-1]
                        if year not in list_year:
                            list_year.append(year)
        return list_year

    def update_treeview_by_year(self, event= None):
        year = self.choos_year_variable.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if year: 
            revenue_per_months = revenue_per_month("data/transaction.json", year)
            usage_per_months = expense_per_month("data/transaction.json", "data/setting.json", year)

            revenue_month_format = [{'month': int(k), 'revenue': v} for d in revenue_per_months for k, v in d.items()]
            usage_per_months_format = [{'month': int(k), 'expense': v} for d in usage_per_months for k, v in d.items()]

            #4: merge 2 list    
            merged_data = []
            previous_profit = 0
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

                month_data['profit'] = month_data['revenue'] - month_data['expense']
                status = self.get_status(month_data['profit'], previous_profit)
                previous_profit = month_data['profit']
                fee = self.add_expensed_content()
                self.tree.insert("", "end", values=(
                    month_data['month'],
                    change_number_to_thousand(month_data['expense']),
                    fee,
                    change_number_to_thousand(month_data['revenue']),
                    change_number_to_thousand(month_data['profit']),
                    status
                ))
        else:
            return 

    def get_status(self, current_profit, previous_profit):
        delta = current_profit - previous_profit
        if delta > 0:
            return "🔺 Tăng"
        elif delta < 0:
            return "🔻 Giảm"
        else :
            return "⚪ Không đổi"


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

    def add_expensed_content(self):
        # Lấy month làm gốc
        loaded_record = None
        selected = self.tree.selection()
        selected_data = self.tree.item(selected, "values")
        if not selected: 
            return 0
        month = selected_data[0]

        with open('data/expensed.json', "r", encoding='utf-8') as f:
            data= json.load(f)

        # Load thu tiền
        with open('data/transaction.json', "r", encoding='utf-8') as f:
            data_in = json.load(f)
        month_value = {}

        #Lấy tháng và lấy tổng chi phí 
        for item in data_in:
            month_in = item['time'].split("/")[0]
            year_in = item['time'].split("/")[-1]
            value = item["total_fee"]
            if year_in != self.choos_year_variable.get():
                continue
            if month_in in month_value:
                month_value[month_in] += int(value)
            else: 
                month_value[month_in] = int(value)
                # month_value = {"6", xxxxxxxx, "7": yyyyy}

        # Load ban đầu
            first_expensed = int(selected_data[1])

        for dict in data: 
            if dict['month'] == month :
                loaded_record = dict 
        if loaded_record and month in month_value: 
            fee= int(loaded_record['total_expensed']) + month_value[month] - first_expensed
            return fee
        else:
            return 0