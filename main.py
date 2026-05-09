import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home(): return "Test-Active"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def start_test():
    # رسالة ترحيب
    send_tg("⚙️ <b>بدء فحص النظام (تجربة وهمية)...</b>")
    
    # تجربة سحب بيانات سهم واحد لإثبات أن البوت يقرأ السوق
    symbol = 'NVDA'
    try:
        data = yf.download(symbol, period='1d', interval='1m')
        price = data['Close'].iloc[-1]
        
        msg = (f"🐳 <b>إشارة تجريبية: رصد حيتان في {symbol}</b>\n"
               f"--------------------------\n"
               f"📍 الاتجاه: CALL 🟢 (تجربة)\n"
               f"💰 آخر سعر مسجل: ${price:.2f}\n"
               f"🎯 الهدف التجريبي: ${price * 1.01:.2f}\n"
               f"❌ وقف الخسارة: ${price * 0.99:.2f}\n"
               f"--------------------------\n"
               f"✅ إذا وصلت هذه الرسالة، فالبوت جاهز للعمل يوم الاثنين!")
        send_tg(msg)
    except Exception as e:
        send_tg(f"خطأ في التجربة: {e}")

if __name__ == "__main__":
    # تشغيل السيرفر
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    # تشغيل الفحص لمرة واحدة
    start_test()
