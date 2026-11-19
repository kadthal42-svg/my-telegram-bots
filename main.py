import os
import threading
import random, string
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = "Mickyram_bot"

app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Mickyram Bot is Alive!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

batches = {}
current_batch = []
batch_mode = False

def make_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return
    code = context.args[0]
    if code in batches:
        for f_type, file_id in batches[code]:
            if f_type == "photo":
                await update.message.reply_photo(photo=file_id)
            else:
                await update.message.reply_video(video=file_id)
        return
    else:
        return

async def batch_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    batch_mode = True
    current_batch.clear()
    await update.message.reply_text("Ok mama! 🔥\n\nPic ledha Video Pettu!\n10 lopu enni aina pettochu!\nAipoyaka /done kottu!")

async def handle_single(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    if batch_mode:
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            current_batch.append(("photo", file_id))
        elif update.message.video:
            file_id = update.message.video.file_id
            current_batch.append(("video", file_id))
        await update.message.reply_text(f"{len(current_batch)}/10 vachayi mama! Inka pettu, leka /done kottu!")
        return

    # Single Pic / Video pedithe - SHORT ID ivvu
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        f_type = "photo"
    elif update.message.video:
        file_id = update.message.video.file_id
        f_type = "video"
    else:
        return

    short_id = make_short_code()
    batches[short_id] = [(f_type, file_id)]
    link = f"https://t.me/{BOT_USERNAME}?start={short_id}"
    await update.message.reply_text(f"Done mama! ✅\n\nShort ID:\n`{short_id}`\n\nLink:\n{link}\n\nIdhi Channel lo paste cheyyi mama!", parse_mode="Markdown")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    if not current_batch:
        await update.message.reply_text("Emi pettaledhu mama! Mundhu Pic / Video pettu!")
        return
    short_id = make_short_code()
    batches[short_id] = current_batch.copy()
    link = f"https://t.me/{BOT_USERNAME}?start={short_id}"
    keyboard = [
        [InlineKeyboardButton("PREVIEW : CLICK HERE", url="https://t.me/NEE_PREVIEW")],
        [InlineKeyboardButton("POST LINK 👇", url="https://t.me/NEE_POST")],
        [InlineKeyboardButton("HOW TO DOWNLOAD : CLICK HERE", url="https://t.me/NEE_TUTORIAL")],
        [InlineKeyboardButton("JOIN BACKUP : CLICK HERE", url="https://t.me/NEE_BACKUP")],
    ]
    await update.message.reply_text(f"Ready mama! ✅\n{len(current_batch)} Files Ready!\n\nShort ID:\n`{short_id}`\n\nLink:\n{link}", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
    current_batch.clear()
    batch_mode = False

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("batch", batch_start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_single))
    app.run_polling(drop_pending_updates=True)
