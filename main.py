import yfinance as yf
import requests
import time
import pandas_ta as ta
from threading import Thread
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "رادار القيعان والسيولة اللحظي نشط"

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
CHAT_ID = "1068286006"

def send_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
    except: pass

def get_market_analysis(symbol):
    try:
        # سحب بيانات تشمل التداول الليلي prepost=True
        df = yf.download(symbol, period='1d', interval='5m', prepost=True, progress=False)
        if df.empty: return None
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        price = last['Close']
        
        # 1. تحليل الشموع والقيعان (Hammer Detection)
        body = abs(last['Close'] - last['Open'])
        lower_shadow = last['Open'] - last['Low'] if last['Close'] > last['Open'] else last['Close'] - last['Low']
        is_bottom_candle = lower_shadow > (body * 2) # شمعة ارتداد من قاع
        
        # 2. مؤشر RSI
        df['RSI'] = ta.rsi(df['Close'], length=14)
        rsi_val = df['RSI'].iloc[-1]
        
        # 3. تقييم قوة الفرصة (Logic)
        if (rsi_val < 30 or rsi_val > 70) and is_bottom_candle:
            strength = "قوية جداً 🔥 (منطقة حيتان)"
            stars = "⭐⭐⭐"
        elif (rsi_val < 40 or rsi_val > 60):
            strength = "متوسطة 🟠 (فرصة جيدة)"
            stars = "⭐⭐"
        else:
            strength = "ضعيفة ⚠️ (مخاطرة عالية)"
            stars = "⭐"
            
        return {
            "price": price, "rsi": rsi_val, "strength": strength, 
            "stars": stars, "is_bottom": is_bottom_candle
        }
    except: return None

def run_radar():
    symbols = ['AMZN', 'AMD', 'NVDA', 'TSLA', 'AAPL', 'OXY']
    send_tg("🕵️‍♂️ <b>بدء الرادار الشامل (قيعان + سيولة + تداول ليلي)</b>\nسأرسل لك كل الفرص مع تقييم قوتها.")

    while True:
        for symbol in symbols:
            data = get_market_analysis(symbol)
            if data:
                direction = "CALL 🟢" if data['rsi'] < 55 else "PUT 🔴"
                target = data['price'] * 1.015 if "CALL" in direction else data['price'] * 0.985
                
                msg = (f"🔍 <b>تنبيه الرادار: {symbol}</b>\n"
                       f"--------------------------\n"
                       f"📊 القوة: <b>{data['strength']}</b> {data['stars']}\n"
                       f"📍 الاتجاه المتوقع: {direction}\n"
                       f"💰 السعر الحالي: {data['price']:.2f}\n"
                       f"📈 مؤشر RSI: {data['rsi']:.1f}\n"
                       f"🏠 القيعان: {'رصد ارتداد من قاع ✅' if data['is_bottom'] else 'لا يوجد شكل قاع واضح ❌'}\n"
                       f"🎯 الهدف المقترح: {target:.2f}\n"
                       f"--------------------------\n"
                       f"🌃 يشمل التداول الليلي | يعمل الآن")
                
                send_tg(msg)
                time.sleep(1) # سرعة التنقل بين الأسهم
        
        # انتظار دقيقتين قبل الجولة القادمة لضمان الاستمرارية
        time.sleep(120) 

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    run_radar()
