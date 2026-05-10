import telebot
import feedparser
from flask import Flask
from threading import Thread

# توكن البوت حقك
TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
bot = telebot.TeleBot(TOKEN)

# تنظيف أي تعليق قديم
bot.remove_webhook()

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon News is Live! ⚽🌍"

# دالة تجيب الأخبار وترتبها
def get_news_feed(url):
    feed = feedparser.parse(url)
    out = ""
    for entry in feed.entries[:6]: # بيجيب لك أفضل 6 أخبار
        out += f"🔹 {entry.title}\n🔗 {entry.link}\n\n"
    return out if out else "لا توجد أخبار حالياً."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "هلا بك في رادار الأخبار! 🦅\n\nأرسل 'كورة' لأخبار الملاعب\nأرسل 'عالم' لأخبار العالم")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    msg = message.text.lower()
    
    if "كورة" in msg or "رياضة" in msg:
        bot.reply_to(message, "⚽ جاري صيد أخبار الكورة والصفقات...")
        # رابط متخصص كورة (FilGoal)
        news = get_news_feed("https://www.filgoal.com/section/rss?sectionid=2")
        bot.send_message(message.chat.id, f"🏆 **أخبار كرة القدم:**\n\n{news}")

    elif "عالم" in msg or "أخبار" in msg:
        bot.reply_to(message, "🌍 جاري جلب العناوين العالمية العاجلة...")
        # رابط سكاي نيوز عالم
        news = get_news_feed("https://www.skynewsarabia.com/rss/v1/world.xml")
        bot.send_message(message.chat.id, f"🌎 **عاجل العالم:**\n\n{news}")
    
    else:
        bot.reply_to(message, "أرسل 'كورة' أو 'عالم' عشان أعطيك الأخبار. 😉")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
