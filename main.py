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
    send_tg("⚙️ <b>بدء فحص النظام النهائي...</b>")
    
    symbol = 'NVDA'
    try:
        # جلب البيانات
        data = yf.download(symbol, period='5d', interval='1m')
        # تحويل السعر لرقم بسيط
        price = float(data['Close'].iloc[-1])
        
        target = price * 1.015
        stop_loss = price * 0.99
        
        msg = (f"🐳 <b>تجربة صيد حيتان ناجحة!</b>\n"
               f"--------------------------\n"
               f"📍 السهم: {symbol}\n"
               f"💰 السعر الحالي: {price:.2f}\n"
               f"✅ الهدف: {target:.2f}\n"
               f"❌ الستوب: {stop_loss:.2f}\n"
               f"--------------------------\n"
               f"🚀 البوت الآن جاهز 100% ليوم الاثنين!")
        send_tg(msg)
    except Exception as e:
        send_tg(f"حدث خطأ بسيط: {str(e)}")

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    start_test()
