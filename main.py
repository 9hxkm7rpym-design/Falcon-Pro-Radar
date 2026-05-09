import yfinance as yf
import requests
import time
import pandas_ta as ta
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "الرادار يعمل بنجاح"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=5)
    except: pass

def run_radar():
    symbols = ['AMZN', 'AMD', 'NVDA', 'TSLA', 'AAPL', 'OXY']
    send_tg("✅ تم تحديث النظام: الرادار جاهز الآن")
    while True:
        for symbol in symbols:
            try:
                df = yf.download(symbol, period='1d', interval='5m', prepost=True, progress=False)
                if df.empty: continue
                # حساب الـ RSI
                df.ta.rsi(append=True) 
                rsi_val = df.iloc[-1]['RSI_14']
                price = df.iloc[-1]['Close']
                
                strength = "قوية 🔥" if rsi_val < 35 or rsi_val > 65 else "عادية ⚪"
                
                msg = f"🔍 {symbol}\nالسعر: {price:.2f}\nالقوة: {strength}\nالـ RSI: {rsi_val:.1f}"
                send_tg(msg)
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(2)
        time.sleep(120)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
