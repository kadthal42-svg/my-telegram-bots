import asyncio, os, threading, random, string
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "9282102705:AAHEExuvYDgE8kTrxo4qm54aieGm1LT9KtY"

# Video lu save cheskovadaniki
VIDEOS = {}

def make_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

app_flask = Flask(__name__)
@app_flask.route('/')
def home(): return "Bot is Live!"
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# NUVVU VIDEO PAMPITHE
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.video.file_id
    code = make_code()
    VIDEOS[code] = file_id
    bot_name = (await context.bot.get_me()).username
    link = f"https://t.me/{bot_name}?start={code}"
    await update.message.reply_text(f"✅ Done!\n\n🔗 Link:\n{link}\n\nCode: {code}")

# USER LINK CLICK CHESTHE
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Video pampu mama.")
        return
    code = context.args[0]
    file_id = VIDEOS.get(code)
    if not file_id:
        await update.message.reply_text("❌ Video dorakaledhu mama, malli link tiyyu. Render restart ayyindhi.")
        return
    
    video_msg = await context.bot.send_video(chat_id=update.effective_chat.id, video=file_id)
    note_msg = await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ NOTE: This message will delete in 5 mins.\nPlease save or forward this video!")
    await asyncio.sleep(300)
    try:
        await context.bot.delete_message(update.effective_chat.id, video_msg.message_id)
        await context.bot.delete_message(update.effective_chat.id, note_msg.message_id)
        await context.bot.delete_message(update.effective_chat.id, update.message.message_id)
    except: pass

async def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, get_id))
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.initialize(); await app.start()
    await app.updater.start_polling(drop_pending_updates=True)

def start_bot_thread():
    loop = asyncio.new_event_loop(); asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot()); loop.run_forever()

if __name__ == "__main__":
    threading.Thread(target=start_bot_thread, daemon=True).start()
    run_flask()
