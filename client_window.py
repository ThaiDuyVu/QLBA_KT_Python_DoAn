import tkinter as tk
from tkinter import messagebox
from users import User
from services import authService
from services import mealService
from services import dataService
from datetime import datetime
from tkinter import ttk
from crawl import get_weather
import random
weather = get_weather("Ho_Chi_Minh")
auth_service = authService("dataUser.json")
class ClientUI :
    @staticmethod
    def get_thoi_tiet() :
        wth = weather

        if ("🌧️" in wth) or ("🌦️" in wth) or ("☔" in wth) or ("rain" in wth.lower()) or ("mưa" in wth.lower()):
            thoitiet = "rain"
        elif ("☀️" in wth) or ("nắng" in wth.lower()) or ("sun" in wth.lower()):
            thoitiet = "sunny"
        elif ("⛅" in wth) or ("mây" in wth.lower()) or ("cloud" in wth.lower()):
            thoitiet = "cloudy"
        elif any(x in wth for x in ["❄️", "snow", "tuyết"]):
            thoitiet = "snow"
        elif any(x in wth for x in ["⚡", "thunder", "storm"]):
            thoitiet = "storm"
        elif any(x in wth for x in ["🌫️", "fog", "sương mù"]):
            thoitiet = "fog"
        else :
            return "unknow"
    @staticmethod
    def hint_meal(parent_window, thoitiet) : 
        if hasattr(parent_window, 'hint_label'):
            parent_window.hint_label.destroy()
        mon_kho = ["Cơm tấm", "Mì xào", "Cơm chiên", "Bánh mì ốp la", "Cơm gà"]
        mon_nuoc = ["Bún bò", "Phở", "Bún riêu", "Mì nước", "Hủ tiếu"]
        mon_cay = ["Mì cay Hàn Quốc", "Gà nướng muối ớt", "Lẩu Thái", "Bún bò Huế", "Cơm trộn cay"]
        if thoitiet == "rain" or thoitiet == "snow" or thoitiet == "storm":
            goi_y = random.choice(mon_cay) 
        elif thoitiet == "cloudy" :
            goi_y = random.choice(mon_nuoc)
        else :
            goi_y = random.choice(mon_kho) 
        return goi_y 
    @staticmethod
    def delete_meal(parent_window, filePath):
        if hasattr(parent_window, 'meal_form_frame'):
            parent_window.meal_form_frame.destroy()

        form_frame = tk.Frame(parent_window, bg="#fff0e6", bd=2, relief="groove")
        form_frame.place(relx=0.5, rely=0.55, anchor="n")
        parent_window.meal_form_frame = form_frame

        meals = dataService.load_data(filePath)
        if not meals:
            messagebox.showwarning("Lỗi dữ liệu", "Không có dữ liệu để xoá.")
            return

        times = [meal.get("time", "Không rõ thời gian") for meal in meals]

        title = tk.Label(form_frame, text="🗑️ Xoá món ăn", font=("Arial", 14, "bold"), bg="#fff0e6", fg="black")
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        tk.Label(form_frame, text="Chọn ngày - giờ bạn muốn xoá:", bg="#fff0e6", fg="black").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        combo = ttk.Combobox(form_frame, values=times, state="readonly", width=30)
        combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        fields = {
            "main_dish": "Món chính",
            "side_dish": "Món phụ",
            "third_dish": "Món thêm",
            "soub": "Súp (Canh)",
            "dessert": "Tráng miệng",
            "carbo": "Tinh bột chính"
        }

        check_vars = {}
        label_vars = {}

        for i, (key, label_text) in enumerate(fields.items(), start=2):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(form_frame, text=label_text, variable=var, bg="#fff0e6", fg="black", selectcolor="#d9d9d9")
            chk.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            check_vars[key] = var

            lbl = tk.Label(form_frame, text="", bg="#fff0e6", fg="gray", anchor="w")
            lbl.grid(row=i, column=1, sticky="w", padx=5)
            label_vars[key] = lbl

            def toggle_label(k=key, v=var):
                idx = combo.current()
                if idx >= 0 and v.get():
                    val = meals[idx].get(k, "")
                    label_vars[k].config(text=f"=> {val}")
                else:
                    label_vars[k].config(text="")

            var.trace_add("write", lambda *args, k=key, v=var: toggle_label(k, v))

        def load_selected_meal(event=None):
            idx = combo.current()
            if idx < 0:
                return
            for key in fields:
                check_vars[key].set(False)
                label_vars[key].config(text="")

        combo.bind("<<ComboboxSelected>>", load_selected_meal)

        def confirm_delete():
            idx = combo.current()
            if idx < 0:
                messagebox.showwarning("Chưa chọn ngày", "Vui lòng chọn ngày để xoá món.")
                return
            selected_meal = meals[idx]
            deleted = False
            for key, var in check_vars.items():
                if var.get() and key in selected_meal:
                    selected_meal[key] = ""
                    deleted = True
            if not deleted:
                messagebox.showinfo("Không có thao tác", "Bạn chưa chọn món nào để xoá.")
                return
            meals[idx] = selected_meal
            dataService.save_data_write(filePath, meals)
            messagebox.showinfo("Thành công", "Đã xoá các món được chọn.")
            form_frame.destroy()

        def delete_all():
            idx = combo.current()
            if idx < 0:
                messagebox.showwarning("Chưa chọn ngày", "Vui lòng chọn ngày để xoá cả bữa.")
                return
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xoá toàn bộ bữa ăn này?")
            if confirm:
                del meals[idx]
                dataService.save_data_write(filePath, meals)
                messagebox.showinfo("Thành công", "Đã xoá toàn bộ bữa ăn.")
                form_frame.destroy()

        def cancel():
            form_frame.destroy()

        btn_frame = tk.Frame(form_frame, bg="#fff0e6")
        btn_frame.grid(row=len(fields) + 2, column=0, columnspan=2, pady=15)

        btn_confirm = tk.Button(btn_frame, text="🗑️ Xác nhận xoá món đã chọn", command=confirm_delete, bg="#4caf50", fg="black", padx=10)
        btn_confirm.pack(side="left", padx=5)

        btn_delete_all = tk.Button(btn_frame, text="❌ Xoá cả bữa ăn", command=delete_all, bg="#f44336", fg="black", padx=10)
        btn_delete_all.pack(side="left", padx=5)

        btn_cancel = tk.Button(btn_frame, text="🚪 Thoát", command=cancel, bg="#9e9e9e", fg="black", padx=10)
        btn_cancel.pack(side="left", padx=5)
    @staticmethod
    def update_meal(parent_window, filePath):
        if hasattr(parent_window, 'meal_form_frame'):
            parent_window.meal_form_frame.destroy()

        form_frame = tk.Frame(parent_window, bg="#fff0e6", bd=2, relief="groove")
        form_frame.place(relx=0.5, rely=0.55, anchor="n")
        parent_window.meal_form_frame = form_frame

        meals = dataService.load_data(filePath)
        if not meals:
            messagebox.showwarning("Lỗi dữ liệu", "Không có dữ liệu để sửa")
            return

        times = [meal.get("time", "Không rõ thời gian") for meal in meals]

        title = tk.Label(form_frame, text="✏️ Cập nhật món ăn", font=("Arial", 14, "bold"), bg="#fff0e6", fg="black")
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        tk.Label(form_frame, text="Chọn ngày để sửa món ăn:", bg="#fff0e6", fg="black").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        combo = ttk.Combobox(form_frame, values=times, state="readonly", width=30)
        combo.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        fields = {
            "main_dish": "Món chính",
            "side_dish": "Món phụ",
            "third_dish": "Món thêm",
            "soub": "Súp (Canh)",
            "dessert": "Tráng miệng",
            "carbo": "Tinh bột chính"
        }

        check_vars = {}
        entries = {}

        for i, (key, label_text) in enumerate(fields.items(), start=2):
            var = tk.BooleanVar()
            chk = tk.Checkbutton(form_frame, text=label_text, variable=var, bg="#fff0e6", fg="black", selectcolor="#d9d9d9")
            chk.grid(row=i, column=0, sticky="w", padx=5, pady=2)
            check_vars[key] = var

            entry = tk.Entry(form_frame, width=40, state="disabled")
            entry.grid(row=i, column=1, pady=2, padx=5)
            entries[key] = entry

            def toggle_entry(e=entry, v=var):
                e.config(state="normal" if v.get() else "disabled")
            var.trace_add("write", lambda *args, e=entry, v=var: toggle_entry(e, v))

        def load_selected_meal(event=None):
            idx = combo.current()
            if idx < 0:
                return
            selected_meal = meals[idx]
            for key in fields:
                entries[key].delete(0, tk.END)
                entries[key].insert(0, selected_meal.get(key, ""))
                entries[key].config(state="disabled")
                check_vars[key].set(False)

        combo.bind("<<ComboboxSelected>>", load_selected_meal)

        def save_changes():
            idx = combo.current()
            if idx < 0:
                messagebox.showwarning("Chưa chọn ngày", "Vui lòng chọn ngày để sửa món.")
                return

            selected_meal = meals[idx]
            updated_meal = selected_meal.copy()

            changed = False
            for key in fields:
                if check_vars[key].get():
                    new_val = entries[key].get().strip()
                    updated_meal[key] = new_val
                    changed = True

            if not changed:
                messagebox.showwarning("Không có thay đổi", "Bạn chưa chọn mục nào để sửa.")
                return

            meals[idx] = updated_meal
            dataService.save_data_write(filePath, meals)

            messagebox.showinfo("Thành công", "Đã cập nhật món ăn.")
            form_frame.destroy()

        btn_frame = tk.Frame(form_frame, bg="#fff0e6")
        btn_frame.grid(row=len(fields) + 2, column=0, columnspan=2, pady=15)

        btn_save = tk.Button(btn_frame, text="💾 Lưu thay đổi", command=save_changes, bg="#4caf50", fg="black", padx=10)
        btn_save.pack(side="left", padx=5)

        btn_close = tk.Button(btn_frame, text="❌ Đóng", command=form_frame.destroy, bg="#f44336", fg="black", padx=10)
        btn_close.pack(side="left", padx=5)
    @staticmethod
    def create_meal(parent_window, filePath):
        if hasattr(parent_window, 'meal_form_frame'):
            parent_window.meal_form_frame.destroy()

        form_frame = tk.Frame(parent_window, bg="#fff0e6", bd=2, relief="groove")
        form_frame.place(relx=0.5, rely=0.55, anchor="n")  # căn giữa theo chiều ngang, xuất hiện phía dưới các nút
        parent_window.meal_form_frame = form_frame

        fields = {
            "main_dish": "🍱 Món chính",
            "side_dish": "🥗 Món phụ",
            "third_dish": "🍤 Món thêm",
            "soub": "🥣 Súp (Canh)",
            "dessert": "🍰 Tráng miệng",
            "carbo": "🍚 Tinh bột chính"
        }

        entries = {}

        title = tk.Label(form_frame, text="➕ Nhập món ăn cho hôm nay", font=("Arial", 14, "bold"), bg="#fff0e6", fg="black")
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15))

        for i, (key, label_text) in enumerate(fields.items(), start=1):
            label = tk.Label(form_frame, text=label_text + ":", bg="#fff0e6", fg="black", anchor="w")
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, pady=2)
            entries[key] = entry

        def confirm_add():
            meal_data = {key: entries[key].get().strip() for key in fields}
            meal_data["time"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if not meal_data["main_dish"]:
                messagebox.showwarning("Thiếu thông tin", "Món chính không được để trống!")
                return

            dataService.save_data(filePath, meal_data)
            messagebox.showinfo("Thành công", "Đã thêm bữa ăn thành công!")
            form_frame.destroy()

        def out():
            form_frame.destroy()

        btn_frame = tk.Frame(form_frame, bg="#fff0e6")
        btn_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=15)

        btn_confirm = tk.Button(btn_frame, text="✅ Xác nhận thêm", command=confirm_add, bg="#4caf50", fg="black", padx=10)
        btn_confirm.pack(side="left", padx=5)

        btn_out = tk.Button(btn_frame, text="❌ Thoát", command=out, bg="#f44336", fg="black", padx=10)
        btn_out.pack(side="left", padx=5)
    @staticmethod
    def xem_lich_su(filePath):
        hsWindow = tk.Toplevel()
        hsWindow.title("Lịch sử bữa ăn của bạn")
        hsWindow.geometry("1200x600")
        hsWindow.config(bg="#fff0e6")

        columns = ["main_dish", "side_dish", "third_dish", "soub", "dessert", "carbo", "time"]
        headers = {
            "main_dish": "Món chính",
            "side_dish": "Món phụ",
            "third_dish": "Món thứ 3",
            "soub": "Súp",
            "dessert": "Tráng miệng",
            "carbo": "Tinh bột chính",
            "time": "Thời gian"
        }

        title = tk.Label(hsWindow, text="📜 Lịch sử bữa ăn của bạn", font=("Arial", 16, "bold"), bg="#fff0e6", fg="black")
        title.pack(pady=(15, 10))

        tree_frame = tk.Frame(hsWindow, bg="#fff0e6")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)

        # Thiết lập tiêu đề và cột
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=140 if col != "time" else 180, anchor=tk.CENTER)

        # Thêm thanh cuộn dọc
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)

        lich_su = dataService.load_data(filePath)
        if lich_su:
            for bua_an in lich_su:
                tree.insert('', tk.END, values=(
                    bua_an.get("main_dish", ""), bua_an.get("side_dish", ""), bua_an.get("third_dish", ""),
                    bua_an.get("soub", ""), bua_an.get("dessert", ""), bua_an.get("carbo", ""),
                    bua_an.get("time", "")
                    ))
        else:
            messagebox.showinfo("Thông báo", "Chưa có dữ liệu bữa ăn nào.")
        btn_frame = tk.Frame(hsWindow, bg="#fff0e6")
        btn_frame.pack(pady=10)

        btn_close = tk.Button(btn_frame, text="🚪 Đóng", command=hsWindow.destroy, bg="#9e9e9e", fg="black", padx=15, pady=6)
        btn_close.pack()
    @staticmethod
    def clientWindow(user):
        clWindow = tk.Tk()
        clWindow.title("🍽️ Quản lý bữa ăn của bạn")
        clWindow.geometry("1200x700")
        clWindow.configure(bg="#fff8e1")

        dataFilePath = mealService.get_user_meal_file(user.get_username())

        main_frame = tk.Frame(clWindow, bg="#fff8e1")
        main_frame.pack(fill='both', expand=True)

        # Cấu hình cột để giãn đều
        for col in range(3):
            main_frame.columnconfigure(col, weight=1)

        # --- HEADER ---
        header_frame = tk.Frame(main_frame, bg="#fff8e1")
        header_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        tk.Label(header_frame, text=f"👤 Tên: {user.get_username()}",
                 font=("Arial", 12, "bold"), bg="#fff8e1", fg="#4e342e").pack(side='left', padx=10)

        ngay_hien_tai = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tk.Label(header_frame, text=f"📅 {ngay_hien_tai}",
                 font=("Arial", 12), bg="#fff8e1", fg="#4e342e").pack(side='right', padx=10)

        # --- THỜI TIẾT ---
        tk.Label(main_frame, text=f"🌤️ Thời tiết hôm nay: {weather}",
                 font=("Arial", 12, "italic"), bg="#fff8e1", fg="#6d4c41").grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # --- MENU ---
        menu_bar = tk.Menu(clWindow)
        clWindow.config(menu=menu_bar)

        chuc_nang_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Chức năng", menu=chuc_nang_menu)

        chuc_nang_menu.add_command(label="Xem lịch sử bữa ăn", command=lambda: ClientUI.xem_lich_su(dataFilePath))
        chuc_nang_menu.add_command(label="Thêm món ăn", command=lambda: ClientUI.create_meal(main_frame, dataFilePath))
        chuc_nang_menu.add_command(label="Xóa món ăn", command=lambda: ClientUI.delete_meal(main_frame, dataFilePath))
        chuc_nang_menu.add_command(label="Cập nhật (chỉnh sửa) món ăn", command=lambda: ClientUI.update_meal(main_frame, dataFilePath))
        chuc_nang_menu.add_separator()
        chuc_nang_menu.add_command(label="Thoát", command=clWindow.destroy)

        # --- STYLE NÚT ---
        btn_style = {
            "font": ("Arial", 12, "bold"),
            "bg": "#ffcc80",
            "fg": "#4e342e",
            "width": 25,
            "height": 2,
            "relief": "raised",
            "bd": 2
        }

        # --- BUTTONS CHÍNH ---
        tk.Button(main_frame, text="🍲 Thêm món ăn hôm nay",
                  command=lambda: ClientUI.create_meal(main_frame, dataFilePath), **btn_style).grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        tk.Button(main_frame, text="📜 Xem lịch sử món ăn",
                  command=lambda: ClientUI.xem_lich_su(dataFilePath), **btn_style).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        tk.Button(main_frame, text="✏️ Chỉnh sửa món ăn",
                  command=lambda: ClientUI.update_meal(main_frame, dataFilePath), **btn_style).grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        tk.Button(main_frame, text="🗑️ Xoá món ăn",
                  command=lambda: ClientUI.delete_meal(main_frame, dataFilePath), **btn_style).grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # --- NÚT GỢI Ý MÓN ĂN ---
        def handle_hint():
            goi_y = ClientUI.hint_meal(main_frame, ClientUI.get_thoi_tiet())
            hint_label.config(text=f"💡 Gợi ý hôm nay: thời tiết {weather} bạn hãy thử ăn : {goi_y} sẽ thấy ngon hơn")

        tk.Button(main_frame, text="🌟 Gợi ý món ăn hôm nay",
                  command=handle_hint, **btn_style).grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")

        # --- NHÃN GỢI Ý MÓN ĂN (để trống ban đầu) ---
        hint_label = tk.Label(main_frame, text="",
                              font=("Arial", 12, "italic"),
                              bg="#fff3e0", fg="#6d4c41",
                              wraplength=600, justify="left")
        hint_label.grid(row=5, column=0, columnspan=3, pady=(20, 5), padx=10, sticky="w")

        clWindow.mainloop()
