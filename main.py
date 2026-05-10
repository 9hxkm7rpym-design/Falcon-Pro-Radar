import os
import telebot
from flask import Flask
from threading import Thread
import time
import yfinance as yf

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "634887309"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

WATCHLIST = ['NVDA', 'TSLA', 'AMZN', 'OXY', 'AAPL', 'MSFT', 'QQQ', '^SPX']

@app.route('/')
def home(): return "Falcon Radar is Active! 🦅"

# الرد الآلي (موجود وشغال)
@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
    bot.reply_to(message, "🦅 هلا والله يا سلطان! رادار الفالكون شغال الحين وجالس يراقب الأسهم. أبشر بالسعد!")

def scanner():
    # ننتظر قليلاً قبل بدء الرادار لضمان استقرار استقبال الرسائل
    time.sleep(10)
    while True:
        for s in WATCHLIST:
            try:
                ticker = yf.Ticker(s)
                data = ticker.history(period='1d')
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    name = "SPX (سباكس)" if s == '^SPX' else s
                    msg = f"🦅 رادار الفالكون:\n📊 السهم: {name}\n💰 السعر الحالي: ${current_price:.2f}"
                    bot.send_message(CHAT_ID, msg)
                    time.sleep(5)
            except: pass
        time.sleep(3600)

if __name__ == "__main__":
    # 1. تشغيل الرادار في الخلفية
    t = Thread(target=scanner)
    t.daemon = True
    t.start()
    
    # 2. تشغيل استقبال الرسائل (Polling) في خيط منفصل
    # استخدمنا infinity_polling لأنها أقوى في الاستمرارية
    t2 = Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5))
    t2.daemon = True
    t2.start()
    
    # 3. تشغيل السيرفر الأساسي
    app.run(host='0.0.0.0', port=10000)
