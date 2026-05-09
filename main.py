import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon Radar Pro: Stable Mode ✅"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"
target_tracker = {}

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def get_analysis(symbol):
    ticker_sym = "^SPX" if symbol == "SPX" else symbol
    try:
        # إضافة 'proxy' وتغيير طريقة الطلب لتجنب الرفض
        ticker = yf.Ticker(ticker_sym)
        df = ticker.history(period='2d', interval='15m', prepost=True)
        
        if df.empty or len(df) < 2: return None
        
        last_row = df.iloc[-1]
        price = last_row['Close']
        
        # حساب RSI مبسط
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
        rsi = 100 - (100 / (1 + (gain / (loss + 1e-9))))
        
        # تحليل الشموع (المطرقة)
        body = abs(last_row['Open'] - last_row['Close'])
        lower_shadow = last_row[['Open', 'Close']].min() - last_row['Low']
        is_hammer = lower_shadow > (1.8 * body) and body > 0
        
        if rsi < 30: status = "منطقة قاع/صيد حيتان 🐳🔥"
        elif rsi > 70: status = "قمة/جني أرباح ⚠️"
        else: status = "مراقبة مستمرة ⚖️"

        return {
            "price": price, "rsi": rsi, "status": status,
            "target": price * 1.015, "stop": price * 0.985,
            "strike": round(price), "hammer": is_hammer
        }
    except: return None

def run_radar():
    symbols = ['NVDA', 'TSLA', 'AMZN', 'AMD', 'AAPL', 'OXY', 'SPY', 'SPX', 'META', 'MSFT']
    send_tg("🚀 <b>تحديث: نظام الرادار مستقر الآن</b>\nجاري مراقبة الـ 10 شركات بدقة.")
    
    while True:
        for symbol in symbols:
            data = get_analysis(symbol)
            if data:
                if symbol in target_tracker and data['price'] >= target_tracker[symbol]:
                    send_tg(f"✅✅ <b>هدف محقق في {symbol}!</b>")
                    target_tracker.pop(symbol)

                candle = "🔨 مطرقة" if data['hammer'] else "طبيعية"
                msg = (f"🎯 <b>رصد: {symbol}</b>\n"
                       f"💡 <b>الحالة:</b> {data['status']}\n"
                       f"💰 <b>السعر:</b> {data['price']:.2f}\n"
                       f"📈 <b>RSI:</b> {data['rsi']:.1f}\n"
                       f"🎯 <b>الهدف:</b> {data['target']:.2f}\n"
                       f"💎 <b>السترايك:</b> {data['strike']}")
                
                send_tg(msg)
                target_tracker[symbol] = data['target']
                time.sleep(10) # زيادة وقت الانتظار لتجنب الحظر
        time.sleep(600) # فحص كل 10 دقائق والسوق مقفل

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
