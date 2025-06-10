import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from datetime import datetime
from turtle import color, window_width
from tkcalendar import DateEntry
from collections import defaultdict
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("House rental management system")
        self.root.geometry("1420x960")
        self.root.configure(bg="#f5f5f5")
        self.content_frame = None
        self.create_widgets()
        self.overview()
        

    def create_widgets(self):
        # Create a frame for the main content
        # Tiêu đề
        title = tk.Label(self.root, 
                         text="🏠 Trang chủ", 
                         font=("Helvetica", 24, "bold"),
                         fg="#1a237e"
                         )
        title.pack(pady=10)

        # Tạo các tab 
        # Tab bar
        tab_bar = tk.Frame(root, bg ="#F0F8FF", width = 100)
        tab_bar.pack(side="left", fill="y")
        
        
        # Tab 1: Overview 
        overview_button = tk.Button(tab_bar,
            text="Trang chủ",
            font=("Segoe UI", 11, "bold"),
            bg="#F0F8FF", 
            bd=0,           # ❗ bỏ viền
            relief="flat",  # ❗ không gờ nổi
            fg="#0d47a1",
            activebackground="#d0e8ff",
            activeforeground="black",
            cursor="hand2",
            command=self.overview
        )
        overview_button.pack(anchor="nw", pady=10, padx=5)

        # Tab 2: Danh sách phòng, số người 
        list_button = tk.Button(tab_bar,
            text="Danh sách",
            font=("Segoe UI", 11, "bold"),
            bg="#F0F8FF", 
            bd=0,           # ❗ bỏ viền
            relief="flat",  # ❗ không gờ nổi
            fg="#0d47a1",
            activebackground="#d0e8ff",
            activeforeground="black",
            cursor="hand2",
            command=self.list_room_people
        )
        list_button.pack(anchor="nw", pady=10, padx=5)

        # Tab 3: Giao dịch
        transaction_button = tk.Button(tab_bar,
            text="Giao dịch",
            font=("Segoe UI", 11, "bold"),
            bg="#F0F8FF", 
            bd=0,           # ❗ bỏ viền
            relief="flat",  # ❗ không gờ nổi
            fg="#0d47a1",
            activebackground="#d0e8ff",
            activeforeground="black",
            cursor="hand2",
            command=self.transaction
        )
        transaction_button.pack(anchor="nw", pady=10, padx=5)

        # Tab 4: Doanh thu 
        revenue_button = tk.Button(tab_bar,
            text="Doanh thu",
            font=("Segoe UI", 11, "bold"),
            bg="#F0F8FF", 
            bd=0,           # ❗ bỏ viền
            relief="flat",  # ❗ không gờ nổi
            fg="#0d47a1",
            activebackground="#d0e8ff",
            activeforeground="black",
            cursor="hand2",
            command=self.revenue
        )
        revenue_button.pack(anchor="nw", pady=10, padx=5)

        # Tab 5: Cài đặt
        setting_button = tk.Button(tab_bar,
            text="Cài đặt",
            font=("Segoe UI", 11, "bold"),
            bg="#F0F8FF", 
            bd=0,           # ❗ bỏ viền
            relief="flat",  # ❗ không gờ nổi
            fg="#0d47a1",
            activebackground="#d0e8ff",
            activeforeground="black",
            cursor="hand2",
            command=self.setting
        )
        setting_button.pack(anchor="nw", pady=10, padx=5)

        # Tab 6: Liên hệ
        contact_button = tk.Button(tab_bar,
            text="Thông tin",
            font=("Segoe UI", 11, "bold"),
            bg="#F0F8FF", 
            bd=0,           # ❗ bỏ viền
            relief="flat",  # ❗ không gờ nổi
            fg="#0d47a1",
            activebackground="#d0e8ff",
            activeforeground="black",
            cursor="hand2",
            command=self.contact
        )
        contact_button.pack(anchor="sw", pady=10, padx=5)

    def overview(self):
        # ===== Xoá content cũ (nếu có) =====
        if self.content_frame:
            self.content_frame.destroy()

        # ===== Tạo content mới =====
        self.content_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.content_frame.pack(fill="both", expand=True, side="right")

        # ===== Header chứa nút Reload =====
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        reload_btn = ttk.Button(header_frame, text="🔄 Reload", command=self.reload_overview)
        reload_btn.pack(anchor="e")

        # ===== Khung chứa biểu đồ =====
        chart_frame = ttk.Frame(self.content_frame)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        chart_frame.columnconfigure(0, weight=1)
        chart_frame.columnconfigure(1, weight=1)
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.rowconfigure(1, weight=1)

        # ===== 1. Biểu đồ Bar (Số người/phòng) =====
        room_path = "data/list.json"
        data_room = []
        if os.path.exists(room_path):
            with open(room_path, "r", encoding="utf-8") as f:
                data_room = json.load(f)

        room_count = defaultdict(int)
        for person in data_room:
            room_count[person["room"]] += 1

        rooms = list(room_count.keys())
        counts = list(room_count.values())

        fig_bar = Figure(figsize=(4, 3.5), dpi=100)
        ax_bar = fig_bar.add_subplot(111)
        ax_bar.bar(rooms, counts, color="#5BC0EB")
        ax_bar.set_title("Số người trong mỗi phòng", fontsize=8)
        ax_bar.set_xlabel("Phòng", fontsize=8)
        ax_bar.set_ylabel("Số người", fontsize=8)
        ax_bar.tick_params(axis='x', labelrotation=30, labelsize=7)
        ax_bar.grid(axis="y", linestyle='--', linewidth=0.5)

        canvas_bar = FigureCanvasTkAgg(fig_bar, master=chart_frame)
        canvas_bar.draw()
        canvas_bar.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# ===== 2. Biểu đồ Tròn (Tỉ lệ thanh toán) =====
        revenue_path = "data/transaction.json"
        if not os.path.exists(revenue_path):
            return

        with open(revenue_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        current_year = datetime.now().strftime("%y")
        current_month = datetime.now().month
        paid = unpaid = 0

        for entry in data:
            parts = entry.get("time", "").split("/")
            if len(parts) == 3:
                m, _, y = parts
                if y == current_year and int(m) == current_month:
                    if entry.get("status") == "Đã thanh toán":
                        paid += 1
                    else:
                        unpaid += 1

        fig_pie, ax_pie = plt.subplots(figsize=(4, 3.5))
        wedges, _, autotexts = ax_pie.pie(
            [paid, unpaid], 
            colors=["#4CAF50", "#F44336"], 
            autopct=lambda p: f'{p:.1f}%' if p > 0 else '',  # Chỉ hiển thị % nếu >0
            startangle=90,
            pctdistance=0.5,  # Điều chỉnh % vào giữa các phần
            textprops={'fontsize': 9, 'color': 'white', 'weight': 'bold'}  # Style cho text
        )

        # Điều chỉnh vị trí các text phần trăm
        for text in autotexts:
            text.set_horizontalalignment('center')
            text.set_verticalalignment('center')

        ax_pie.set_title("Tỉ lệ thanh toán tháng này")

        # Thêm legend phía dưới biểu đồ
        ax_pie.legend(
            wedges,
            ["Đã thanh toán", "Chưa thanh toán"],
            loc="lower center",
            bbox_to_anchor=(0.5, -0.15),
            ncol=2
        )

        plt.tight_layout()

        canvas_pie = FigureCanvasTkAgg(fig_pie, master=chart_frame)
        canvas_pie.draw()
        canvas_pie.get_tk_widget().grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        # ===== Label tháng hiện tại =====
        month_frame = tk.Frame(chart_frame, bg="#f5f5f5")
        month_frame.grid(row=1, column=1, pady=(5, 5))

        month_label = tk.Label(
            month_frame, 
            text=f"Tháng hiện tại: {current_month:02d}/{datetime.now().year}", 
            font=("Segoe UI", 9, "italic"), 
            fg="gray", 
            bg="#f5f5f5"
        )
        month_label.pack()


        # ===== 3. Biểu đồ Đường (Doanh thu theo tháng) =====
        monthly_revenue = defaultdict(int)
        for entry in data:
            parts = entry.get("time", "").split("/")
            if len(parts) == 3:
                m, _, y = parts
                if y == current_year:
                    monthly_revenue[int(m)] += int(entry.get("total_fee", 0))

        months = list(range(1, 13))
        revenues = [monthly_revenue.get(m, 0) for m in months]

        fig_line, ax_line = plt.subplots(figsize=(8.5, 4))
        ax_line.plot(months, revenues, marker='o', linestyle='-', color='#2196F3')
        ax_line.set_xticks(months)
        ax_line.set_title("Doanh thu theo tháng")
        ax_line.set_xlabel("Tháng")
        ax_line.set_ylabel("Doanh thu")

        canvas_line = FigureCanvasTkAgg(fig_line, master=chart_frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


    def reload_overview(self):
        self.overview()


    def list_room_people(self):
        from function.list import ListRoomPeople
        list_room_people = ListRoomPeople(self.root)

    def transaction(self):
        from function.transaction import Transaction
        transaction = Transaction(self.root)

    def revenue(self):
        from function.revenue import Revenue
        revenue = Revenue(self.root)

    def setting(self):
        from function.setting import Setting
        setting = Setting(self.root)

    def contact(self):
        pass
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


