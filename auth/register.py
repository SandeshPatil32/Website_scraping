from tkinter import *
from tkinter import messagebox
import hashlib
import os
from pymongo import MongoClient
from auth.login import Login


class Register:
    def __init__(self, master, on_success=None):
        self.master = master
        self.master.title("Create Account")
        self.master.geometry("500x630")
        self.master.config(bg="#E3F2FD")
        self.on_success = on_success

        Label(
            self.master,
            text="Create Your Account",
            font=("Arial", 20, "bold"),
            bg="#E3F2FD",
            fg="#0D47A1",
        ).pack(pady=20)

        self.frame = Frame(self.master, bg="white", bd=2, relief="ridge")
        self.frame.pack(pady=10, padx=20, fill=BOTH)

        self.make_input("First Name", "fname")
        self.make_input("Last Name", "lname")
        self.make_input("Email", "email")
        self.make_input("Username", "uname")
        self.make_input("Password", "pw", hide=True)

        Button(
            self.master,
            text="Register",
            width=20,
            font=("Arial", 12),
            bg="#0D47A1",
            fg="white",
            command=self.submit,
        ).pack(pady=20)

        Button(
            self.master,
            text="Login",
            width=20,
            font=("Arial", 12),
            bg="#0D47A1",
            fg="white",
            command = self.login
        ).pack(pady=20)
        
    def login(self):
        self.master.destroy()
        root = Tk()
        Login(root)
        root.mainloop()
        
    def make_input(self, label, key, hide=False):
        Label(
            self.frame, text=label, bg="white", fg="#0D47A1", font=("Arial", 11, "bold")
        ).pack(pady=(15, 0))

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

    def submit(self):
        fname = self.fname.get().strip()
        lname = self.lname.get().strip()
        email = self.email.get().strip()
        uname = self.uname.get().strip()
        pw = self.pw.get()

        if not all([fname, lname, email, uname, pw]):
            messagebox.showerror("Error", "All fields are required")
            return

        if "@" not in email:
            messagebox.showerror("Error", "Invalid email address")
            return

        if len(pw) < 6:
            messagebox.showerror("Error", "Password should be 6+ chars")
            return

        hashed_pw = hashlib.sha256((uname + pw).encode()).hexdigest()

        db = MongoClient(os.getenv("MONGODB_URI"))["website_scan"]

        if db.users.find_one({"username": uname}):
            messagebox.showerror("Error", "Username already exists")
            return

        db.users.insert_one(
            {
                "fname": fname,
                "lname": lname,
                "email": email,
                "username": uname,
                "password": hashed_pw,
            }
        )

        messagebox.showinfo("Success", "Registration Complete")

        if self.on_success:
            self.on_success()

        self.master.destroy()


""" if __name__ == "__main__":
    root = Tk()
    Register(root)
    root.mainloop()
 """
