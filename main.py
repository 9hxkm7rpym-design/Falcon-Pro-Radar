import telebot
import yfinance as yf
import feedparser
from flask import Flask
from threading import Thread

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon Multi-Bot is Live! 🦅"

# دالة تجيب الأخبار
def get_news_feed(url):
    feed = feedparser.parse(url)
    out = ""
    for entry in feed.entries[:5]:
        out += f"🔹 {entry.title}\n🔗 {entry.link}\n\n"
    return out if out else "لا توجد أخبار حالياً."

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    msg = message.text.lower()
    
    # إذا طلبتِ كورة
    if "كورة" in msg or "رياضة" in msg:
        bot.reply_to(message, "⚽ جاري صيد أخبار الملاعب...")
        news = get_news_feed("https://www.aljazeera.net/aljazeerarss/ad38061e-ca7b-457f-b363-69ad31f2c395/363f8983-f36e-44d4-8399-563b7e719601")
        bot.send_message(message.chat.id, f"🏆 **أخبار الرياضة:**\n\n{news}")

    # إذا طلبتِ أخبار العالم
    elif "عالم" in msg or "أخبار" in msg:
        bot.reply_to(message, "🌍 جاري جلب العناوين العالمية...")
        news = get_news_feed("https://www.aljazeera.net/aljazeerarss/3c6d3630-4621-4954-841c-c04941919623/6909405d-635c-48c0-83f5-6679549f7ba3")
        bot.send_message(message.chat.id, f"🌎 **عاجل العالم:**\n\n{news}")

    # إذا أرسلتِ رمز سهم (مثل AAPL أو BTC-USD)
    else:
        symbol = message.text.upper()
        bot.send_message(message.chat.id, f"🔍 جاري فحص السعر لـ {symbol}...")
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d')
            if not data.empty:
                price = data['Close'].iloc[-1]
                bot.reply_to(message, f"💰 السعر الحالي لـ {symbol} هو: ${price:.2f}")
            else:
                bot.reply_to(message, "❌ ياهو مقفل حالياً، جربي 'كورة' أو 'عالم' لين يفتح السوق!")
        except:
            bot.reply_to(message, "أرسلي رمز سهم صحيح، أو اكتبي 'كورة' للأخبار.")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
