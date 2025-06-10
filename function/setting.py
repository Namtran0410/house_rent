import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from turtle import width
from tkcalendar import DateEntry
from collections import defaultdict

class Setting:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("🔧 Cài đặt")
        self.window.geometry("720x360")
        self.build_ui()
        self.update_setting()

    def build_ui(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(expand=True, fill="both")

        title_frame = ttk.Frame(main_frame)
        title_frame.pack(pady=10)
        title = ttk.Label(title_frame, text="Cài đặt chung", font=("Helvetica", 16, "bold"))
        title.pack(anchor="center")

        label_frame = ttk.Frame(main_frame)
        label_frame.pack(pady=10)

        # Giá đầu tư
        self.invest_value = tk.StringVar()
        ttk.Label(label_frame, text="Giá đầu tư", font=("Helvetica", 10, "bold")).grid(column=0, row=0, padx=5, pady=5, sticky="w")
        self.initial_investment_entry = ttk.Entry(label_frame, textvariable=self.invest_value)
        self.initial_investment_entry.grid(column=1, row=0, padx=5, pady=5, sticky="w")
        self.initial_investment_entry.bind("<KeyRelease>", lambda e: self.format_thousand(self.invest_value, self.initial_investment_entry))

        # Giá điện
        labels = ["Giá điện gốc", "Giá điện kinh doanh"]
        self.entry_electric_vars = []
        for i, label in enumerate(labels):
            var = tk.StringVar()
            ttk.Label(label_frame, text=label, font=("Helvetica", 10, "bold")) \
                .grid(column=i * 2, row=1, padx=5, pady=10, sticky="w")
            entry = ttk.Entry(label_frame, textvariable=var)
            entry.grid(column=i * 2 + 1, row=1, padx=5, pady=10, sticky="w")
            entry.bind("<KeyRelease>", lambda e, v=var, w=entry: self.format_thousand(v, w))
            self.entry_electric_vars.append(var)

        # Giá nước
        labels = ["Giá nước gốc", "Giá nước kinh doanh"]
        self.entry_water_vars = []
        for i, label in enumerate(labels):
            var = tk.StringVar()
            ttk.Label(label_frame, text=label, font=("Helvetica", 10, "bold")) \
                .grid(column=i * 2, row=2, padx=5, pady=10, sticky="w")
            entry = ttk.Entry(label_frame, textvariable=var)
            entry.grid(column=i * 2 + 1, row=2, padx=5, pady=10, sticky="w")
            entry.bind("<KeyRelease>", lambda e, v=var, w=entry: self.format_thousand(v, w))
            self.entry_water_vars.append(var)

        # Giá dịch vụ kinh doanh
        self.entry_service_vars = tk.StringVar()
        ttk.Label(label_frame, text="Giá dịch vụ kinh doanh", font=("Helvetica", 10, "bold")) \
            .grid(column=0, row=3, padx=5, pady=10, sticky="w")
        self.service_entry = ttk.Entry(label_frame, textvariable=self.entry_service_vars)
        self.service_entry.grid(column=1, row=3, padx=5, pady=10, sticky="w")
        self.service_entry.bind("<KeyRelease>", lambda e: self.format_thousand(self.entry_service_vars, self.service_entry))

        # Nút thêm giá phòng
        ttk.Button(label_frame, text="Thêm giá phòng", command = self.add_room).grid(column=0, row=4, padx=5, 
        columnspan=2, pady=10, sticky="w")

        # Nút lưu
        save_button_frame = ttk.Frame(main_frame)
        save_button_frame.pack(pady=10, side="right", anchor="se")
        save_button = ttk.Button(save_button_frame, text="Lưu thông tin", command=self.save_info)
        save_button.pack()

    def save_info(self):
        # Lấy và làm sạch giá trị
        invest_value = self.clean_number(self.invest_value.get())
        electric_price = [self.clean_number(var.get()) for var in self.entry_electric_vars]
        water_price = [self.clean_number(var.get()) for var in self.entry_water_vars]
        service_price = self.clean_number(self.entry_service_vars.get())

        # Kiểm tra
        if not invest_value or not all(electric_price) or not all(water_price) or not service_price:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin", parent=self.window)
            return

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

        # Đọc dữ liệu cũ nếu có
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
        except (json.JSONDecodeError, FileNotFoundError):
            data = []

        data = [setting_data]  # Ghi đè
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Thông báo", "Cài đặt thành công", parent=self.window)

    def load_setting(self):
        file_path = "data/setting.json"
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
        except json.JSONDecodeError:
            data = []

        return data

    def update_setting(self):
        load_data = self.load_setting()
        if load_data:
            d = load_data[0]
            self.invest_value.set(f"{int(d['invest_value']):,}")
            self.entry_electric_vars[0].set(f"{int(d['electric_base_price']):,}")
            self.entry_electric_vars[1].set(f"{int(d['electric_business_price']):,}")
            self.entry_water_vars[0].set(f"{int(d['water_base_price']):,}")
            self.entry_water_vars[1].set(f"{int(d['water_business_price']):,}")
            self.entry_service_vars.set(f"{int(d['service_price']):,}")

    def format_thousand(self, var, entry_widget):
        value = var.get().replace(",", "")
        if value.isdigit():
            formatted = f"{int(value):,}"
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, formatted)

    def clean_number(self, s):
        return s.replace(",", "")

    def add_room(self):
        self.add_room_window = tk.Toplevel(self.window)
        self.add_room_window.title("Thêm phòng và giá phòng")
        self.add_room_window.geometry("480x720")
        
        # Thêm nút bấm
        #Frame tổng 
        form_frame = ttk.Frame(self.add_room_window, padding=10)
        form_frame.pack(fill="both", expand=True)

        self.field_count = 0
        self.entries = []

        def add_room_infor():
            if self.entries:
                last_entries = self.entries[-1]
                room= last_entries[0].get().strip()
                price = last_entries[1].get().strip()
                if not room and not price:
                    return

            self.field_count += 1
            # Tạo label
            ttk.Label(form_frame, text="Số phòng")\
                .grid(row= self.field_count, column=0, padx=5, pady=2, sticky="w") 

            #Tạo entry
            ttk.Entry(form_frame, width=25)\
                .grid(row= self.field_count, column=1, padx=5, pady=2)

            #Tạo VNĐ giá tiền đằng sau 
            ttk.Label(form_frame, text="VNĐ")\
                .grid(row= self.field_count, column=2, padx=5, pady=2) 

            ttk.Entry(form_frame, width=25)\
                .grid(row= self.field_count, column=3, padx=5, pady=2)

        ttk.Button(form_frame, text='Thêm thông tin phòng',command= add_room_infor)\
            .grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        # Frame chứa nút Lưu dưới cùng
        save_btn_frame = ttk.Frame(self.add_room_window)
        save_btn_frame.pack(side="bottom", pady=10)

        # Nút Lưu (tạo 1 lần duy nhất)
        ttk.Button(save_btn_frame, text="Lưu", command=lambda: print("Lưu dữ liệu"))\
            .pack(anchor="center")

#TODO: Lưu data và các entry