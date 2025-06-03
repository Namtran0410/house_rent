import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("House rental management system")
        self.root.geometry("1080x720")
        self.root.configure(bg="#f5f5f5")
        self.create_widgets()

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
        pass

    def list_room_people(self):
        from function.list import ListRoomPeople
        list_room_people = ListRoomPeople(self.root)

    def transaction(self):
        from function.transaction import Transaction
        transaction = Transaction(self.root)

    def revenue(self):
        pass

    def setting(self):
        from function.setting import Setting
        setting = Setting(self.root)

    def contact(self):
        pass
if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


