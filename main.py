import yfinance as yf
import requests
import time
import random
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon Radar: Final Solution Active ✅"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def get_data_v4(symbol):
    sym = "^SPX" if symbol == "SPX" else symbol
    try:
        # التعديل السحري: إقناع ياهو إننا متصفح حقيقي
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'})
        
        ticker = yf.Ticker(sym, session=session)
        dat = ticker.history(period='2d', interval='15m', prepost=True)
        
        if dat.empty: return None
        
        price = float(dat['Close'].iloc[-1])
        delta = dat['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
        rsi = 100 - (100 / (1 + (gain / (loss + 1e-9))))
        
        return {"price": price, "rsi": rsi, "target": price * 1.015, "strike": round(price)}
    except: return None

def run_radar():
    symbols = ['NVDA', 'TSLA', 'AMZN', 'AMD', 'AAPL', 'OXY', 'SPY', 'SPX', 'META', 'MSFT']
    send_tg("🦾 <b>تم تفعيل النسخة المصفحة</b>\nالآن البوت يتصل بهوية متصفح آيفون لضمان تخطي الحظر.")
    
    while True:
        for symbol in symbols:
            data = get_data_v4(symbol)
            if data:
                status = "صيد حيتان 🐳" if data['rsi'] < 32 else "مراقبة ⚖️"
                msg = (f"🎯 <b>{symbol}</b>\n💰 السعر: {data['price']:.2f}\n📈 RSI: {data['rsi']:.1f}\n💡 الحالة: {status}\n🎯 الهدف: {data['target']:.2f}\n💎 السترايك: {data['strike']}")
                send_tg(msg)
                time.sleep(20) # راحة طويلة بين الشركات
            else:
                time.sleep(5)
        time.sleep(900)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
