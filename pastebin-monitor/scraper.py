import os
import re
import time
import cloudscraper
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from generate_keywords import generate_keywords
from notifier import notify_make, notify_slack

load_dotenv()

PASTEBIN_ARCHIVE = "https://pastebin.com/archive"
PASTEBIN_RAW = "https://pastebin.com/raw/"
USER_AGENT = "Mozilla/5.0"
USE_TOR = os.getenv("USE_TOR", "false").lower() == "true"

# Company domains
with open("config/companies.txt") as f:
    COMPANY_DOMAINS = [line.strip() for line in f.readlines()]
KEYWORDS = generate_keywords(COMPANY_DOMAINS)

# Setup scraper
scraper = cloudscraper.create_scraper(browser='chrome')
if USE_TOR:
    scraper.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

def get_recent_pastes():
    try:
        res = scraper.get(PASTEBIN_ARCHIVE, headers={"User-Agent": USER_AGENT})
        soup = BeautifulSoup(res.text, 'html.parser')
        return [a.get("href")[1:] for a in soup.select("table.maintable tr td a")[:10]]
    except Exception as e:
        print(f"[ERROR] Fetching recent pastes: {e}")
        return []

def check_paste_content(paste_id):
    try:
        res = scraper.get(PASTEBIN_RAW + paste_id, headers={"User-Agent": USER_AGENT})
        content = res.text.lower()

        company_matches = []
        for kw in KEYWORDS:
            pattern = rf"(?<!\w){re.escape(kw.lower())}(?!\w)"
            if re.search(pattern, content):
                company_matches.append(kw)

        if not company_matches:
            return None

        # Check for sensitive patterns
        sensitive_patterns = [
            r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b",         # Phone numbers
            r"\b\d{4}[-.\s]??\d{4}[-.\s]??\d{4}[-.\s]??\d{4}\b",  # Credit cards
            r"(sk|api|key|token|secret)[_-]?[a-z0-9]{10,}",      # API keys
        ]
        for pattern in sensitive_patterns:
            if re.search(pattern, content):
                company_matches.append(f"[Sensitive: {pattern}]")

        print(f"[DEBUG] Keywords found in paste {paste_id}: {company_matches}")
        return {
            "paste_id": paste_id,
            "url": f"https://pastebin.com/{paste_id}",
            "keywords_found": list(set(company_matches)),
            "excerpt": content[:300]
        }

    except Exception as e:
        print(f"[ERROR] Checking paste {paste_id}: {e}")
        return None

def main():
    print("[*] Starting Pastebin Monitoring...")
    while True:
        paste_ids = get_recent_pastes()
        for pid in paste_ids:
            result = check_paste_content(pid)
            if result:
                print(f"[ALERT] Match found in {result['url']}")
                notify_make(result)
                notify_slack(result)
        time.sleep(1000)

if __name__ == "__main__":
    main()
