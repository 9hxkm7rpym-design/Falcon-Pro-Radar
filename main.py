import telebot
import time
import yfinance as yf
import pandas_ta as ta
from flask import Flask
from threading import Thread

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "634887309"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# القائمة كاملة مع سباكس (الهدف المنشود)
WATCHLIST = ['NVDA', 'TSLA', 'AMZN', 'OXY', 'AAPL', 'MSFT', 'QQQ', '^SPX']

@app.route('/')
def home(): return "Falcon Master Analyzer is Active! 🦅"

def get_signal_strength(rsi):
    # تصنيف دقيق بناءً على مناطق الارتداد
    if rsi <= 30 or rsi >= 70:
        return "🔥 قوية جداً (منطقة انفجار)"
    elif (35 >= rsi > 30) or (65 <= rsi < 70):
        return "⚡️ متوسطة"
    else:
        return "❄️ ضعيفة (تحت المراقبة)"

def analyzer():
    while True:
        for s in WATCHLIST:
            try:
                # جلب بيانات ربع ساعة للتحليل اللحظي
                data = yf.download(s, period='2d', interval='15m', progress=False)
                if len(data) < 20: continue

                data['RSI'] = ta.rsi(data['Close'], length=14)
                
                cp = data['Close'].iloc[-1]
                rsi_val = data['RSI'].iloc[-1]
                
                strength = get_signal_strength(rsi_val)
                name = "SPX (سباكس)" if s == '^SPX' else s
                
                # إرسال التحليل
                msg = (f"🦅 **رادار الفالكون - تحليل مباشر**\n\n"
                       f"📊 السهم: {name}\n"
                       f"💰 السعر: ${cp:.2f}\n"
                       f"📉 مؤشر RSI: {rsi_val:.2f}\n"
                       f"💪 القوة: {strength}\n"
                       f"📍 التوجه: {'شراء/ارتداد' if rsi_val < 50 else 'بيع/تصحيح'}")
                
                bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                time.sleep(4) # انتظار بسيط عشان تليجرام ما يحظرنا
            except Exception as e:
                print(f"Error with {s}: {e}")
        
        # يحلل كل ساعة ويرسل لك التقرير كامل
        time.sleep(3600)

if __name__ == "__main__":
    Thread(target=analyzer, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
