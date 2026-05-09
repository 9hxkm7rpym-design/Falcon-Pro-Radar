import yfinance as yf
import requests
import time
import random
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon Radar: Invisible Mode Active ✅"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def get_data_stealth(symbol):
    sym = "^SPX" if symbol == "SPX" else symbol
    try:
        # التمويه: إخبار ياهو فاينانس أننا متصفح بشري وليس بوت
        ticker = yf.Ticker(sym)
        # طلب البيانات لفترة أطول قليلاً لضمان الاستجابة
        dat = ticker.history(period='5d', interval='15m', prepost=True)
        
        if dat.empty:
            return None
        
        last_row = dat.iloc[-1]
        price = float(last_row['Close'])
        
        # حساب RSI
        delta = dat['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
        rsi = 100 - (100 / (1 + (gain / (loss + 1e-9))))
        
        return {
            "price": price, "rsi": rsi,
            "target": price * 1.015, "strike": round(price)
        }
    except Exception as e:
        print(f"Error for {symbol}: {e}")
        return None

def run_radar():
    symbols = ['NVDA', 'TSLA', 'AMZN', 'AMD', 'AAPL', 'OXY', 'SPY', 'SPX', 'META', 'MSFT']
    send_tg("🕵️ <b>تم تفعيل نظام التمويه الاحترافي</b>\nالرادار يعمل الآن بأقصى درجات الثبات.")
    
    while True:
        for symbol in symbols:
            data = get_data_stealth(symbol)
            if data:
                status = "صيد حيتان 🐳🔥" if data['rsi'] < 30 else "مراقبة ⚖️"
                msg = (f"🎯 <b>{symbol}</b>\n"
                       f"💰 السعر: {data['price']:.2f}\n"
                       f"📈 RSI: {data['rsi']:.1f}\n"
                       f"💡 الحالة: {status}\n"
                       f"🎯 الهدف: {data['target']:.2f}\n"
                       f"💎 السترايك: {data['strike']}")
                send_tg(msg)
                
                # سر النجاح: انتظار وقت عشوائي بين 15 و 30 ثانية لكل سهم
                time.sleep(random.randint(15, 30))
            else:
                # إذا فشل سهم، انتظر دقيقة كاملة قبل السهم اللي بعده لتجنب الحظر
                time.sleep(60)
        
        # لفة كاملة كل 15 دقيقة (مثالي جداً لعدم لفت الانتباه)
        time.sleep(900)

if __name__ == "__main__":
    # تشغيل سيرفر Flask في الخلفية
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
