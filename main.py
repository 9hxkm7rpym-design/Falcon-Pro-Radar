import telebot
import yfinance as yf
import pandas_ta as ta
from flask import Flask
from threading import Thread
import time

# --- الإعدادات (جاهزة بالتوكن حقك) ---
TOKEN = "7018512629:AAGgCHUnPn2gU2uo-d8fneC-fpquxyTHdMs"
CHAT_ID = "634887309"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# قائمة الشركات اللي تتابعها
WATCHLIST = ['NVDA', 'TSLA', 'AMZN', 'OXY']

@app.route('/')
def home(): 
    return "Falcon Radar is Online! 🦅"

def analyze_market(symbol):
    try:
        # جلب بيانات 15 دقيقة (للمضاربة السريعة واليومية)
        df = yf.download(symbol, period='5d', interval='15m', progress=False)
        if df.empty or len(df) < 20: return None
        
        # 1. تحليل المؤشرات (RSI)
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        # 2. تحليل الشمعات (SMC - Hammer & Engulfing)
        df['hammer'] = ta.cdl_pattern(df['Open'], df['High'], df['Low'], df['Close'], name="hammer")
        df['engulfing'] = ta.cdl_pattern(df['Open'], df['High'], df['Low'], df['Close'], name="engulfing")
        
        current = df.iloc[-1]
        avg_vol = df['Volume'].mean()
        
        score = 0
        signals = []

        # فحص سيولة الحيتان (SMC Volume)
        if current['Volume'] > avg_vol * 1.5:
            score += 3
            signals.append("🐳 سيولة حيتان ضخمة")
        
        # فحص شمعات الارتداد (تأكيد الدخول)
        if current['hammer'] != 0 or current['engulfing'] != 0:
            score += 3
            signals.append("🔥 شمعة ارتداد (تأكيد)")

        # فحص مناطق التشبع (RSI)
        if current['RSI'] < 35:
            score += 2
            signals.append("📉 منطقة قاع (رخيص)")

        # إرسال التنبيه إذا وجدنا أي إشارة (قوية أو متوسطة)
        if score >= 3:
            stars = "⭐⭐⭐" if score >= 6 else "⭐"
            status = "فرصة ذهبية" if score >= 6 else "فرصة للمراقبة"
            
            # حساب الأهداف المقترحة (3% و 5% من سعر السهم)
            target1 = current['Close'] * 1.03
            target2 = current['Close'] * 1.05
            
            msg = (f"🎯 **رادار الفالكون PRO: {symbol}**\n\n"
                   f"💪 القوة: {stars} ({status})\n"
                   f"📊 الإشارات: {' + '.join(signals)}\n"
                   f"💰 السعر الحالي: ${current['Close']:.2f}\n\n"
                   f"💡 **توصية الأوبشن:**\n"
                   f"Strike: {round(current['Close'])} CALL\n"
                   f"الهدف الأول: ${target1:.2f}\n"
                   f"الهدف الثاني: ${target2:.2f}\n\n"
                   f"⚠️ تابع السيولة عند المقاومة!")
            return msg
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return None
    return None

def run_scanner():
    while True:
        for s in WATCHLIST:
            try:
                alert = analyze_market(s)
                if alert:
                    bot.send_message(CHAT_ID, alert)
                    time.sleep(5) # تجنب الحظر من تليجرام
            except:
                pass
        time.sleep(600) # يشيّك كل 10 دقائق

if __name__ == "__main__":
    # مسح أي ويب هوك قديم لضمان العمل
    bot.remove_webhook()
    # تشغيل الرادار في خلفية السيرفر
    Thread(target=run_scanner).start()
    # تشغيل السيرفر ليبقى البوت حياً 24 ساعة
    app.run(host='0.0.0.0', port=10000)
