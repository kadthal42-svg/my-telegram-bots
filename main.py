import asyncio
import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "9282102705:AAFr672ot5HqvlIe3g4iD2BFFmuY2HQVekE"
UPDATE_CHANNEL = "https://t.me/Mickyram_bot"

# 1. Flask - Render kosam
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "Bot is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)

# 2. Bot Logic - Video lo laga
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if not context.args:
        await update.message.reply_text("Welcome Mama! Link tho raa.")
        return

    file_id = context.args[0]
    wait_msg = await update.message.reply_text("Please wait...")

    try:
        video_msg = await context.bot.send_video(chat_id=chat_id, video=file_id)
    except:
        await wait_msg.edit_text("❌ Invalid Link Mama! Ee video expired ayyindhi.")
        return

    await wait_msg.delete()

    keyboard = [[InlineKeyboardButton("📢 UPDATE CHANNEL", url=UPDATE_CHANNEL)]]
    text = """⚠️ Important:
All Messages will be deleted after 5 minutes.
Please save or forward these messages to your personal saved messages to avoid losing them!"""
    
    warn_msg = await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))

    await asyncio.sleep(300)
    try:
        await context.bot.delete_message(chat_id, video_msg.message_id)
        await context.bot.delete_message(chat_id, warn_msg.message_id)
        await context.bot.delete_message(chat_id, update.message.message_id)
    except:
        pass

async def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # Paatha pending updates anni clear cheyyi - Conflict raakunda
    await app.bot.delete_webhook(drop_pending_updates=True)
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    print("Bot Started!")

def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())
    loop.run_forever()

if __name__ == "__main__":
    threading.Thread(target=start_bot_thread, daemon=True).start()
    run_flask()
