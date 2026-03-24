import cloudscraper
from bs4 import BeautifulSoup
import requests
import os
from flask import Flask

app = Flask(__name__)

# --- CONFIGURATION ---
BOT_TOKEN = os.environ.get("8669291841:AAGJzGF5ZVb95ypH8_GWIFWOGnOt4DbDY84")
CHAT_ID = os.environ.get("@MWjobalart")
SESSION_ID = os.environ.get("va398qh99aof6n0v3i89cc9ulh")

scraper = cloudscraper.create_scraper()
old_jobs = set()

def scan():
    global old_jobs
    url = "https://www.microworkers.com/jobs.php"
    cookies = {'PHPSESSID': SESSION_ID}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    
    try:
        response = scraper.get(url, cookies=cookies, headers=headers)
        if "Logout" not in response.text:
            return "❌ Session Expired. Update PHPSESSID in Render Settings."

        soup = BeautifulSoup(response.text, 'html.parser')
        job_rows = soup.select('tr[id^="job_"]') or soup.select('tr.job_item')
        
        count = 0
        for row in job_rows:
            job_id = row.get('id')
            if job_id and job_id not in old_jobs:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    title = cells[2].text.strip()
                    payment = cells[3].text.strip()
                    msg = f"🚀 **New Job!**\n\n📝 {title}\n💰 {payment}\n🔗 [Apply](https://www.microworkers.com/jobs.php)"
                    
                    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                 params={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                    old_jobs.add(job_id)
                    count += 1
        return f"✅ Scan Complete. New jobs: {count}"
    except Exception as e:
        return f"🔥 Error: {str(e)}"

@app.route('/')
def home():
    # Jokhoni UptimeRobot ekhane hit korbe, scan run hobe
    result = scan()
    print(f"Update: {result}")
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
