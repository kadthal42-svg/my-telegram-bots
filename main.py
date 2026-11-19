import os, random, string, asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = "Mickyram_bot"

app_flask = Flask(__name__)
batches = {}
current_batch = []
batch_mode = False

def make_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

async def delete_after_5min(context, chat_id, msg_ids):
    await asyncio.sleep(300)  # 5 Min
    for mid in msg_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=mid)
        except:
            pass
    # Delete ayyaka User ki Notification
    try:
        await context.bot.send_message(chat_id=chat_id, text="⏰ 5 Mins ayipoyayi! Ee Files Auto Delete ayyayi!")
    except:
        pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Hi! Pic / Video pettu!")
        return
    code = context.args[0]
    if code in batches:
        # 1. User ki Notification - Mundhe
        await update.message.reply_text("⚠️ Ee Files 5 Min lo Auto Delete avthayi! Ventane Save chesukondi!")

        sent_ids = []
        for f_type, file_id in batches[code]:
            if f_type == "photo":
                m = await update.message.reply_photo(photo=file_id)
            else:
                m = await update.message.reply_video(video=file_id)
            sent_ids.append(m.message_id)

        # 2. 5 Min taruvatha Delete + Notification
        asyncio.create_task(delete_after_5min(context, update.effective_chat.id, sent_ids))
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
    if batch_mode:
        current_batch.append([f_type, file_id])
        await msg.reply_text(f"{len(current_batch)} vachayi! Inka pettu, leka /done kottu!")
        return
    sid = make_id()
    batches[sid] = [[f_type, file_id]]
    link = f"https://t.me/{BOT_USERNAME}?start={sid}"
    await msg.reply_text(f"Short ID: {sid}\nLink: {link}")

app_bot = Application.builder().token(TOKEN).build()
app_bot.add_handler(CommandHandler("start", start))
app_bot.add_handler(CommandHandler("batch", batch_cmd))
app_bot.add_handler(CommandHandler("done", done))
app_bot.add_handler(CommandHandler("cancel", cancel))
app_bot.add_handler(MessageHandler(filters.ALL, handle_all))

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(app_bot.initialize())

@app_flask.route('/')
def home():
    return "Bot Alive - Webhook Mode FIXED!"

@app_flask.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, app_bot.bot)
        loop.run_until_complete(app_bot.process_update(update))
    except Exception as e:
        print(f"WEBHOOK ERROR: {e}")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
