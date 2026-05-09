import yfinance as yf
import requests
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home(): return "Ready"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def start_test():
    send_tg("⚙️ <b>بدء فحص النظام النهائي (نسخة الويكند)...</b>")
    
    symbol = 'NVDA'
    try:
        # بنسحب بيانات اليوم السابق لأن السوق مقفل الآن
        ticker = yf.Ticker(symbol)
        price = ticker.fast_info['last_price']
        
        target = price * 1.015
        stop_loss = price * 0.99
        
        msg = (f"🐳 <b>تجربة صيد حيتان ناجحة!</b>\n"
               f"--------------------------\n"
               f"📍 السهم: {symbol}\n"
               f"💰 سعر الإغلاق: {price:.2f}\n"
               f"✅ الهدف المقترح: {target:.2f}\n"
               f"❌ وقف الخسارة: {stop_loss:.2f}\n"
               f"--------------------------\n"
               f"🚀 رادار الحيتان جاهز تماماً للافتتاح!")
        send_tg(msg)
    except Exception as e:
        send_tg(f"حدث خطأ في النظام: {str(e)}")

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    start_test()
