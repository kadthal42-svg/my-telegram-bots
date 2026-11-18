import os
from flask import Flask
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

FILE_ID_BOT_TOKEN = "9282102705:AAHZKh_6kcfBaLseI_WTAJORNyfmnmYVHuM"
BOT1_TOKEN = "9116495685:AAF22rs147pbc_rY5pAok3Lx3wshtyGxZLM"
BOT2_TOKEN = "9224056622:AAHBD5P4jjRKhK1jSchcGUnrY9UjKhGbI-A"

VIDEO_1 = "`BAACAgQAAxkBAAM0av1sbusZjsafulMr_Lit_EpmWDgAAtwcAAK0Y9BTcstzacNM-xs9BA`"
VIDEO_2 = "`BAACAgQAAxkBAAM5av1tLHAunzHjQbGJVhU8l0CO1rsAAkArAAKTVjBT_lyiIeBDkYk9BA`"

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
def keep_alive():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Live!")
        def do_HEAD(self):
            self.send_response(200)
            self.end_headers()
        def log_message(self, *args):
            pass
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

threading.Thread(target=keep_alive, daemon=True).start()
async def main():
    app1 = Application.builder().token(FILE_ID_BOT_TOKEN).build()
    app1.add_handler(CommandHandler("start", start_file_bot))
    app1.add_handler(MessageHandler(filters.VIDEO, get_id))
    app2 = Application.builder().token(BOT1_TOKEN).build()
    app2.add_handler(CommandHandler("start", start_bot1))
    app3 = Application.builder().token(BOT2_TOKEN).build()
    app3.add_handler(CommandHandler("start", start_bot2))

    async with app1, app2, app3:
        await app1.start()
        await app2.start()
        await app3.start()
        await asyncio.gather(
            app1.updater.start_polling(),
            app2.updater.start_polling(),
            app3.updater.start_polling()
        )
        print("3 Bots Started...")
        await asyncio.Event().wait()

asyncio.run(main())
