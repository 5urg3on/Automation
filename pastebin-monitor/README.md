# Automated Pastebin Monitoring System

A Python-based system to monitor Pastebin leaks for company-related data using keywords generated from domains.

## Features

- Automatic keyword generation from company domains
- Slack or Make.com webhook alerts to slack
- Optional TOR proxy support for anonymity
- Easy to deploy on Kali, VPS, or Raspberry Pi

## Setup

```bash
git clone https://github.com/5urg3on/Automation.git
cd pastebin-monitor
pip install -r requirements.txt
cp .env.example .env
# Add your domains to config/companies.txt
python scraper.py
