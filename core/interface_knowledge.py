# core/interface_knowledge.py

import json
import os
import requests
from bs4 import BeautifulSoup

knowledge_base = {}

def preload_interface_knowledge():
    global knowledge_base
    apps = ["whatsapp", "instagram", "youtube"]

    for app in apps:
        url = f"https://www.google.com/search?q=interface+elements+in+{app}+app"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        texts = soup.stripped_strings
        found = set([line for line in texts if len(line) > 4 and "button" in line.lower()])
        knowledge_base[app] = list(found)

    print("✅ RUDRA trained on UI elements:")
    for app, items in knowledge_base.items():
        print(f"  {app.title()}: {len(items)} elements learned")
