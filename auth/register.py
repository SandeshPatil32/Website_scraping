from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient
from scraping.website_scan import WebsiteScanner
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "website_scan"


def get_database():
    client = MongoClient(MONGODB_URI)
    return client[DB_NAME], client


class Register:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x500")
        self.master.config(bg="azure")

        f = Frame(self.master, bg="azure", relief="ridge", bd=20)
        f.pack(fill=BOTH, expand=True)

        Label(f, text="Register Yourself", bg="azure", font=("Arial", 25, "bold")).pack(
            pady=10
        )

        Label(f, text="First Name:", bg="azure").pack()
        self.tname = Entry(f, width=30)
        self.tname.pack()

        Label(f, text="Last Name:", bg="azure").pack()
        self.tlname = Entry(f, width=30)
        self.tlname.pack()

        Label(f, text="Email ID:", bg="azure").pack()
        self.temail = Entry(f, width=30)
        self.temail.pack()

        Label(f, text="Username:", bg="azure").pack()
        self.tuname = Entry(f, width=30)
        self.tuname.pack()

        Label(f, text="Enter Password:", bg="azure").pack()
        self.tpw = Entry(f, width=30, show="*")
        self.tpw.pack()

        self.var = IntVar()
        Checkbutton(
            f,
            text="Show Password",
            bg="azure",
            command=self.Showpassword,
            variable=self.var,
        ).pack()

        Button(
            f,
            text="Submit",
            width=20,
            height=2,
            bg="lavender",
            command=self.submit,
        ).pack(pady=20)

    def Showpassword(self):
        self.tpw.config(show="" if self.var.get() else "*")

    def submit(self):
        name = self.tname.get().strip()
        lname = self.tlname.get().strip()
        email = self.temail.get().strip()
        uname = self.tuname.get().strip()
        pw = self.tpw.get()

        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Enter valid email")
            return

        if len(pw) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters")
            return

        if not uname.strip():
            messagebox.showerror("Error", "Username is required")
            return

        hashed = hashlib.sha1((uname[:5] + pw).encode("utf-8")).hexdigest()

        db, client = get_database()
        try:
            if db["account"].find_one({"uname": uname}):
                messagebox.showwarning("Warning", "Username already exists")
                return

            db["account"].insert_one(
                {
                    "name": name,
                    "lname": lname,
                    "email": email,
                    "uname": uname,
                    "p": hashed,
                }
            )

            messagebox.showinfo("Success", "Registration Completed!")
            self.master.destroy()

        finally:
            client.close()
