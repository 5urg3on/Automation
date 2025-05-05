import os
import re
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from keyword_utils import generate_keywords
from notifier import notify_make, notify_slack

# Load environment variables
load_dotenv()

# Constants and Configuration
PASTEBIN_ARCHIVE = "https://pastebin.com/archive"
PASTEBIN_RAW = "https://pastebin.com/raw/"
USER_AGENT = "Mozilla/5.0"
USE_TOR = os.getenv("USE_TOR", "false").lower() == "true"

# Load company domains
with open("config/companies.txt") as f:
    COMPANY_DOMAINS = [line.strip() for line in f.readlines()]
KEYWORDS = generate_keywords(COMPANY_DOMAINS)

# Proxy config if using Tor
PROXIES = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
} if USE_TOR else {}

# Fetch recent paste IDs
def get_recent_pastes():
    try:
        res = requests.get(PASTEBIN_ARCHIVE, headers={"User-Agent": USER_AGENT}, proxies=PROXIES)
        soup = BeautifulSoup(res.text, 'html.parser')
        return [a.get("href")[1:] for a in soup.select("table.maintable tr td a")[:10]]
    except Exception as e:
        print(f"[ERROR] Fetching recent pastes: {e}")
        return []

# Check content of each paste for keywords or patterns
def check_paste(paste_id):
    try:
        res = requests.get(PASTEBIN_RAW + paste_id, headers={"User-Agent": USER_AGENT}, proxies=PROXIES)
        content = res.text.lower()

        matches = []

        # Match custom keywords
        for keyword in KEYWORDS:
            if re.search(rf"\b{re.escape(keyword)}\b", content):
                matches.append(keyword)

        # Match sensitive data patterns
        patterns = [
            r"\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b",        # Phone numbers
            r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",  # Emails
            r"\b\d{4}[-.\s]??\d{4}[-.\s]??\d{4}[-.\s]??\d{4}\b", # Credit card-style
            r"api[_-]?key\s*[:=]\s*[a-z0-9]{16,}",         # API keys
        ]

        for pattern in patterns:
            if re.search(pattern, content):
                matches.append(pattern)

        if matches:
            return {
                "paste_id": paste_id,
                "url": f"https://pastebin.com/{paste_id}",
                "keywords_found": matches,
                "excerpt": content[:200] + "..."
            }

    except Exception as e:
        print(f"[ERROR] Checking paste {paste_id}: {e}")
    
    return None

# Main monitoring loop
def main():
    print("[*] Starting Pastebin Monitoring...")
    while True:
        paste_ids = get_recent_pastes()
        for pid in paste_ids:
            result = check_paste(pid)
            if result:
                print(f"[ALERT] Match found in {result['url']}")
                notify_make(result)
                notify_slack(result)
        time.sleep(3600)  # Sleep for 1 hour

if __name__ == "__main__":
    main()
