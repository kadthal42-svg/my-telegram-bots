import random, string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "9282102705:AAHEExuvYDgE8kTrxo4qm54aieGm1LT9KtY"
BOT_USERNAME = "Mickyram_bot"

batches = {}
current_batch = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # User Link click chesi vachinappudu
    if context.args:
        code = context.args[0]
        if code in batches:
            await update.message.reply_text("Videos vasthunnayi mama! Wait...")
            for file_id in batches[code]:
                await update.message.reply_video(video=file_id)
            return
    await update.message.reply_text("Hi mama! 10 videos pampali ante /batch kottu")

async def batch_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_batch.clear()
    await update.message.reply_text("Ok mama! Ippudu 10 videos pampu, ayyaka /done kottu")

async def collect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        current_batch.append(update.message.video.file_id)
        await update.message.reply_text(f"{len(current_batch)}/10 vachayi mama!")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = "BQ" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    batches[code] = current_batch.copy()
    link = f"https://t.me/{BOT_USERNAME}?start={code}"

    keyboard = [
        [InlineKeyboardButton("PREVIEW : CLICK HERE", url="https://t.me/NEE_PREVIEW_CHANNEL")],
        [InlineKeyboardButton("POST LINK 👇", url="https://t.me/NEE_POST_LINK")],
        [InlineKeyboardButton("HOW TO DOWNLOAD : CLICK HERE", url="https://t.me/NEE_TUTORIAL")],
        [InlineKeyboardButton("JOIN BACKUP : CLICK HERE", url="https://t.me/NEE_BACKUP_CHANNEL")],
    ]
    await update.message.reply_text(
        f"Ready mama! Idhigo Link:\n{link}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    current_batch.clear()

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("batch", batch_start))
app.add_handler(CommandHandler("done", done))
app.add_handler(MessageHandler(filters.VIDEO, collect))
app.run_polling()
