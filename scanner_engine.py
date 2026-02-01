import requests
from bs4 import BeautifulSoup
import validators
import hashlib
import time as pytime
from datetime import datetime, timezone


class ScannerEngine:
    def __init__(self, url): 
        self.url = url
        self.sections = []

    def clean(self, soup):
        for tag in soup(
            ["script", "style", "nav", "footer", "header", "aside", "noscript"]
        ):
            tag.decompose()

    def extract(self, soup):
        sections = []
        current = {"heading": "INTRODUCTION", "paragraphs": []}

        for tag in soup.find_all(["h1", "h2", "h3", "p", "div"]):
            if tag.name in ["h1", "h2", "h3"]:
                if current["paragraphs"]:
                    sections.append(current)

                current = {
                    "heading": f"{tag.name.upper()} - {tag.get_text(strip=True)}",
                    "paragraphs": [],
                }
            else:
                text = tag.get_text(" ", strip=True)
                if 60 < len(text) < 800:
                    current["paragraphs"].append(text)

        if current["paragraphs"]:
            sections.append(current)
        return sections

    def content_hash(self):
        combined = ""
        for sec in self.sections:
            combined += sec["heading"] + "".join(sec["paragraphs"])
        return hashlib.sha256(combined.encode()).hexdigest()

    def detect_changes(self, new_hash):
        try:
            with open("last_hash.txt", "r") as f:
                return f.read() != new_hash
        except:
            return True

    def save_hash(self, h):
        with open("last_hash.txt", "w") as f:
            f.write(h)

    def analyze_quality(self):
        issues = []
        seen = set()

        for sec in self.sections:
            for p in sec["paragraphs"]:
                if len(p) > 600:
                    issues.append("Long paragraph detected")
                if p in seen:
                    issues.append("Duplicate paragraph detected")
                seen.add(p)

        return issues

    def scan(self):
        if not validators.url(self.url):
            raise ValueError("Invalid URL format")

        r = requests.get(self.url, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        self.clean(soup)

        title = soup.title.string.strip() if soup.title else "No Title"
        self.sections = self.extract(soup)

        now_hash = self.content_hash()
        changed = self.detect_changes(now_hash)
        self.save_hash(now_hash)

        paragraphs = []
        for sec in self.sections:
            for p in sec["paragraphs"]:
                paragraphs.append({"heading": sec["heading"], "paragraph": p})

        return {
            "url": self.url,
            "title": title,
            "sections": self.sections,
            "content_hash": now_hash,
            "change_status": "CHANGED" if changed else "NO CHANGE",
            "paragraphs": paragraphs,
            "quality_issues": self.analyze_quality(),
            "scanned_at": datetime.now(timezone.utc),
        }
