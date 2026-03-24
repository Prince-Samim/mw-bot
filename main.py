import cloudscraper
from bs4 import BeautifulSoup
import requests
import os
import time
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = os.environ.get("8669291841:AAGJzGF5ZVb95ypH8_GWIFWOGnOt4DbDY84")
CHAT_ID = os.environ.get("@MWjobalart")
SESSION_ID = os.environ.get("6occkg3c89c7am7i7a5q49akqs")

# উন্নত ব্রাউজার হেডার
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

old_jobs = set()

def scan():
    global old_jobs
    url = "https://www.microworkers.com/jobs.php"
    cookies = {'PHPSESSID': SESSION_ID}
    
    # এটি মাইক্রোওয়ার্কার্সকে ধোঁকা দিতে সাহায্য করবে
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.microworkers.com/index.php'
    }
    
    try:
        response = scraper.get(url, cookies=cookies, headers=headers, timeout=15)
        
        # লগইন চেক
        if "Logout" not in response.text:
            return "❌ Session Expired. Update PHPSESSID from your browser."

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
                    msg = f"🚀 **New Job Found!**\n\n📝 **Job:** {title}\n💰 **Pay:** {payment}\n🔗 [Apply](https://www.microworkers.com/jobs.php)"
                    
                    requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                                 params={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'})
                    old_jobs.add(job_id)
                    count += 1
        return f"✅ Scan Done. Jobs Found: {count}"
    except Exception as e:
        return f"🔥 Error: {str(e)}"

@app.route('/')
def home():
    result = scan()
    return f"Bot Status: {result}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
