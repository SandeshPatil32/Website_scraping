from tkinter import *
from auth.register import Register
from auth.login import Login
from scrap.scanner_ui import ScannerUI


class AppController:

    def __init__(self, root):
        self.root = root
        self.root.withdraw() 

        self.register_win = None
        self.login_win = None
        self.dashboard_win = None

        self.show_register()
        
    def show_register(self):
        self.register_win = Toplevel(self.root)
        self.register_win.title("Register")
        self.register_win.protocol("WM_DELETE_WINDOW", self.root.quit)

        Register(self.register_win, on_success=self.after_register)

    def after_register(self):
        if self.register_win:
            self.register_win.destroy()
        self.show_login()

    def show_login(self):
        self.login_win = Toplevel(self.root)
        self.login_win.title("Login")
        self.login_win.protocol("WM_DELETE_WINDOW", self.root.quit)

        Login(self.login_win, on_success=self.after_login)

    def after_login(self, username):
        self.username = username

        if self.login_win:
            self.login_win.destroy()

        self.show_dashboard() 

    def show_dashboard(self):
        self.dashboard_win = Toplevel(self.root)
        self.dashboard_win.title("Dashboard")
        self.dashboard_win.geometry("850x550")
        self.dashboard_win.config(bg="#E3F2FD")

        Label(
            self.dashboard_win,
            text=f"Welcome, {self.username}",
            font=("Arial", 22, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1",
        ).pack(pady=20)

        Button(
            self.dashboard_win,
            text="Start Scanner",
            font=("Arial", 14, "bold"),
            bg="#0D47A1",
            fg="white",
            command=self.open_scanner,
        ).pack(pady=20)

        Button(
            self.dashboard_win,
            text="Logout",
            font=("Arial", 14, "bold"),
            bg="#B71C1C",
            fg="white",
            command=self.logout,
        ).pack(pady=10)

    def open_scanner(self):
        scan_win = Toplevel(self.dashboard_win)
        scan_win.title("Scanner")
        ScannerUI(scan_win)


    def logout(self):
        if self.dashboard_win:
            self.dashboard_win.destroy()
        self.show_login()

if __name__ == "__main__":
    root = Tk()
    AppController(root)
    root.mainloop()
     
     