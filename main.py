import asyncio
import feedparser
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ======================
# CONFIGURACIÓN
# ======================
TOKEN = "AQUÍ_TU_TOKEN_DEL_BOT"
CHANNEL_ID = "@VIDALTYT11k"  # Tu canal de YouTube (username)
YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCYpVz5dM2pRWb6TQF7gB8zA"  # ID de tu canal
TELEGRAM_CHAT_ID = -1002713828219  # ID del grupo donde notificar

last_video_id = None


# ======================
# FUNCIONES
# ======================

def get_latest_video():
    """Obtiene el video más reciente del feed RSS de YouTube."""
    feed = feedparser.parse(YOUTUBE_RSS)
    if not feed.entries:
        return None
    entry = feed.entries[0]
    return {
        "title": entry.title,
        "link": entry.link,
        "published": entry.published,
        "id": entry.yt_videoid
    }


async def notify_new_video(app):
    """Verifica cada minuto si hay un nuevo video."""
    global last_video_id
    while True:
        video = get_latest_video()
        if video and video["id"] != last_video_id:
            last_video_id = video["id"]
            text = f"📢 Nuevo video subido:\n\n🎬 *{video['title']}*\n🔗 {video['link']}"
            await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode="Markdown")
        await asyncio.sleep(60)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 ¡Hola! Usa /notify para ver el último video del canal.")


async def notify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = get_latest_video()
    if video:
        text = f"🎬 Último video:\n\n*{video['title']}*\n🔗 {video['link']}"
        await update.message.reply_text(text, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ No pude obtener los videos del canal.")


# ======================
# MAIN
# ======================

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("notify", notify))

    # Iniciar verificador de nuevos videos en segundo plano
    app.job_queue.run_once(lambda _: asyncio.create_task(notify_new_video(app)), 5)

    print("✅ Bot iniciado correctamente.")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
