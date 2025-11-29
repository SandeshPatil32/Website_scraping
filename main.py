from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient
from website_scan import WebsiteScanner
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = "website_scan"


def get_database():
    client = MongoClient(MONGODB_URI)
    return client[DB_NAME], client


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


class Login:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x300")
        self.master.config(bg="azure")

        f = Frame(self.master, bg="azure", relief="ridge", bd=20)
        f.pack(fill=BOTH, expand=True)

        Label(f, text="Enter Username:", bg="azure").pack(pady=10)
        self.e1 = Entry(f, width=30)
        self.e1.pack()

        Label(f, text="Enter Password:", bg="azure").pack(pady=10)
        self.e2 = Entry(f, width=30, show="*")
        self.e2.pack()

        self.var = IntVar()
        Checkbutton(
            f,
            text="Show Password",
            bg="azure",
            variable=self.var,
            command=self.Showpassword,
        ).pack()

        Button(f, text="Login", width=15, bg="lavender", command=self.clicked).pack(
            pady=15
        )

    def Showpassword(self):
        self.e2.config(show="" if self.var.get() else "*")

    def clicked(self):
        u = self.e1.get().strip()
        pw = self.e2.get()
        hashed = hashlib.sha1((u[:5] + pw).encode("utf-8")).hexdigest()

        db, client = get_database()
        try:
            result = db["account"].find_one({"uname": u, "p": hashed})
        finally:
            client.close()

        if result:
            Account(Toplevel(self.master), u)
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


class Account:
    def __init__(self, master, u):
        self.u = u
        self.master = master
        self.master.geometry("600x400")
        self.master.config(bg="#009FBF")

        f = Frame(self.master, bg="azure", relief="ridge", bd=20)
        f.pack(fill=BOTH, expand=True)

        Label(f, text=f"Welcome {self.u}", bg="azure", font=("Arial", 20)).pack(pady=30)

        Button(
            f,
            text="Scan Website",
            width=20,
            height=2,
            bg="lavender",
            command=self.website_ws,
        ).pack(pady=20)

        Button(
            f,
            text="Logout",
            width=20,
            height=2,
            bg="lavender",
            command=self.master.destroy,
        ).pack()

    def website_ws(self):
        Scanner(Toplevel(self.master))


class Scanner:
    def __init__(self, master):
        self.master = master
        self.master.geometry("900x600")
        self.master.config(bg="azure")

        f = Frame(self.master, bg="azure", relief="ridge", bd=20)
        f.pack(fill=BOTH, expand=True)

        Label(f, text="Website Scanning", font=("Arial", 22), bg="azure").pack(pady=10)

        self.url_entry = Entry(f, width=50)
        self.url_entry.pack(pady=10)

        Button(
            f,
            text="Scan Website",
            bg="green",
            fg="white",
            width=20,
            command=self.scan_website,
        ).pack(pady=10)

        self.msg = Label(
            f, text="Waiting for website...", bg="azure", font=("Arial", 12)
        )
        self.msg.pack(pady=5)

        self.tree = ttk.Treeview(
            f, columns=("Type", "Value"), show="headings", height=15
        )
        self.tree.heading("Type", text="Data Type")
        self.tree.heading("Value", text="Value")
        self.tree.column("Type", width=150)
        self.tree.column("Value", width=600)
        self.tree.pack(fill=BOTH, expand=True, pady=10)

    def scan_website(self):
        url = self.url_entry.get().strip()
        for row in self.tree.get_children():
            self.tree.delete(row)

        WebsiteScanner(url, self.msg, self.tree).start_scan()


if __name__ == "__main__":
    root = Tk()
    root.resizable(0, 0)
    MainWindow(root)
    root.mainloop()

