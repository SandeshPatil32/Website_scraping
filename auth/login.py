from tkinter import *
from tkinter import messagebox
import hashlib
import os
from pymongo import MongoClient

class Login:
    def __init__(self, master, on_success=None):
        self.master = master
        self.master.title("Login")
        self.master.geometry("420x450")
        self.master.config(bg="#E3F2FD")
        self.on_success = on_success

        Label(
            self.master,
            text="Welcome Back",
            font=("Arial", 22, "bold"),
            bg="#E3F2FD", 
            fg="#0D47A1",
        ).pack(pady=20)

        self.frame = Frame(self.master, bg="white", bd=2, relief="ridge")
        self.frame.pack(pady=10, padx=20, fill=BOTH)

        self.make_input("Username", "uname")
        self.make_input("Password", "pw", hide=True)

        Button(
            self.master,
            text="Login",
            width=20,
            font=("Arial", 12),
            bg="#0D47A1",
            fg="white",
            command=self.login,
        ).pack(pady=20)

    def make_input(self, label, key, hide=False):
        Label(
            self.frame, text=label, bg="white", fg="#0D47A1", font=("Arial", 11, "bold")
        ).pack(pady=(20, 0))

        entry = Entry(
            self.frame,
            width=30,
            show="*" if hide else "",
            bd=2,
            relief="groove",
            font=("Arial", 12),
        )
        entry.pack(pady=5)

        setattr(self, key, entry)

    def login(self):
        uname = self.uname.get().strip()
        pw = self.pw.get()

        hashed_pw = hashlib.sha256((uname + pw).encode()).hexdigest()

        db = MongoClient(os.getenv("MONGODB_URI"))["website_scan"]
        user = db.users.find_one({"username": uname, "password": hashed_pw})

        if user:
            messagebox.showinfo("Success", "Login Successful")

            if self.on_success:
                self.on_success(uname)

            self.master.destroy()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

