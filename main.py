import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random, string

TOKEN = os.getenv("TOKEN")
print(f"TOKEN LENGTH CHECK: {len(TOKEN) if TOKEN else 0}")
print(f"TOKEN START CHECK: {TOKEN[:5] if TOKEN else 'NO TOKEN'}")
BOT_USERNAME = "Mickyram_bot"

# Dummy Website - Render kosam
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Mickyram Bot is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

batches = {}
current_batch = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        code = context.args[0]
        if code in batches:
            await update.message.reply_text("Videos vasthunnayi mama!")
            for file_id in batches[code]:
                await update.message.reply_video(video=file_id)
            return
    await update.message.reply_text("Hi mama! /batch kottu")

async def batch_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_batch.clear()
    await update.message.reply_text("Ok mama! 10 videos pampu, /done kottu")

async def collect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        current_batch.append(update.message.video.file_id)
        await update.message.reply_text(f"{len(current_batch)}/10 vachayi!")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    code = "BQ" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    batches[code] = current_batch.copy()
    link = f"https://t.me/{BOT_USERNAME}?start={code}"
    keyboard = [
        [InlineKeyboardButton("PREVIEW : CLICK HERE", url="https://t.me/NEE_PREVIEW")],
        [InlineKeyboardButton("POST LINK 👇", url="https://t.me/NEE_POST")],
        [InlineKeyboardButton("HOW TO DOWNLOAD : CLICK HERE", url="https://t.me/NEE_TUTORIAL")],
        [InlineKeyboardButton("JOIN BACKUP : CLICK HERE", url="https://t.me/NEE_BACKUP")],
    ]
    await update.message.reply_text(f"Ready mama! Link:\n{link}", reply_markup=InlineKeyboardMarkup(keyboard))
    current_batch.clear()

if __name__ == "__main__":
    # Flask ni pakkana run cheyyi
    threading.Thread(target=run_flask, daemon=True).start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("batch", batch_start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(MessageHandler(filters.VIDEO, collect))
    app.run_polling(drop_pending_updates=True)
