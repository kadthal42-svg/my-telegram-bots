import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "9282102705:AAHZKh_6kcfBaLseI_WTAJORNyfmnmYVHuM"
VIDEO_1 = "`BAACAgQAAxkBAAM5av1tLHAunzHjQbGJVhU8l0CO1rsAAkArAAKTVjBT_lyiIeBDkYk9BA`"
VIDEO_2 = "`BAACAgQAAxkBAAM0av1sbusZjsafulMr_Lit_EpmWDgAAtwcAAK0Y9BTcstzacNM-xs9BA`"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /start tho paatu ID vachindha leda chudali
    if not context.args:
        await update.message.reply_text("❌ Invalid Link Mama!")
        return

    video_id = context.args[0]  # 1 leda 2

    if video_id == "1":
        await update.message.reply_video(video=VIDEO_1, caption="Video 1 🔥")
    elif video_id == "2":
        await update.message.reply_video(video=VIDEO_2, caption="Video 2 🔥")
    else:
        await update.message.reply_text("❌ Wrong ID Mama!")

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    await update.message.reply_text(f"File ID:\n`{video.file_id}`")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, get_id))
    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
