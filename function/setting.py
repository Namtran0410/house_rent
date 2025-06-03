import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from tkcalendar import DateEntry
from collections import defaultdict

class Setting:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("🔧 Cài đặt")
        self.window.geometry("800x500")
        self.build_ui()
        self.update_setting()

    def build_ui(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(expand=True, fill="both")

        # Title frame dùng pack
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=10)
        title = ttk.Label(title_frame, text="Cài đặt chung", font=("Helvetica", 16, "bold"))
        title.pack(anchor="center")

        # Label frame dùng grid nhưng nằm trong main_frame
        label_frame = ttk.Frame(main_frame)
        label_frame.pack(pady=10)

        # Giá đầu tư
        self.invest_value = tk.StringVar()
        ttk.Label(label_frame, text="Giá đầu tư", font=("Helvetica", 10, "bold")).grid(column=0, row=0, padx=5, pady=5, sticky="w")
        self.initial_investment_entry = ttk.Entry(label_frame, textvariable=self.invest_value)
        self.initial_investment_entry.grid(column=1, row=0, padx=5, pady=5, sticky="w")

        labels = ["Giá điện gốc", "Giá điện kinh doanh"]
        self.entry_electric_vars = []
        for i, label in enumerate(labels):
            var = tk.StringVar()
            ttk.Label(label_frame, text=label, font=("Helvetica", 10, "bold")) \
                .grid(column=i * 2, row=1, padx=5, pady=10, sticky="w")

            ttk.Entry(label_frame, textvariable=var) \
                .grid(column=i * 2 + 1, row=1, padx=5, pady=10, sticky="w")
            self.entry_electric_vars.append(var)

        labels = ["Giá nước gốc", "Giá nước kinh doanh"]
        self.entry_water_vars = []
        for i, label in enumerate(labels):
            var = tk.StringVar()
            ttk.Label(label_frame, text=label, font=("Helvetica", 10, "bold")) \
                .grid(column=i * 2, row=2, padx=5, pady=10, sticky="w")

            ttk.Entry(label_frame, textvariable=var) \
                .grid(column=i * 2 + 1, row=2, padx=5, pady=10, sticky="w")
            self.entry_water_vars.append(var)

        # Giá dịch vụ kinh doanh 
        self.entry_service_vars = tk.StringVar()
        ttk.Label(label_frame, text= "Giá dịch vụ kinh doanh", font=("Helvetica", 10, "bold")) \
            .grid(column =0, row=3, padx=5, pady=10, sticky="w")
        ttk.Entry(label_frame, textvariable=self.entry_service_vars) \
            .grid(column =1, row=3, padx=5, pady=10, sticky="w")
        
        # Nút lưu thông tin
        save_button_frame = ttk.Frame(main_frame)
        save_button_frame.pack(pady=10, side="right", anchor="se")
        save_button = ttk.Button(save_button_frame, text="Lưu thông tin", command=self.save_info)
        save_button.pack()
        
    def save_info(self):
        
        # Lấy giá trị từ các entry 
        invest_value = self.initial_investment_entry.get()
        electric_price = [var.get() for var in self.entry_electric_vars]
        water_price = [var.get() for var in self.entry_water_vars]
        service_price = self.entry_service_vars.get()

        # Kiểm tra giá trị 
        if not invest_value or not all(electric_price) or not all(water_price) or not service_price:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin", parent=self.window)
            return

        # Lưu giá trị vào file setting.json
        setting_data = {
            "invest_value": invest_value,
            "electric_base_price": electric_price[0],
            "electric_business_price": electric_price[1],
            "water_base_price": water_price[0],
            "water_business_price": water_price[1],
            "service_price": service_price
        }
        file_path = "data/setting.json"
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                data = []
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data= [data]
            except json.JSONDecodeError:
                data = []
        data = [setting_data]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Thông báo", "Cài đặt thành công", parent=self.window)

    def load_setting(self):
        # Load các giá trị trong json
        file_path = "data/setting.json"
        
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                data = []
        with open(file_path, "r", encoding="utf-8") as f:
            try: 
                data= json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []
        return data
    
    def update_setting(self):
        load_data = self.load_setting()
        if load_data:
            # Lấy giá trị từ các entry 
            self.invest_value.set(load_data[0]["invest_value"])
            self.entry_electric_vars[0].set(load_data[0]["electric_base_price"])
            self.entry_electric_vars[1].set(load_data[0]["electric_business_price"])
            self.entry_water_vars[0].set(load_data[0]["water_base_price"])
            self.entry_water_vars[1].set(load_data[0]["water_business_price"])
            self.entry_service_vars.set(load_data[0]["service_price"])


        






