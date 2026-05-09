import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Radar is Online"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def run_radar():
    symbols = ['AMZN', 'AMD', 'NVDA', 'TSLA', 'AAPL', 'OXY']
    send_tg("🚀 <b>تم تحديث الرادار بنجاح</b>\nسيتم تقييم قوة الفرص الآن.")
    while True:
        for symbol in symbols:
            try:
                df = yf.download(symbol, period='1d', interval='15m', prepost=True, progress=False)
                if df.empty: continue
                price = df['Close'].iloc[-1]
                delta = df['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rsi = 100 - (100 / (1 + (gain.iloc[-1] / loss.iloc[-1])))
                
                if rsi < 30 or rsi > 70: strength = "قوية جداً 🔥"
                elif rsi < 45 or rsi > 55: strength = "متوسطة 🟠"
                else: strength = "ضعيفة ⚠️"

                msg = (f"🎯 <b>فرصة: {symbol}</b>\n"
                       f"📊 القوة: {strength}\n"
                       f"💰 السعر: {price:.2f}\n"
                       f"📈 RSI: {rsi:.1f}\n"
                       f"🌃 تشمل التداول الليلي")
                send_tg(msg)
                time.sleep(2)
            except: continue
        time.sleep(180)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
