import cloudscraper
from bs4 import BeautifulSoup
import requests
import os
from flask import Flask

app = Flask(__name__)

# CONFIGURATION
BOT_TOKEN = os.environ.get("8669291841:AAGJzGF5ZVb95ypH8_GWIFWOGnOt4DbDY84")
CHAT_ID = os.environ.get("@MWjobalart")
SESSION_ID = os.environ.get("r1vki8jd6iqvm5e0kucqoudpa9")

# Cloudflare bypass korar jonno scraper
scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
)

old_jobs = set()

def scan():
    global old_jobs
    url = "https://www.microworkers.com/jobs.php"
    cookies = {'PHPSESSID': SESSION_ID}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = scraper.get(url, cookies=cookies, headers=headers, timeout=25)
        
        if "Logout" not in response.text:
            return "❌ Error: Session Expired/IP Blocked"

        soup = BeautifulSoup(response.text, 'html.parser')
        job_rows = soup.select('tr[id^="job_"]')
        
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
        return f"✅ Scan Success. New jobs: {count}"
    except Exception as e:
        return f"🔥 Error: {str(e)}"

@app.route('/')
def home():
    res = scan()
    print(f"Log Output: {res}")
    return res

if __name__ == "__main__":
    # Render-er port issue fix korar jonno
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
