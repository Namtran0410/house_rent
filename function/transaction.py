import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from tkcalendar import DateEntry
from collections import defaultdict

class Transaction:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("💳 Giao dịch")
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
        title = ttk.Label(self.window, text= "Giao dịch hàng tháng", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Thêm giao dịch", command=self.add_transaction).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Sửa giao dịch", command=self.edit_transaction).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Xóa giao dịch", command=self.delete_transaction).pack(side="left", padx=5)
        col_widths = {
            "Thời gian": 100,
            "Số Phòng": 80,
            "Số người": 80,
            "Số điện": 80,
            "Số nước": 80,
            "Tiền dịch vụ": 100,
            "Tổng tiền": 100,
            "Trạng thái": 80
        }
        columns = ("Thời gian", "Số Phòng", "Số người", "Số điện", "Số nước", "Tiền dịch vụ", "Tổng tiền", "Trạng thái")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=15)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width= col_widths[col])

        self.load_data()

    def add_transaction(self):
        # Tạo cửa sổ giao dịch 
        add_transaction_window = tk.Toplevel(self.window)
        add_transaction_window.title("Thêm giao dịch")
        add_transaction_window.geometry("300x200")
        add_transaction_window.grab_set()
        self.setup_button_style(add_transaction_window)
        
        # Tạo các entry
        form_frame = ttk.Frame(add_transaction_window, padding=10)
        form_frame.pack(fill="both", expand=True)

        # Tạo entry thời gian
        self.time_var = tk.StringVar()
        ttk.Label(form_frame, text="Thời gian", width=15, anchor="w").grid(row=0, column=0, padx=2, pady=5)
        self.date_entry = DateEntry(form_frame, textvariable=self.time_var, width = 22)
        self.date_entry.grid(row=0, column=1, padx=2, pady=5)

    # Tạo combobox cho số phòng
        self.room_var = tk.StringVar()
        # Tạo options
        if not os.path.exists("data/list.json"):
            self.options_room = []
        else:
            with open("data/list.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.options_room = sorted(set(item["room"] for item in data))

        # Tạo combobox
        ttk.Label(form_frame, text="Số phòng", width=15, anchor="w").grid(row=1, column=0, padx=2, pady=5)
        self.room_combobox = ttk.Combobox(form_frame, textvariable=self.room_var, values = self.options_room, width = 22)
        self.room_combobox.grid(row=1, column=1, padx=2, pady=5)
        self.room_combobox.current(0)
        self.room_combobox.bind("<<ComboboxSelected>>", self.update_human_entry)

        # room count
        self.room_counts = defaultdict(int)
        for item in data:
            self.room_counts[item["room"]] += 1
        self.room_counts = dict(self.room_counts)

        # Tạo entry khác
        labels = ["Số người","Số điện", "Số nước", "Tiền dịch vụ", "Tổng tiền", "Trạng thái"]
        self.entry_vars =[]

        for i, text in enumerate(labels):
            var = tk.StringVar()
            ttk.Label(form_frame, text=text, width=15, anchor="w").grid(row=i+2, column=0, padx=2, pady=5)
            ttk.Entry(form_frame, textvariable=var, width=25).grid(row=i+2, column=1, padx=2, pady=5)
            self.entry_vars.append(var)
            
        def add_transaction_action():
            for var in self.entry_vars:
                if not var.get():
                    messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
                    return

            new_data = {
                "time": self.time_var.get(),
                "room": self.room_var.get(),
                "number_human": self.entry_vars[0].get(),
                "number_electric": self.entry_vars[1].get(),
                "number_water": self.entry_vars[2].get(),
                "service_fee": self.entry_vars[3].get(),
                "total_fee": self.entry_vars[4].get(),
                "status": self.entry_vars[5].get()
            }
            file_path = "data/transaction.json"
            if not os.path.exists("data"):
                os.makedirs("data")
            if not os.path.exists(file_path):
                data = []
            else: 
                with open(file_path, "r", encoding= "utf-8") as f:
                    try: 
                        data = json.load(f)
                        if not isinstance(data, list):
                            data= [data]
                    except json.JSONDecodeError:
                        data = []
            data.append(new_data)
            with open(file_path, "w", encoding= "utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            self.tree.insert("", "end", values=(new_data["time"], new_data["room"], new_data["number_human"], new_data["number_electric"], new_data["number_water"], new_data["service_fee"], new_data["total_fee"], new_data["status"]))
            messagebox.showinfo("Thông báo", "Thêm giao dịch thành công", parent=add_transaction_window)
            add_transaction_window.destroy()

        # Nút xác nhận
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=15, sticky="ew")
        tk.Button(button_frame,
          text="➕ Thêm",
          font=("Segoe UI", 11, "bold"),
          bg="#5BC0EB",
          fg="white",
          activebackground="#4299c7",
          relief="flat",
          bd=0,
          padx=10,
          pady=5,
          cursor="hand2",
          command=add_transaction_action).pack(fill="x")    
           
    def edit_transaction(self):
        pass

    def delete_transaction(self):
        pass

    def load_data(self):
        pass

    def update_human_entry(self, event=None):
        room = self.room_var.get()
        count = self.room_counts.get(room, 0)
        self.entry_vars[0].set(str(count))
