import requests
from bs4 import BeautifulSoup
from threading import Thread
import validators

class WebsiteScanner:
    def __init__(self, url, msg_label, tree):
        self.url = url
        self.msg_label = msg_label
        self.tree = tree

    def start_scan(self):
        Thread(target=self._scan).start() 

    def _scan(self):
        if not validators.url(self.url):
            self.msg_label.config(text="Invalid URL format")
            return

        try:
            self.msg_label.config(text="Scanning website...")

            response = requests.get(self.url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.title.string if soup.title else "No Title"
            headings = [h.get_text().strip() for h in soup.find_all(["h1", "h2", "h3"])]
            links = [a.get("href") for a in soup.find_all("a", href=True)]
            forms = [f.get("action") for f in soup.find_all("form")]
            scripts = [s.get("src") for s in soup.find_all("script", src=True)]

            self.tree.insert("", "end", values=("Title", title))

            for h in headings:
                self.tree.insert("", "end", values=("Heading", h))

            for l in links:
                self.tree.insert("", "end", values=("Link", l))

            for f in forms:
                self.tree.insert("", "end", values=("Form Action", f))

            for s in scripts:
                self.tree.insert("", "end", values=("Script Src", s))

            self.msg_label.config(text=f"✔ Scan Complete — {len(links)} links found")

        except Exception as e:
            self.msg_label.config(text=f"Error: {e}")
            
