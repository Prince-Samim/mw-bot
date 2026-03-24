import cloudscraper
from bs4 import BeautifulSoup
import time
import requests
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running! All system normal."

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("8669291841:AAGJzGF5ZVb95ypH8_GWIFWOGnOt4DbDY84")
CHAT_ID = os.environ.get("@MWjobalart")
SESSION_ID = os.environ.get("b9nuin9bpn89r323j1dpfegogk")

scraper = cloudscraper.create_scraper()
old_jobs = set()

def get_jobs():
    global old_jobs
    url = "https://www.microworkers.com/jobs.php"
    cookies = {'PHPSESSID': SESSION_ID}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    try:
        print("🔍 Checking Microworkers for new jobs...")
        response = scraper.get(url, cookies=cookies, headers=headers)
        
        if "Logout" not in response.text:
            print("❌ Session ID is NOT working or expired. Please update it.")
            return

        print("✅ Logged in successfully. Scanning jobs...")
        soup = BeautifulSoup(response.text, 'html.parser')
        job_rows = soup.select('tr[id^="job_"]') or soup.select('tr.job_item')

        if not job_rows:
            print("ℹ️ No jobs found on the page.")
            return

        for row in job_rows:
            job_id = row.get('id')
            if job_id and job_id not in old_jobs:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    title = cells[2].text.strip()
                    payment = cells[3].text.strip()
                    msg = f"🚀 **New Job Alert!**\n\n📝 **Job:** {title}\n💰 **Payment:** {payment}\n🔗 [Apply Now](https://www.microworkers.com/jobs.php)"
                    
                    res = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                    if res.status_code == 200:
                        print(f"✅ Telegram Alert Sent: {title}")
                        old_jobs.add(job_id)
                    else:
                        print(f"❌ Telegram Error: {res.text}")
                        
    except Exception as e:
        print(f"🔥 Error: {e}")

def run_bot_loop():
    # Prothom bar list load kora jate purono sob message na ashe
    print("🚀 Bot thread starting...")
    while True:
        get_jobs()
        time.sleep(30) # Interval

if __name__ == "__main__":
    # Start bot thread
    Thread(target=run_bot_loop, daemon=True).start()
    # Start Web Server
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
