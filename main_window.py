import tkinter as tk
from tkinter import messagebox, font
from users import User
from services import authService
from services import mealService
auth_service = authService("dataUser.json")
from services import dataService
from client_window import ClientUI
from admin_window import AdminUI


def handle_login(main):
    main.destroy()
    loginWindow = tk.Tk()
    loginWindow.geometry("400x400")
    loginWindow.title("Cửa sổ đăng nhập")
    loginWindow.configure(bg="#e1eaf7")  # nền xanh nhạt

    title = tk.Label(loginWindow, text="Đăng nhập", font=("Arial", 22, "bold"), bg="#e1eaf7", fg="black")
    title.pack(pady=20)

    form_frame = tk.Frame(loginWindow, bg="#e1eaf7")
    form_frame.pack(pady=10, padx=30, fill='x')

    usernameLabel = tk.Label(form_frame, text="Tên đăng nhập", font=("Arial", 12), bg="#e1eaf7", fg="black")
    usernameLabel.pack(anchor="w", pady=(0, 5))
    usernameEntry = tk.Entry(form_frame, font=("Arial", 12))
    usernameEntry.pack(fill='x', pady=(0, 15))

    passwordLabel = tk.Label(form_frame, text="Mật khẩu", font=("Arial", 12), bg="#e1eaf7", fg="black")
    passwordLabel.pack(anchor="w", pady=(0, 5))
    passwordEntry = tk.Entry(form_frame, show="*", font=("Arial", 12))
    passwordEntry.pack(fill='x', pady=(0, 15))

    def on_login():
        u = usernameEntry.get()
        p = passwordEntry.get()
        user = auth_service.authenticate(u, p)
        if user:
            loginWindow.destroy()
            if user.get_role() == "admin":
                adminui = AdminUI(user)
                adminui.show()
            else:
                ClientUI.clientWindow(user)
        else:
            messagebox.showerror("Đăng nhập thất bại", "Sai tài khoản hoặc mật khẩu")

    login_btn = tk.Button(loginWindow, text="Đăng nhập", command=on_login,
                          bg="#1e3f66", fg="black", font=("Arial", 14, "bold"), relief="raised", bd=3, width=30)
    login_btn.pack(pady=30, ipady=8)

    loginWindow.mainloop()


def handle_register(main):
    main.destroy()
    rg = tk.Tk()
    rg.geometry("400x500")
    rg.title("Cửa sổ đăng ký tài khoản")
    rg.configure(bg="#e1eaf7")  # nền xanh nhạt

    title = tk.Label(rg, text="Đăng ký tài khoản", font=("Arial", 22, "bold"), bg="#e1eaf7", fg="black")
    title.pack(pady=20)

    form_frame = tk.Frame(rg, bg="#e1eaf7")
    form_frame.pack(pady=10, padx=30, fill='x')

    usernameLabel = tk.Label(form_frame, text="Tên đăng nhập", font=("Arial", 12), bg="#e1eaf7", fg="black")
    usernameLabel.pack(anchor="w", pady=(0, 5))
    usernameEntry = tk.Entry(form_frame, font=("Arial", 12))
    usernameEntry.pack(fill='x', pady=(0, 15))

    passwordLabel = tk.Label(form_frame, text="Mật khẩu", font=("Arial", 12), bg="#e1eaf7", fg="black")
    passwordLabel.pack(anchor="w", pady=(0, 5))
    passwordEntry = tk.Entry(form_frame, show="*", font=("Arial", 12))
    passwordEntry.pack(fill='x', pady=(0, 15))

    cfpasswordLabel = tk.Label(form_frame, text="Xác nhận mật khẩu", font=("Arial", 12), bg="#e1eaf7", fg="black")
    cfpasswordLabel.pack(anchor="w", pady=(0, 5))
    cfpasswordEntry = tk.Entry(form_frame, show="*", font=("Arial", 12))
    cfpasswordEntry.pack(fill='x', pady=(0, 15))

    def on_register():
        u = usernameEntry.get()
        p = passwordEntry.get()
        cfp = cfpasswordEntry.get()
        if not u or not p:
            messagebox.showerror("Lỗi", "Không được để trống trường nào cả!")
        elif p != cfp:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận phải trùng với mật khẩu")
        else:
            user = auth_service.registerAuthenticate(u, p)
            if user is None:
                messagebox.showerror("Thất bại", "Tên tài khoản đã tồn tại")
            else:
                dataService.save_data("dataUser.json", user.to_dict())
                messagebox.showinfo("Thành công", "Đăng ký thành công, hãy đăng nhập")
                rg.destroy()
                show_main_window()

    register_btn = tk.Button(rg, text="Đăng ký", command=on_register,
                             bg="#1e3f66", fg="black", font=("Arial", 14, "bold"), relief="raised", bd=3, width=30)
    register_btn.pack(pady=30, ipady=8)

    rg.mainloop()


def show_main_window():
    main = tk.Tk()
    main.title("Ứng dụng quản lý bữa ăn")
    main.geometry("400x300")
    main.configure(bg="#e1eaf7")  # nền xanh nhạt

    title = tk.Label(main, text="Chào mừng bạn!", font=("Arial", 24, "bold"), bg="#e1eaf7", fg="black")
    title.pack(pady=30)

    login_btn = tk.Button(main, text="Đăng nhập", command=lambda: handle_login(main),
                          bg="#1e3f66", fg="black", font=("Arial", 16, "bold"), relief="raised", bd=3, width=30)
    login_btn.pack(pady=10, ipady=8)

    register_btn = tk.Button(main, text="Đăng ký nếu chưa có tài khoản", command=lambda: handle_register(main),
                             bg="#1e3f66", fg="black", font=("Arial", 16, "bold"), relief="raised", bd=3, width=30)
    register_btn.pack(pady=10, ipady=8)

    main.mainloop()

show_main_window()
