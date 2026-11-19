import os, threading, random, string
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = "Mickyram_bot"
print("BOT STARTED...")

app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot Alive!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

batches = {}
current_batch = []
batch_mode = False

def make_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Hi! Pic / Video pettu!")
        return
    code = context.args[0]
    if code in batches:
        for f_type, file_id in batches[code]:
            if f_type == "photo":
                await update.message.reply_photo(photo=file_id)
            else:
                await update.message.reply_video(video=file_id)
    else:
        await update.message.reply_text("Link expired!")

async def batch_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    batch_mode = True
    current_batch.clear()
    await update.message.reply_text("Multiple pettu! Aipoyaka /done kottu!")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    if not current_batch:
        batch_mode = False
        await update.message.reply_text("Emi pettaledhu!")
        return
    sid = make_id()
    batches[sid] = current_batch.copy()
    link = f"https://t.me/{BOT_USERNAME}?start={sid}"
    await update.message.reply_text(f"Done!\nShort ID: {sid}\nLink: {link}")
    current_batch.clear()
    batch_mode = False

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global batch_mode
    batch_mode = False
    current_batch.clear()
    await update.message.reply_text("Cancel!")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message or update.channel_post
    if not msg: return
    if msg.text and msg.text.startswith("/"): return

    file_id = None; f_type = None
    if msg.photo:
        file_id = msg.photo[-1].file_id; f_type = "photo"
    elif msg.video:
        file_id = msg.video.file_id; f_type = "video"
    elif msg.document:
        file_id = msg.document.file_id; f_type = "photo"
    elif msg.animation:
        file_id = msg.animation.file_id; f_type = "video"
    else:
        return

    global batch_mode
    # MULTIPLE MODE lo unte list lo add cheyyi
    if batch_mode:
        current_batch.append([f_type, file_id])
        await msg.reply_text(f"{len(current_batch)} vachayi! Inka pettu, leka /done kottu!")
        return

    # SINGLE PIC / VIDEO - Just Short ID
    sid = make_id()
    batches[sid] = [[f_type, file_id]]
    link = f"https://t.me/{BOT_USERNAME}?start={sid}"
    await msg.reply_text(f"Short ID: {sid}\nLink: {link}")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("batch", batch_cmd))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(MessageHandler(filters.ALL, handle_all))
    app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
