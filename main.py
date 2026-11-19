import os
import threading
import random, string
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = "Mickyram_bot"
print(f"TOKEN UNDHA? {'YES' if TOKEN else 'NO'}")

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

async def test_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot LIVE lo undhi mama! ✅ Ippudu Pic pettu!")

async def batch_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    batch_mode = True
    current_batch.clear()
    await update.message.reply_text("Ok mama! 🔥 Pic ledha Video Pettu! Aipoyaka /done kottu!")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    batch_mode = False
    current_batch.clear()
    await update.message.reply_text("Cancel ayyindhi mama! ✅ Ippudu Pic pettu!")

async def debug_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message or update.channel_post
    if not msg:
        return
    if msg.text and msg.text.startswith("/"):
        return
    print(f"DEBUG: photo={bool(msg.photo)} video={bool(msg.video)} doc={bool(msg.document)}")
    await msg.reply_text("Message vachindhi mama! ✅ Chusthunna...")
    global batch_mode
    file_id = None
    f_type = None
    if msg.photo:
        file_id = msg.photo[-1].file_id
        f_type = "photo"
    elif msg.video:
        file_id = msg.video.file_id
        f_type = "video"
    elif msg.document:
        file_id = msg.document.file_id
        mime = msg.document.mime_type or ""
        f_type = "video" if "video" in mime else "photo"
    elif msg.animation:
        file_id = msg.animation.file_id
        f_type = "video"
    else:
        await msg.reply_text("Idhi Pic / Video kaadhu mama! Pic pettu!")
        return
    if batch_mode:
        current_batch.append((f_type, file_id))
        await msg.reply_text(f"{len(current_batch)}/10 vachayi mama! Inka pettu, leka /done kottu!")
        return
    short_id = make_short_code()
    batches[short_id] = [(f_type, file_id)]
    link = f"https://t.me/{BOT_USERNAME}?start={short_id}"
    await msg.reply_text(f"Done mama! ✅\n\nShort ID:\n`{short_id}`\n\nLink:\n{link}", parse_mode="Markdown")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    if not current_batch:
        batch_mode = False
        await update.message.reply_text("Emi pettaledhu mama! Batch Close chesa!")
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
    print("BOT STARTED - POLLING MODALO KI VELTHUNDHI...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_cmd))
    app.add_handler(CommandHandler("batch", batch_start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.ALL, debug_all), group=1)
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
