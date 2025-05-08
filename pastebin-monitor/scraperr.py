import os
import re
import time
import cloudscraper
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from generate_keywords import generate_keywords
from notifier import notify_make, notify_slack

# === Load Environment Variables ===
load_dotenv()
PASTEBIN_ARCHIVE = "https://pastebin.com/archive"
PASTEBIN_RAW = "https://pastebin.com/raw/"
USER_AGENT = "Mozilla/5.0"
USE_TOR = os.getenv("USE_TOR", "false").lower() == "true"

# === Load and Generate Keywords ===
try:
    with open("config/companies.txt", "r") as f:
        company_domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
except FileNotFoundError:
    print("[ERROR] 'config/companies.txt' not found. Exiting.")
    exit(1)

KEYWORDS = list(set(generate_keywords(company_domains)))  # Remove duplicates
print(f"[*] Loaded {len(KEYWORDS)} keywords from company list.")

# === Setup Scraper ===
scraper = cloudscraper.create_scraper(browser='chrome')
if USE_TOR:
    scraper.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

# === Fetch Latest Paste IDs ===
def get_recent_pastes():
    try:
        res = scraper.get(PASTEBIN_ARCHIVE, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(res.text, 'html.parser')
        return [a.get("href")[1:] for a in soup.select("table.maintable tr td a") if a.get("href")][:10]
    except Exception as e:
        print(f"[ERROR] Fetching recent pastes: {e}")
        return []

# === Check Each Paste for Keywords and Sensitive Info ===
def check_paste_content(paste_id):
    try:
        res = scraper.get(PASTEBIN_RAW + paste_id, headers={"User-Agent": USER_AGENT})
        content = res.text.lower()

        matched_keywords = [
            kw for kw in KEYWORDS
            if re.search(rf"(?<!\w){re.escape(kw.lower())}(?!\w)", content)
        ]

        if not matched_keywords:
            return None

        sensitive_patterns = {
            "Phone Number": r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b",
            "Credit Card": r"\b\d{4}[-.\s]??\d{4}[-.\s]??\d{4}[-.\s]??\d{4}\b",
            "API Key": r"(sk|api|key|token|secret)[_-]?[a-z0-9]{10,}"
        }

        for label, pattern in sensitive_patterns.items():
            if re.search(pattern, content):
                matched_keywords.append(f"[Sensitive: {label}]")

        return {
            "paste_id": paste_id,
            "url": f"https://pastebin.com/{paste_id}",
            "keywords_found": list(set(matched_keywords)),
            "excerpt": content[:300]
        }

    except Exception as e:
        print(f"[ERROR] Checking paste {paste_id}: {e}")
        return None

# === Main Monitoring Loop ===
def main():
    print("[*] Starting Pastebin monitoring...")
    scanned = set()

    while True:
        paste_ids = get_recent_pastes()
        for pid in paste_ids:
            if pid in scanned:
                continue

            result = check_paste_content(pid)
            if result:
                print(f"[ALERT] Match found: {result['url']}")
                print(f"       Keywords: {result['keywords_found']}")
                notify_make(result)
                notify_slack(result)

            scanned.add(pid)

        time.sleep(60)  # Delay between scans

if __name__ == "__main__":
    main()
