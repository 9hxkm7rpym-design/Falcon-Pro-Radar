import os

# أمر إجباري لتثبيت المكتبات قبل أي شيء آخر
os.system('pip install pyTelegramBotAPI yfinance pandas pandas-ta flask')

import telebot
import yfinance as yf
import pandas_ta as ta
from flask import Flask
from threading import Thread
import time

TOKEN = "7018512629:AAGgCHUnPn2gU2uo-d8fneC-fpquxyTHdMs"
CHAT_ID = "634887309"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Falcon is Live!"

def scanner():
    while True:
        for s in ['NVDA', 'TSLA', 'AMZN', 'OXY']:
            try:
                df = yf.download(s, period='5d', interval='15m', progress=False)
                if not df.empty:
                    rsi = ta.rsi(df['Close'], length=14).iloc[-1]
                    if rsi < 35:
                        bot.send_message(CHAT_ID, f"🎯 فرصة قنص: {s}\nالسبب: السهم رخيص (RSI: {rsi:.1f})")
            except: pass
        time.sleep(600)

if __name__ == "__main__":
    Thread(target=scanner).start()
    app.run(host='0.0.0.0', port=10000)
