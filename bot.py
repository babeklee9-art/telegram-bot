import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TOKEN, CHANNEL_ID, ADMIN_ID
from tiktok_live import run_live

users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in users:
        users.append(update.effective_user.id)

    await update.message.reply_text("Bot aktivdir ✅")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    text = f"""
📊 Bot statistikası

👥 istifadəçi: {len(users)}
"""
    await update.message.reply_text(text)

async def send_live(link, app):
    message = f"""
🎁 TikTok Sandıq Yayımı

🔥 Canlı başladı!

🔗 {link}

Tələs qoşul!
"""
    await app.bot.send_message(chat_id=CHANNEL_ID, text=message)

async def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin))

    async def callback(link):
        await send_live(link, app)

    asyncio.create_task(run_live(callback))

    print("Bot işləyir...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
