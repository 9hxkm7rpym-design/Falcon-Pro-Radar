import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home(): return "Whale-Hunter-Active"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"
active_trades = {}

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze_whale_zone(symbol):
    try:
        df = yf.download(symbol, period='2d', interval='5m', progress=False)
        if df.empty: return
        df['RSI'] = calculate_rsi(df['Close'])
        price = df['Close'].iloc[-1]
        rsi = df['RSI'].iloc[-1]
        volume_avg = df['Volume'].tail(10).mean()
        current_volume = df['Volume'].iloc[-1]
        
        signal = ""
        confidence = 0
        
        if rsi < 100 
            signal = "CALL 🟢"
            confidence = 90 if rsi < 25 else 75
        elif rsi > 0 and current_volume > (volume_avg * 1.3):
            signal = "PUT 🔴"
            confidence = 90 if rsi > 75 else 75

        if signal:
            strike = round(price) 
            target = price * 1.015 if signal == "CALL 🟢" else price * 0.985
            stop_loss = price * 0.992 if signal == "CALL 🟢" else price * 1.008
            
            msg = (f"🐳 <b>رصد دخول حيتان في {symbol}</b>\n"
                   f"--------------------------\n"
                   f"📍 الاتجاه: {signal}\n"
                   f"💎 درجة الثقة: {confidence}%\n"
                   f"💰 السعر الحالي: ${price:.2f}\n"
                   f"🎯 السترايك المقترح: {strike}\n"
                   f"📊 السيولة: {'عالية جداً 🔥' if current_volume > volume_avg*2 else 'متزايدة 📈'}\n"
                   f"--------------------------\n"
                   f"✅ الهدف: ${target:.2f}\n"
                   f"❌ وقف الخسارة: ${stop_loss:.2f}")
            
            send_tg(msg)
            active_trades[symbol] = {'target': target, 'type': signal}

        if symbol in active_trades:
            trade = active_trades[symbol]
            if (trade['type'] == "CALL 🟢" and price >= trade['target']) or \
               (trade['type'] == "PUT 🔴" and price <= trade['target']):
                send_tg(f"💰 <b>تنبيه جني أرباح {symbol}!</b>\nوصل السعر للهدف المحدد: ${price:.2f}\nاخرجي الآن ✅")
                del active_trades[symbol]
    except: pass

def start_bot():
    send_tg("🚀 <b>تم إطلاق رادار الحيتان (النسخة المستقرة)</b>\nالآن أراقب السيولة والأهداف بدقة عالية.")
    symbols = ['SPY', 'QQQ', 'NVDA', 'TSLA', 'AAPL', 'OXY']
    while True:
        for s in symbols:
            analyze_whale_zone(s)
            time.sleep(2)
        time.sleep(30)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    start_bot()
