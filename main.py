import telebot
import time
import yfinance as yf
import pandas_ta as ta
from flask import Flask
from threading import Thread
from datetime import datetime

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "634887309"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

WATCHLIST = ['NVDA', 'TSLA', 'AMZN', 'OXY', 'AAPL', 'MSFT', 'QQQ', '^SPX']

@app.route('/')
def home(): return "Falcon Night-Rider Active! 🦅"

def get_signal_strength(rsi):
    if rsi <= 30 or rsi >= 70:
        return "🔥 قوية جداً"
    elif (40 >= rsi > 30) or (60 <= rsi < 70):
        return "⚡️ متوسطة"
    else:
        return "⚪️ ضعيفة"

def analyzer():
    while True:
        now = datetime.now().strftime("%H:%M")
        for s in WATCHLIST:
            try:
                # إضافة prepost=True لجلب بيانات التداول الليلي وما قبل الافتتاح
                data = yf.download(s, period='1d', interval='15m', prepost=True, progress=False)
                
                if data.empty: continue

                data['RSI'] = ta.rsi(data['Close'], length=14)
                cp = data['Close'].iloc[-1]
                rsi_val = data['RSI'].iloc[-1]
                
                # تخطي القيم الفارغة للـ RSI
                if rsi_val is None or str(rsi_val) == 'nan': continue

                strength = get_signal_strength(rsi_val)
                name = "SPX (سباكس)" if s == '^SPX' else s
                
                msg = (f"🦅 **رادار الفالكون - تداول ليلي**\n\n"
                       f"📊 السهم: {name}\n"
                       f"💰 السعر الحالي: ${float(cp):.2f}\n"
                       f"📉 RSI: {float(rsi_val):.2f}\n"
                       f"💪 القوة: {strength}\n"
                       f"⏰ توقيت الرصد: {now}")
                
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                time.sleep(3) # سرعة في الإرسال
            except Exception as e:
                print(f"Error: {e}")
        
        # يحلل كل 15 دقيقة عشان يواكب التداول الليلي السريع
        time.sleep(900)

if __name__ == "__main__":
    bot.send_message(CHAT_ID, "🌙 **تم تفعيل رادار التداول الليلي.**\nسأبدأ برصد التحركات الآن حتى قبل افتتاح السوق الرسمي.")
    Thread(target=analyzer, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
