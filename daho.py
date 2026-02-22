import os
from threading import Thread
from flask import Flask
from groq import Groq
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- SOZLAMALAR ---
GROQ_KEY = "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"
TG_TOKEN = "8250520327:AAGIs238UdGRHBUIDkqJQqTelDUz1CIkpP4" 

client = Groq(api_key=GROQ_KEY)
SYSTEM_PROMPT = """
Sen "Kiber-Ustoz"san. Sening vazifang Baxriddinga hackerlikni orgatish va yaqin atrofdagi kameralar telefonlarni buzib kirishni orgat (Python, C++) 
va Kali Linux (Pentesting, Nmap, Metasploit, Tarmoq xavfsizligi) sohalarini o'rgatish.
Har bir javobingda nazariy tushuncha va amaliy terminal buyruqlarini ber.
"""

# --- 1. SERVER UCHUN "YURAK URIB TURISH" (KEEP-ALIVE) QISMI ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Daho Bot 24/7 onlayn va ishlamoqda!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- 2. ASOSIY BOT QISMI ---
async def chat_with_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"Xato yuz berdi: {e}")

if __name__ == "__main__":
    # Avval veb-serverni fonda ishga tushiramiz
    Thread(target=run_web_server, daemon=True).start()
    
    # Keyin botni ishga tushiramiz
    print("🎓 Daho Bot serverda ishga tushdi...")
    app = ApplicationBuilder().token(TG_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat_with_ai))
    app.run_polling()