import telebot
import yfinance as yf
from flask import Flask
from threading import Thread

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "Interactive Mode Active ✅"

# الرد على رسالة الترحيب
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "هلا بك! أنا بوت الفالكون في وضع الدردشة 🦅\n\nأرسلي لي اسم أي سهم (مثلاً: NVDA أو TSLA) وراح أعطيكِ آخر سعر له!")

# الرد على أسماء الأسهم
@bot.message_handler(func=lambda message: True)
def get_stock_price(message):
    symbol = message.text.upper()
    bot.send_message(message.chat.id, f"لحظة أشيك لك على {symbol}... 🔍")
    
    try:
        ticker = yf.Ticker(symbol)
        # جلب بيانات يوم واحد (إغلاق الجمعة)
        data = ticker.history(period='1d')
        if not data.empty:
            price = data['Close'].iloc[-1]
            bot.reply_to(message, f"💰 آخر سعر مسجل لـ {symbol} هو: {price:.2f} دولار.\n\n(تذكرِ إن السوق مقفل حالياً، وهذا سعر إغلاق الجمعة) ⚓")
        else:
            bot.reply_to(message, f"ما قدرت ألاقي بيانات لـ {symbol}. تأكدي من كتابة الرمز صح.")
    except:
        bot.reply_to(message, "حصل خطأ بسيط وأنا أدور.. جربي اسم سهم ثاني.")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
