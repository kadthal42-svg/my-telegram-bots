import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

FILE_ID_BOT_TOKEN = "9282102705:AAHZKh_6kcfBaLseI_WTAJORNyfmnmYVHuM"
BOT1_TOKEN = "9116495685:AAF22rs147pbc_rY5pAok3Lx3wshtyGxZLM"
BOT2_TOKEN = "9224056622:AAHBD5P4jjRKhK1jSchcGUnrY9UjKhGbI-A"

VIDEO_1 = "PASTE_VIDEO_1_FILE_ID"
VIDEO_2 = "PASTE_VIDEO_2_FILE_ID"

async def get_id(update, context):
    if update.message.video:
        await update.message.reply_text(f"File ID: `{update.message.video.file_id}`")
    else:
        await update.message.reply_text("Video pampu mama!")

async def start_file_bot(update, context):
    await update.message.reply_text("Hi mama! Video pampu, File ID istha!")

async def start_bot1(update, context):
    button = [[InlineKeyboardButton("▶️ Watch Video", url="https://t.me/YOUR_BOT2_USERNAME?start=video")]]
    await update.message.reply_text("Kindha button click cheyyi 👇", reply_markup=InlineKeyboardMarkup(button))

async def start_bot2(update, context):
    msg1 = await update.message.reply_video(video=VIDEO_1, caption="5 mins lo delete avthadi")
    msg2 = await update.message.reply_video(video=VIDEO_2, caption="5 mins lo delete avthadi")
    await asyncio.sleep(300)
    try:
        await msg1.delete()
        await msg2.delete()
    except:
        pass
async def main():
    app1 = Application.builder().token(FILE_ID_BOT_TOKEN).build()
    app1.add_handler(CommandHandler("start", start_file_bot))
    app1.add_handler(MessageHandler(filters.VIDEO, get_id))
    app2 = Application.builder().token(BOT1_TOKEN).build()
    app2.add_handler(CommandHandler("start", start_bot1))
    app3 = Application.builder().token(BOT2_TOKEN).build()
    app3.add_handler(CommandHandler("start", start_bot2))

    await asyncio.gather(
        app1.run_polling(),
        app2.run_polling(),
        app3.run_polling()
    )
    print("3 Bots Started...")

asyncio.run(main())
