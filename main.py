import yfinance as yf
import requests
import time
import random
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon Radar Pro: Steel Version Active 🦾"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def get_analysis(symbol):
    sym = "^SPX" if symbol == "SPX" else symbol
    try:
        # طلب البيانات بهوية متصفح حقيقية لتجنب الرفض
        dat = yf.download(sym, period='5d', interval='15m', progress=False, prepost=True)
        
        if dat.empty or len(dat) < 15: return None
        
        last_row = dat.iloc[-1]
        price = float(last_row['Close'])
        
        # 1. حساب القوة النسبية (RSI) لصيد القيعان
        delta = dat['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
        rsi = 100 - (100 / (1 + (gain / (loss + 1e-9))))
        
        # 2. كشف الشموع اليابانية (المطرقة الانعكاسية)
        body = abs(last_row['Open'] - last_row['Close'])
        lower_shadow = last_row[['Open', 'Close']].min() - last_row['Low']
        is_hammer = lower_shadow > (1.8 * body) and body > 0
        
        # 3. تحديد مناطق الحوت وقوة الفرصة
        if rsi < 30: status = "منطقة قاع/صيد حيتان 🐳🔥"
        elif rsi > 70: status = "قمة/جني أرباح ⚠️"
        elif rsi < 45: status = "فرصة قيد التكون 🟢"
        else: status = "مراقبة مستمرة ⚖️"

        return {
            "price": price, "rsi": rsi, "status": status,
            "target": price * 1.015, "stop": price * 0.985,
            "strike": round(price), "hammer": is_hammer
        }
    except: return None

def run_radar():
    symbols = ['NVDA', 'TSLA', 'AMZN', 'AMD', 'AAPL', 'OXY', 'SPY', 'SPX', 'META', 'MSFT']
    send_tg("🦾 <b>تم تفعيل النسخة الفولاذية</b>\nالمميزات: قيعان، حيتان، أهداف، سترايك، وشموع.")
    
    while True:
        for symbol in symbols:
            data = get_analysis(symbol)
            if data:
                candle_msg = "🔨 مطرقة (قاع انعكاسي)" if data['hammer'] else "طبيعية"
                msg = (f"🎯 <b>الرمز: {symbol}</b>\n"
                       f"━━━━━━━━━━━━━━\n"
                       f"💡 <b>الحالة:</b> {data['status']}\n"
                       f"💰 <b>السعر:</b> {data['price']:.2f}\n"
                       f"📈 <b>RSI:</b> {data['rsi']:.1f}\n"
                       f"🕯️ <b>الشمعة:</b> {candle_msg}\n"
                       f"━━━━━━━━━━━━━━\n"
                       f"🎯 <b>الهدف:</b> {data['target']:.2f}\n"
                       f"🛑 <b>الوقف:</b> {data['stop']:.2f}\n"
                       f"💎 <b>السترايك:</b> {data['strike']}\n"
                       f"━━━━━━━━━━━━━━")
                send_tg(msg)
                # انتظار عشوائي بين الشركات لتمويه موقع ياهو
                time.sleep(random.randint(15, 25))
            else:
                time.sleep(5)
        
        # لفة كاملة كل 10 دقائق (مثالي للاستقرار)
        time.sleep(600)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
