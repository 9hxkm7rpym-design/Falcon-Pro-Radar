import os
import time
from threading import Thread
from flask import Flask

# محاولة تحميل المكتبات، وإذا لم تكن موجودة يتم تثبيتها تلقائياً
try:
    import telebot
    import yfinance as yf
    import pandas as pd
    import pandas_ta as ta
except ImportError:
    os.system('pip install pyTelegramBotAPI yfinance pandas pandas-ta flask')
    import telebot
    import yfinance as yf
    import pandas as pd
    import pandas_ta as ta

# --- الإعدادات ---
TOKEN = "7018512629:AAGgCHUnPn2gU2uo-d8fneC-fpquxyTHdMs"
CHAT_ID = "634887309"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# الأسهم المراد مراقبتها
WATCHLIST = ['NVDA', 'TSLA', 'AMZN', 'OXY']

@app.route('/')
def home():
    return "Falcon Radar PRO is Online! 🦅"

def analyze_market(symbol):
    try:
        # جلب بيانات 15 دقيقة
        df = yf.download(symbol, period='5d', interval='15m', progress=False)
        if df.empty or len(df) < 20:
            return None
        
        # حساب RSI
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        # كشف نماذج الشمعات (SMC)
        df['hammer'] = ta.cdl_pattern(df['Open'], df['High'], df['Low'], df['Close'], name="hammer")
        df['engulfing'] = ta.cdl_pattern(df['Open'], df['High'], df['Low'], df['Close'], name="engulfing")
        
        current = df.iloc[-1]
        avg_vol = df['Volume'].mean()
        
        score = 0
        signals = []

        # 1. سيولة الحيتان (SMC)
        if current['Volume'] > avg_vol * 1.5:
            score += 3
            signals.append("🐳 سيولة حيتان ضخمة")
        
        # 2. تأكيد الشمعات
        if current.get('hammer', 0) != 0 or current.get('engulfing', 0) != 0:
            score += 3
            signals.append("🔥 شمعة ارتداد (تأكيد SMC)")

        # 3. منطقة القاع
        if current['RSI'] < 35:
            score += 2
            signals.append("📉 منطقة قاع (RSI)")

        if score >= 3:
            stars = "⭐⭐⭐" if score >= 6 else "⭐"
            status = "فرصة ذهبية" if score >= 6 else "فرصة للمراقبة"
            target = current['Close'] * 1.03
            
            msg = (f"🎯 **رادار الفالكون PRO: {symbol}**\n\n"
                   f"💪 القوة: {stars} ({status})\n"
                   f"📊 الإشارات: {' + '.join(signals)}\n"
                   f"💰 السعر الحالي: ${current['Close']:.2f}\n\n"
                   f"💡 **توصية الأوبشن:**\n"
                   f"Strike: {round(current['Close'])} CALL\n"
                   f"الهدف: ${target:.2f}")
            return msg
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
    return None

def run_scanner():
    # انتظار بسيط لضمان استقرار السيرفر عند البدء
    time.sleep(10)
    while True:
        for s in WATCHLIST:
            try:
                alert = analyze_market(s)
                if alert:
                    bot.send_message(CHAT_ID, alert)
                    time.sleep(5)
            except Exception as e:
                print(f"Scanner error: {e}")
        # فحص كل 10 دقائق
        time.sleep(600)

if __name__ == "__main__":
    bot.remove_webhook()
    # تشغيل الفاحص في خلفية السيرفر
    Thread(target=run_scanner).start()
    # تشغيل Flask لضمان بقاء السيرفر حياً على Render
    app.run(host='0.0.0.0', port=10000)
