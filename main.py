import cloudscraper
from bs4 import BeautifulSoup
import time
import requests
import os

# Render-e process active rakhar jonno ekta chotto trick
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Running"

# --- CONFIGURATION (Environment Variables theke neoa hobe) ---
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
        response = scraper.get(url, cookies=cookies, headers=headers)
        if "Logout" in response.text:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_rows = soup.select('tr[id^="job_"]') or soup.select('tr.job_item')
            for row in job_rows:
                job_id = row.get('id')
                if job_id and job_id not in old_jobs:
                    cells = row.find_all('td')
                    if len(cells) >= 4:
                        title = cells[2].text.strip()
                        payment = cells[3].text.strip()
                        msg = f"🚀 **New Job!**\n📝 {title}\n💰 {payment}\n🔗 [Apply](https://www.microworkers.com/jobs.php)"
                        requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                        old_jobs.add(job_id)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    # Script-ti background-e cholbe
    from threading import Thread
    def run_bot():
        while True:
            get_jobs()
            time.sleep(20) # Instant update-er jonno 20 sec interval
    
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
