import os
import telebot
from flask import Flask
from threading import Thread
import time

# تثبيت المكتبات الأساسية تلقائياً
os.system('pip install pyTelegramBotAPI yfinance flask')

import yfinance as yf

# إعدادات البوت (التوكن حقك جاهز)
TOKEN = "7018512629:AAGgCHUnPn2gU2uo-d8fneC-fpquxyTHdMs"
CHAT_ID = "634887309"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# القائمة المحدثة (الأسهم الأربعة + سباكس)
WATCHLIST = ['NVDA', 'TSLA', 'AMZN', 'OXY', '^SPX']

@app.route('/')
def home(): return "Falcon Radar is Active! 🦅"

def scanner():
    while True:
        for s in WATCHLIST:
            try:
                # جلب بيانات السهم
                ticker = yf.Ticker(s)
                data = ticker.history(period='1d')
                
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    name = "SPX (سباكس)" if s == '^SPX' else s
                    
                    # تنبيه بسيط يطمنك إن البوت شغال
                    msg = (f"🦅 **رادار الفالكون يراقب الآن:**\n\n"
                           f"📊 السهم: {name}\n"
                           f"💰 السعر الحالي: ${current_price:.2f}\n"
                           f"🕒 الحالة: يراقب السيولة...")
                    
                    bot.send_message(CHAT_ID, msg)
                    time.sleep(5) 
            except:
                pass
        
        # يكرر الفحص كل ساعة (عشان ما يزعجك والسوق مقفل)
        time.sleep(3600)

if __name__ == "__main__":
    Thread(target=scanner).start()
    app.run(host='0.0.0.0', port=10000)
