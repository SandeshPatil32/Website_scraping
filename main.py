from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from scraping.website_scan import WebsiteScanner
from auth.register import Register
from auth.login import Login


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.geometry("700x500")
        self.master.title("Website Scanning")
        self.master.config(bg="#64C9DD")

        f = Frame(self.master, bg="azure", relief="ridge", bd=20)
        f.pack(fill=BOTH, expand=True)

        Label(
            f,
            text="The Website Scanning Tool",
            fg="blue",
            bg="azure",
            font=("Arial", 30, "bold italic"),
        ).pack(pady=50)

        Button(
            f,
            text="Register Account",
            width=20,
            height=3,
            fg="royalblue4",
            bg="azure",
            font=("Arial", 10, "bold italic"),
            command=self.reg,
        ).pack(pady=20)

        Button(
            f,
            text="Login Account",
            width=20,
            height=3,
            fg="royalblue4",
            bg="azure",
            font=("Arial", 10, "bold italic"),
            command=self.login,
        ).pack(pady=10)

    def reg(self):
        Register(Toplevel(self.master))

    def login(self):
        Login(Toplevel(self.master))

if __name__ == "__main__":
    root = Tk()
    root.resizable(0, 0)
    MainWindow(root)
    root.mainloop()
