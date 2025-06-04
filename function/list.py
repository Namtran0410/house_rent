import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

class ListRoomPeople:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("🏠 Thống kê phòng và người")
        self.window.geometry("800x500")

        self.sort_asc = True  # Biến để toggle sắp xếp tăng/giảm

        self.setup_button_style(self.window)
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
        title = ttk.Label(self.window, text="📋 Danh sách phòng và người", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="➕ Thêm", command=self.add_room).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="✏️ Sửa", command=self.edit_room).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Xóa", command=self.delete_room).pack(side="left", padx=5)

        columns = ("Phòng", "Người ở", "Nghề nghiệp", "số điện thoại")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=15, selectmode= "extended")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.heading("Phòng", text="Phòng", command=self.toggle_sort_by_room)

        for col in columns:
            self.tree.column(col, anchor="center")

        self.load_data()

    def extract_room_number(self, room):
        match = re.match(r"(\d+)", room)
        return int(match.group(1)) if match else room

    def toggle_sort_by_room(self):
        self.sort_asc = not self.sort_asc
        self.load_data()

    def load_data(self):
        file_path = "data/list.json"
        if not os.path.exists(file_path):
            return
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []

        # Sắp xếp tăng hoặc giảm dựa trên self.sort_asc
        data.sort(key=lambda x: self.extract_room_number(x["room"]), reverse=not self.sort_asc)

        self.tree.delete(*self.tree.get_children())
        for item in data:
            self.tree.insert("", "end", values=(item["room"], item["name"], item["job"], item["phone"]))

    def add_room(self):
        add_room_window = tk.Toplevel(self.window)
        add_room_window.title("➕ Thêm thông tin phòng")
        add_room_window.geometry("300x200")
        add_room_window.grab_set()

        self.setup_button_style(add_room_window)
        form_frame = ttk.Frame(add_room_window, padding=10)
        form_frame.pack(fill="both", expand=True)

        labels = ["Tên phòng:", "Tên thành viên:", "Nghề nghiệp:", "Số điện thoại:"]
        entry_vars = []

        for i, text in enumerate(labels):
            var = tk.StringVar()
            ttk.Label(form_frame, text=text, width=15, anchor="w").grid(row=i, column=0, padx=5, pady=5)
            ttk.Entry(form_frame, width=25, textvariable=var).grid(row=i, column=1, padx=2, pady=5)
            entry_vars.append(var)

        def add_room_action():
            for var in entry_vars:
                if var.get() == "":
                    messagebox.showerror("Lỗi", "Không được để trống")
                    return

            new_data = {
                "room": entry_vars[0].get(),
                "name": entry_vars[1].get(),
                "job": entry_vars[2].get(),
                "phone": entry_vars[3].get()
            }

            file_path = "data/list.json"
            if not os.path.exists("data"):
                os.makedirs("data")

            if not os.path.exists(file_path):
                data = []
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = [data]
                    except json.JSONDecodeError:
                        data = []

            data.append(new_data)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            self.load_data()
            messagebox.showinfo("Thông báo", "Thêm thành công", parent=self.window)
            add_room_window.destroy()

        button_frame = tk.Frame(form_frame)
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
          command=add_room_action).pack(fill="x")

    def edit_room(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn một dòng để sửa", parent=self.window)
            return

        current_values = self.tree.item(selected[0], "values")

        edit_window = tk.Toplevel(self.window)
        edit_window.title("✏️ Sửa thông tin phòng")
        edit_window.geometry("300x200")
        edit_window.grab_set()

        self.setup_button_style(edit_window)
        form_frame = ttk.Frame(edit_window, padding=10)
        form_frame.pack(fill="both", expand=True)

        labels = ["Tên phòng:", "Tên thành viên:", "Nghề nghiệp:", "Số điện thoại:"]
        entry_vars = []

        for i, text in enumerate(labels):
            var = tk.StringVar(value=current_values[i])
            ttk.Label(form_frame, text=text, width=15, anchor="w").grid(row=i, column=0, padx=5, pady=5)
            ttk.Entry(form_frame, width=25, textvariable=var).grid(row=i, column=1, padx=2, pady=5)
            entry_vars.append(var)

        def save_edit_action():
            new_values = [var.get() for var in entry_vars]
            if any(v == "" for v in new_values):
                messagebox.showerror("Lỗi", "Không được để trống", parent=edit_window)
                return

            self.tree.item(selected[0], values=new_values)

            file_path = "data/list.json"
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = []

                for d in data:
                    if (d["room"], d["name"], d["job"], d["phone"]) == current_values:
                        d["room"], d["name"], d["job"], d["phone"] = new_values
                        break

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

            self.load_data()
            messagebox.showinfo("Thông báo", "Cập nhật thành công", parent=self.window)
            edit_window.destroy()

        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=len(labels), column=0, columnspan=2, pady=15, sticky="ew")
        tk.Button(button_frame,
          text="💾 Lưu",
          font=("Segoe UI", 11, "bold"),
          bg="#5BC0EB",
          fg="white",
          activebackground="#4299c7",
          relief="flat",
          bd=0,
          padx=10,
          pady=5,
          cursor="hand2",
          command=save_edit_action).pack(fill="x")

    def delete_room(self):
        selected = self.tree.selection()
        selected_list = list(selected)

        if not selected:
            messagebox.showerror("Lỗi", "Vui lòng chọn dòng cần xóa", parent=self.window)
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dòng đã chọn?", parent=self.window)
        if not confirm:
            return
        selected_value = [self.tree.item(item, "values") for item in selected_list]
        for item in selected_list:
            self.tree.delete(item)

        file_path = "data/list.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

            data = [d for d in data if (d["room"], d["name"], d["job"], d["phone"]) not in selected_value]

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
