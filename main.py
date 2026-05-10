import telebot
import feedparser
import time
from flask import Flask
from threading import Thread

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
YOUR_CHAT_ID = "634887309" # حطي الآيدي حقك هنا عشان يرسل لك مباشرة
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon News Radar is Scanning... 📡"

# قائمة لحفظ الأخبار القديمة عشان ما يكررها لك
sent_news = []

def news_radar():
    while True:
        try:
            # روابط الرادار (كورة + عالم)
            urls = [
                "https://feeds.bbci.co.uk/arabic/sports/rss.xml",
                "https://www.skynewsarabia.com/rss/v1/world.xml"
            ]
            
            for url in urls:
                feed = feedparser.parse(url)
                for entry in feed.entries[:3]: # يشيّك على آخر 3 أخبار في كل رابط
                    if entry.link not in sent_news:
                        # خبر جديد! أرسله فوراً
                        message = f"🚨 **خبر عاجل من الرادار:**\n\n{entry.title}\n\n🔗 {entry.link}"
                        bot.send_message(YOUR_CHAT_ID, message)
                        
                        # أضفه للقائمة عشان ما يرسله مرة ثانية
                        sent_news.append(entry.link)
                        
                        # نحافظ على القائمة صغيرة (آخر 50 خبر بس)
                        if len(sent_news) > 50:
                            sent_news.pop(0)
            
            # انتظر 10 دقائق قبل ما تشيك مرة ثانية (عشان ما ينحظر)
            time.sleep(600) 
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    # تشغيل الرادار في خلفية البوت
    Thread(target=news_radar).start()
    Thread(target=run_flask).start()
    bot.infinity_polling()
