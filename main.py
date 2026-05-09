import yfinance as yf
import requests
import time
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Falcon Radar Pro is Fully Active ✅"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

# مخزن الأهداف لمراقبة الوصول لها
target_tracker = {}

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
    except: pass

def get_analysis(symbol):
    ticker_sym = "^SPX" if symbol == "SPX" else symbol
    try:
        df = yf.download(ticker_sym, period='2d', interval='15m', prepost=True, progress=False)
        if df.empty or len(df) < 15: return None
        
        last_row = df.iloc[-1]
        price = last_row['Close']
        
        # حساب RSI يدوي دقيق
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
        rsi = 100 - (100 / (1 + (gain / (loss + 1e-9))))
        
        # تحليل الشموع (المطرقة الانعكاسية)
        body = abs(last_row['Open'] - last_row['Close'])
        lower_shadow = last_row[['Open', 'Close']].min() - last_row['Low']
        is_hammer = lower_shadow > (1.8 * body) and body > 0
        
        # تحديد حالة "الحوت" والقوة
        if rsi < 30: status = "منطقة قاع/صيد حيتان 🐳🔥"
        elif rsi > 70: status = "قمة/جني أرباح ⚠️"
        elif rsi < 45: status = "تجميع صاعد 🟢"
        else: status = "مراقبة مستمرة ⚖️"

        # حساب الأهداف والوقف والسترايك
        target = price * 1.015  # هدف 1.5%
        stop_loss = price * 0.985 # وقف 1.5%
        suggested_strike = round(price)

        return {
            "price": price, "rsi": rsi, "status": status,
            "target": target, "stop": stop_loss,
            "strike": suggested_strike, "hammer": is_hammer
        }
    except: return None

def run_radar():
    symbols = ['NVDA', 'TSLA', 'AMZN', 'AMD', 'AAPL', 'OXY', 'SPY', 'SPX', 'META', 'MSFT']
    send_tg("🚀 <b>تم تفعيل نظام الرادار المتكامل</b>\nنراقب القيعان، الأهداف، والسيولة لـ 10 شركات.")
    
    while True:
        for symbol in symbols:
            data = get_analysis(symbol)
            if data:
                # 1. تنبيه الوصول للهدف (لو السعر الحالي طلع فوق الهدف اللي رصده البوت قبل)
                if symbol in target_tracker and data['price'] >= target_tracker[symbol]:
                    send_tg(f"✅✅ <b>تم تحقيق الهدف في {symbol}!</b>\nالسعر وصل: {data['price']:.2f} 💰")
                    target_tracker.pop(symbol) # مسح الهدف بعد تحقيقه

                # 2. إرسال التقرير الشامل
                candle = "🔨 شمعة مطرقة (قاع انعكاسي)" if data['hammer'] else "طبيعية"
                msg = (f"🎯 <b>رصد: {symbol}</b>\n"
                       f"━━━━━━━━━━━━━━\n"
                       f"💡 <b>الحالة:</b> {data['status']}\n"
                       f"💰 <b>السعر الحالي:</b> {data['price']:.2f}\n"
                       f"📈 <b>RSI:</b> {data['rsi']:.1f}\n"
                       f"🕯️ <b>الشمعة:</b> {candle}\n"
                       f"━━━━━━━━━━━━━━\n"
                       f"🎯 <b>الهدف المقترح:</b> {data['target']:.2f}\n"
                       f"🛑 <b>وقف الخسارة:</b> {data['stop']:.2f}\n"
                       f"💎 <b>السترايك:</b> {data['strike']}\n"
                       f"━━━━━━━━━━━━━━")
                
                send_tg(msg)
                
                # تحديث مخزن الأهداف لمراقبتها في اللفة الجاية
                target_tracker[symbol] = data['target']
                time.sleep(5) 
        time.sleep(300) # فحص كل 5 دقائق لضمان الاستقرار التام

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
