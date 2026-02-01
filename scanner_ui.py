import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from threading import Thread
import json
from pymongo import MongoClient
import os
import time as pytime
from scanner_engine import ScannerEngine
 
MONGO_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGO_URI)
db = client["website_scan"]
collection = db["scanner_data"]


class ScannerUI:
    def __init__(self, master, parent_dashboard=None):
        self.master = master
        self.parent_dashboard = parent_dashboard 

        self.master.title("Website Content Analysis & Monitoring System")
        self.master.geometry("1350x760")


        if self.parent_dashboard:
            self.master.transient(self.parent_dashboard)
            self.master.focus_force()

        self.engine = None
        self.scan_data = None
        self.running = False
        self.start_time = None

        self.build_ui()

    def build_ui(self):

        tk.Label(
            self.master,
            text="Website Content Scanning System",
            font=("Arial", 20, "bold"),
        ).pack(pady=8)


        self.url_entry = tk.Entry(self.master, width=95)
        self.url_entry.pack()


        tk.Button(
            self.master,
            text="Scan Website",
            command=self.start_scan,
            bg="#0b8043",
            fg="white",
            width=18,
        ).pack(pady=4)


        self.msg = tk.Label(self.master, fg="blue", font=("Arial", 10, "bold"))
        self.msg.pack()

        self.timer = tk.Label(self.master, fg="darkred")
        self.timer.pack()

        self.stats = tk.Label(self.master, fg="black", font=("Arial", 10, "bold"))
        self.stats.pack(pady=3)

   
        self.search_entry = tk.Entry(self.master, width=40)
        self.search_entry.pack(pady=2)

        tk.Button(self.master, text="🔍 Search", command=self.search_text).pack()


        columns = ("Type", "Content")
        self.tree = ttk.Treeview(self.master, columns=columns, show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Content", text="Content")
        self.tree.column("Type", width=160)
        self.tree.column("Content", width=1100)
        self.tree.pack(fill="both", expand=True)

        self.tree.tag_configure(
            "title", foreground="#0b5394", font=("Arial", 10, "bold")
        )
        self.tree.tag_configure(
            "section", foreground="#38761d", font=("Arial", 10, "bold")
        )
        self.tree.tag_configure("paragraph", foreground="black")
        self.tree.tag_configure("hash", foreground="#777777")
        self.tree.tag_configure("issue", foreground="#990000")
        self.tree.tag_configure("status", foreground="#6a329f")

        btn_frame = tk.Frame(self.master)
        btn_frame.pack(pady=6)

        tk.Button(
            btn_frame,
            text="📋 Copy Paragraph",
            command=self.copy_paragraph,
            bg="#1c4587",
            fg="white",
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame,
            text="⬇ Export TXT",
            command=self.export_txt,
            bg="#990000",
            fg="white",
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame,
            text="⬇ Export JSON",
            command=self.export_json,
            bg="#274e13",
            fg="white",
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame,
            text="💾 Save to MongoDB",
            command=self.save_to_mongodb,
            bg="#134f5c",
            fg="white",
        ).pack(side="left", padx=4)

        tk.Button(
            self.master,
            text="🔙 Logout to Dashboard",
            command=self.logout,
            bg="#b71c1c",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
        ).pack(pady=10)


    def logout(self):
        self.master.destroy()

    def timer_loop(self):
        while self.running:
            elapsed = int(pytime.time() - self.start_time)
            self.timer.config(text=f"⏱ Scanning… {elapsed}s")
            pytime.sleep(1)

    def start_scan(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Missing", "Enter a URL first.")
            return

        self.tree.delete(*self.tree.get_children())
        self.stats.config(text="")
        self.msg.config(text="🔍 Fetching website…")

        self.start_time = pytime.time()
        self.running = True

        Thread(target=self.timer_loop, daemon=True).start()
        Thread(target=self.worker_scan, args=(url,), daemon=True).start()

 
    def worker_scan(self, url):
        try:
            self.engine = ScannerEngine(url)
            data = self.engine.scan()
            self.scan_data = data
            self.master.after(0, lambda: self.display_results(data))
        except Exception as e:
            self.master.after(0, lambda: self.msg.config(text=f"❌ Error: {e}"))
        finally:
            self.running = False


    def display_results(self, data):
        self.tree.insert("", "end", values=("TITLE", data["title"]), tags=("title",))
        self.tree.insert(
            "", "end", values=("CONTENT_HASH", data["content_hash"]), tags=("hash",)
        )
        self.tree.insert(
            "", "end", values=("CHANGE_STATUS", data["change_status"]), tags=("status",)
        )

        para_count = 0
        for sec in data["sections"]:
            sec_id = self.tree.insert(
                "", "end", values=("SECTION", sec["heading"]), tags=("section",)
            )
            for p in sec["paragraphs"]:
                para_count += 1
                self.tree.insert(
                    sec_id, "end", values=("PARAGRAPH", p), tags=("paragraph",)
                )

        for issue in data["quality_issues"]:
            self.tree.insert(
                "", "end", values=("QUALITY_ISSUE", issue), tags=("issue",)
            )

        elapsed = int(pytime.time() - self.start_time)

        self.stats.config(
            text=f"📊 Sections: {len(data['sections'])} | Paragraphs: {para_count} | Time: {elapsed}s"
        )
        self.timer.config(text=f"⏱ Completed in {elapsed}s")
        self.msg.config(text="✔ Scan Complete (Ready to Save)")


    def search_text(self):
        key = self.search_entry.get().lower()
        self.tree.selection_remove(self.tree.selection())

        for sec in self.tree.get_children():
            for child in self.tree.get_children(sec):
                val = self.tree.item(child)["values"]
                if val and key in val[1].lower():
                    self.tree.selection_add(child)
                    self.tree.see(child)


    def copy_paragraph(self):
        item = self.tree.focus()
        if not item:
            return
        dtype, content = self.tree.item(item)["values"]
        if dtype != "PARAGRAPH":
            messagebox.showwarning("Invalid", "Select a paragraph")
            return

        self.master.clipboard_clear()
        self.master.clipboard_append(content)
        messagebox.showinfo("Copied", "Paragraph copied to clipboard")


    def export_txt(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", parent=self.master)
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            for sec in self.tree.get_children():
                for item in self.tree.get_children(sec):
                    f.write(self.tree.item(item)["values"][1] + "\n\n")


    def export_json(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json", parent=self.master
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.scan_data, f, indent=2, default=str)

    def save_to_mongodb(self):
        if not self.scan_data:
            messagebox.showwarning("No Data", "Scan a website first.")
            return

        Thread(target=self._mongo_worker, daemon=True).start()

    def _mongo_worker(self):
        selected = None
        item = self.tree.focus()

        if item:
            dtype, content = self.tree.item(item)["values"]
            if dtype == "PARAGRAPH":
                selected = content

        doc = {
            **self.scan_data,
            "selected_paragraph": selected,
            "stats": {
                "sections": len(self.scan_data["sections"]),
                "paragraphs": len(self.scan_data["paragraphs"]),
            },
        }

        collection.insert_one(doc)
        self.master.after(
            0, lambda: messagebox.showinfo("Saved", "Scan saved to MongoDB")
        )

