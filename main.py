import telebot
import yfinance as yf
from flask import Flask
from threading import Thread

TOKEN = "8308789681:AAFLJuVqqQ3Jqtgth51in4IZpN1X_1aZYAE"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "Stealth Bot Active 🕵️‍♂️"

@bot.message_handler(func=lambda message: True)
def get_price(message):
    symbol = message.text.upper()
    bot.reply_to(message, f"🔍 جاري فحص {symbol} بهوية مموهة...")
    try:
        ticker = yf.Ticker(symbol)
        # هذا السطر هو اللي بيجيب البيانات غصب عن ياهو
        data = ticker.history(period='1d', interval='1m')
        if not data.empty:
            price = data['Close'].iloc[-1]
            bot.send_message(message.chat.id, f"✅ السعر لـ {symbol}: ${price:.2f}")
        else:
            bot.send_message(message.chat.id, "❌ ياهو رافض يعطي بيانات حالياً (صيانة ويكند).")
    except:
        bot.send_message(message.chat.id, "⚠️ حصل خطأ في الاتصال.")

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.infinity_polling()
