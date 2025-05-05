import requests
import os

def notify_make(data):
    try:
        requests.post(os.getenv("MAKE_WEBHOOK"), json=data)
    except Exception as e:
        print(f"[MAKE ERROR] {e}")

def notify_slack(data):
    try:
        msg = f"*[Pastebin Leak Alert]*\nURL: {data['url']}\nKeywords: {', '.join(data['keywords_found'])}\nExcerpt: {data['excerpt']}"
        requests.post(os.getenv("SLACK_WEBHOOK"), json={"text": msg})
    except Exception as e:
        print(f"[SLACK ERROR] {e}")
