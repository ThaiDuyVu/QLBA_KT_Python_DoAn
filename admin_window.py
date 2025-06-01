import tkinter as tk
from tkinter import messagebox, ttk
from users import User
from services import dataService

class AdminUI:
    def __init__(self, user, user_file="dataUser.json"):
        self.user = user
        self.user_file = user_file
        self.users = self.load_users()

    def load_users(self):
        data = dataService.load_data(self.user_file)
        return [User.from_dict(u) for u in data]

    def save_users(self):
        data = [u.to_dict() for u in self.users]
        dataService.save_data_write(self.user_file, data)

    def show_user_list(self):
        win = tk.Toplevel()
        win.title("Danh sách tài khoản")
        win.geometry("400x300")

        cols = ("username", "role")
        tree = ttk.Treeview(win, columns=cols, show="headings")
        tree.heading("username", text="Tên đăng nhập")
        tree.heading("role", text="Quyền")

        for u in self.users:
            tree.insert("", tk.END, values=(u.get_username(), u.get_role()))
        tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(win, text="Đóng", command=win.destroy).pack(pady=5)

    def edit_user_info(self):
        win = tk.Toplevel()
        win.title("Thay đổi thông tin tài khoản")
        win.geometry("350x250")

        tk.Label(win, text="Chọn tài khoản:").pack(pady=5)
        usernames = [u.get_username() for u in self.users]
        combo = ttk.Combobox(win, values=usernames, state="readonly")
        combo.pack(pady=5)

        entry_username = tk.Entry(win)
        entry_password = tk.Entry(win, show="*")
        entry_role = tk.Entry(win)

        for label, entry in [("Tên đăng nhập mới:", entry_username),
                             ("Mật khẩu mới:", entry_password),
                             ("Quyền (admin/client):", entry_role)]:
            tk.Label(win, text=label).pack(pady=5)
            entry.pack(pady=5)

        def load_user_info(event=None):
            sel = combo.get()
            for u in self.users:
                if u.get_username() == sel:
                    entry_username.delete(0, tk.END)
                    entry_username.insert(0, u.get_username())
                    entry_password.delete(0, tk.END)
                    entry_password.insert(0, u.get_password())
                    entry_role.delete(0, tk.END)
                    entry_role.insert(0, u.get_role())
        combo.bind("<<ComboboxSelected>>", load_user_info)

        def save_changes():
            sel = combo.get()
            if not sel:
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn tài khoản để sửa")
                return

            new_username = entry_username.get().strip()
            new_password = entry_password.get().strip()
            new_role = entry_role.get().strip()

            if not new_username or not new_password or not new_role:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin")
                return

            for u in self.users:
                if u.get_username() == new_username and u.get_username() != sel:
                    messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại")
                    return

            for u in self.users:
                if u.get_username() == sel:
                    u.set_username(new_username)
                    u.set_password(new_password)
                    u.set_role(new_role)
                    break

            self.save_users()
            messagebox.showinfo("Thành công", "Đã cập nhật thông tin tài khoản")
            win.destroy()

        tk.Button(win, text="Lưu thay đổi", command=save_changes).pack(pady=10)

    def delete_user(self):
        win = tk.Toplevel()
        win.title("Xoá tài khoản người dùng")
        win.geometry("300x200")

        tk.Label(win, text="Chọn tài khoản cần xoá:").pack(pady=10)
        usernames = [u.get_username() for u in self.users]
        combo = ttk.Combobox(win, values=usernames, state="readonly")
        combo.pack(pady=10)

        def confirm_delete():
            sel = combo.get()
            if not sel:
                messagebox.showwarning("Chưa chọn", "Vui lòng chọn tài khoản để xoá")
                return

            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá '{sel}'?")
            if not confirm:
                return

            for u in self.users:
                if u.get_username() == sel and u.get_role() == "admin":
                    messagebox.showerror("Lỗi", "Không được xoá tài khoản admin!")
                    return

            self.users = [u for u in self.users if u.get_username() != sel]
            self.save_users()
            messagebox.showinfo("Thành công", "Đã xoá tài khoản")
            win.destroy()

        tk.Button(win, text="Xoá tài khoản", fg="red", command=confirm_delete).pack(pady=10)

    def show(self):
        root = tk.Tk()
        root.title("Quản trị viên")
        root.geometry("400x300")

        tk.Label(root, text=f"Xin chào Admin {self.user.get_username()}!", font=("Arial", 16)).pack(pady=20)
        tk.Button(root, text="1. Hiển thị danh sách tài khoản", width=30, command=self.show_user_list).pack(pady=5)
        tk.Button(root, text="2. Thay đổi thông tin tài khoản", width=30, command=self.edit_user_info).pack(pady=5)
        tk.Button(root, text="3. Xoá tài khoản người dùng", width=30, command=self.delete_user).pack(pady=5)

        root.mainloop()
