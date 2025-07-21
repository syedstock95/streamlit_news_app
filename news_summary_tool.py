import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import os

# Email & SMS settings
EMAIL_FROM = "syedstock95@gmail.com"
EMAIL_TO = ["syedstock95@gmail.com", "2815699748@tmomail.net"]
EMAIL_SUBJECT = "📈 Daily Market & Crypto News Summary"
EMAIL_APP_PASSWORD = "rkzh nbvt rhbw cztq"  # Replace with your Gmail app password

# Excel output directory
OUTPUT_DIR = r"D:\OneDrive\Documents\shares\Document\News"

# Basic news sources
NEWS_SOURCES = {
    "Yahoo Finance": "https://finance.yahoo.com",
    "Google News - Business": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTjJZU0FtVnVLQUFQAQ",
    "CoinDesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "Cointelegraph": "https://cointelegraph.com/rss",
    "MarketWatch": "https://www.marketwatch.com/feeds/rss/topstories",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html"
}

def fetch_rss_news(source_name, rss_url):
    headlines = []
    try:
        resp = requests.get(rss_url)
        soup = BeautifulSoup(resp.content, 'xml')
        items = soup.find_all('item')[:5]
        for item in items:
            headlines.append({
                'source': source_name,
                'title': item.title.text,
                'link': item.link.text,
                'summary': item.description.text[:300]
            })
    except Exception as e:
        print(f"Error fetching from {source_name}: {e}")
    return headlines

def fetch_yahoo_headlines():
    headlines = []
    try:
        resp = requests.get("https://finance.yahoo.com", headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.content, "html.parser")
        for tag in soup.select("a[href^='/news/']")[:5]:
            title = tag.get_text().strip()
            link = "https://finance.yahoo.com" + tag.get("href")
            headlines.append({
                'source': "Yahoo Finance",
                'title': title,
                'link': link,
                'summary': ''
            })
    except Exception as e:
        print(f"Error fetching Yahoo Finance: {e}")
    return headlines

def compile_news():
    all_news = []
    all_news.extend(fetch_yahoo_headlines())
    for name, url in NEWS_SOURCES.items():
        if "Yahoo" not in name:
            all_news.extend(fetch_rss_news(name, url))
    return all_news

def save_to_excel(news_items):
    df = pd.DataFrame(news_items)
    now = datetime.now().strftime("%Y%m%d_%H%M")
    file_path = os.path.join(OUTPUT_DIR, f"market_news_summary_{now}.xlsx")
    df.to_excel(file_path, index=False)
    print(f"✅ News saved to: {file_path}")
    return file_path

def send_email(news_items, attachment=None):
    msg = EmailMessage()
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = EMAIL_FROM
    msg["To"] = ', '.join(EMAIL_TO)

    content = "\n".join([f"- {item['title']} ({item['source']})\n{item['link']}" for item in news_items[:5]])
    msg.set_content(f"🗞 Top Headlines:\n\n{content}")

    if attachment:
        with open(attachment, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename=os.path.basename(attachment))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_FROM, EMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        print("📧 Email and SMS sent!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    news_items = compile_news()
    excel_file = save_to_excel(news_items)
    send_email(news_items, attachment=excel_file)

if __name__ == "__main__":
    main()
