import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "9282102705:AAFd0XQBTIdIbYqqMWKauWqGpIL08VglW98"
# https://t.me/+EdiBliY9sOdjZjA1
UPDATE_CHANNEL = "https://t.me/Mickyram_bot" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    if not context.args:
        await update.message.reply_text("Welcome Mama! Link tho raa.")
        return

    file_id = context.args[0]  # Idhe video file_id

    # 1. Please wait...
    wait_msg = await update.message.reply_text("Please wait...")

    try:
        # 2. Video pampadam
        video_msg = await context.bot.send_video(chat_id=chat_id, video=file_id)
    except:
        await wait_msg.edit_text("❌ Invalid Link Mama! Ee video expired ayyindhi.")
        return

    # Wait msg delete cheyyi
    await wait_msg.delete()

    # 3. Important msg + Button
    keyboard = [[InlineKeyboardButton("📢 UPDATE CHANNEL", url=UPDATE_CHANNEL)]]
    text = """⚠️ Important:
All Messages will be deleted after 5 minutes.
Please save or forward these messages to your personal saved messages to avoid losing them!"""
    
    warn_msg = await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))

    # 5 min aagu - 300 sec
    await asyncio.sleep(300)

    # Motham delete
    try:
        await context.bot.delete_message(chat_id, video_msg.message_id)
        await context.bot.delete_message(chat_id, warn_msg.message_id)
        await context.bot.delete_message(chat_id, update.message.message_id)
    except:
        pass

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
