import os
import telebot
from flask import Flask
from threading import Thread
import time
import yfinance as yf

# التوكن الجديد حق بوت صيد الاسهم
TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "634887309"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# القائمة الكاملة اللي طلبتها
WATCHLIST = ['NVDA', 'TSLA', 'AMZN', 'OXY', 'AAPL', 'MSFT', 'QQQ', '^SPX']

@app.route('/')
def home(): return "Falcon Radar is Active! 🦅"

# ميزة الرد الآلي عشان تتأكد إن البوت يسمعك
@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
    bot.reply_to(message, "🦅 هلا والله يا سلطان! رادار الفالكون شغال الحين وجالس يراقب (NVDA, TSLA, AMZN, OXY, AAPL, MSFT, QQQ, SPX). أبشر بالسعد!")

def scanner():
    while True:
        # ملاحظة: السوق مقفل اليوم الأحد، فبيرسل لك أسعار الإغلاق
        for s in WATCHLIST:
            try:
                ticker = yf.Ticker(s)
                data = ticker.history(period='1d')
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    name = "SPX (سباكس)" if s == '^SPX' else s
                    msg = f"🦅 رادار الفالكون:\n📊 السهم: {name}\n💰 السعر الحالي: ${current_price:.2f}"
                    bot.send_message(CHAT_ID, msg)
                    time.sleep(5) # انتظار بسيط بين الرسائل
            except: pass
        
        # يرسل تحديث كل ساعة (تقدر تغيرها لاحقاً)
        time.sleep(3600)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # تشغيل الرادار في الخلفية
    Thread(target=scanner).start()
    # تشغيل ميزة الرد على الرسائل
    Thread(target=run_bot).start()
    # تشغيل السيرفر لربطه بـ Render
    app.run(host='0.0.0.0', port=10000)
