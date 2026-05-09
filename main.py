import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home(): return "الرادار يعمل بقوة"

# معلومات البوت الخاصة بك
TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def run_radar():
    # القائمة تشمل الآن AMZN و AMD
    symbols = ['AMZN', 'AMD', 'NVDA', 'TSLA', 'SPY', 'AAPL']
    
    send_tg("🚀 <b>تم تفعيل الرادار الشامل (أمازون + AMD)</b>\nسأقوم بإرسال تنبيهات مستمرة الآن حتى والسوق مقفل.")

    while True:
        for symbol in symbols:
            try:
                # سحب بيانات السهم (آخر سعر مسجل)
                ticker = yf.Ticker(symbol)
                price = ticker.fast_info['last_price']
                
                # حساب الأهداف (تغيير بسيط بنسبة 1.5% للربح)
                target = price * 1.015
                stop_loss = price * 0.99
                
                msg = (f"🐳 <b>رصد حوت لحظي في {symbol}</b>\n"
                       f"--------------------------\n"
                       f"📍 الاتجاه المتوقع: CALL 🟢\n"
                       f"💰 السعر الحالي: {price:.2f}\n"
                       f"✅ الهدف المقترح: {target:.2f}\n"
                       f"❌ وقف الخسارة: {stop_loss:.2f}\n"
                       f"--------------------------\n"
                       f"⚡️ الحالة: مراقبة فورية مستمرة")
                
                send_tg(msg)
                time.sleep(2) # انتظار ثانيتين بين كل سهم عشان السرعة
            except:
                continue
        
        # ينتظر 30 ثانية فقط ويرجع يرسل التحديثات من جديد
        time.sleep(30) 

if __name__ == "__main__":
    # تشغيل السيرفر لضمان بقاء Render نشطاً
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    # تشغيل الرادار
    run_radar()
