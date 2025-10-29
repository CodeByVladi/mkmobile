import os
import asyncio
import feedparser
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# Configuración
YOUTUBE_CHANNEL_ID = "UCq1UqQdA7NNeWn8U-W9oZTw"  # Canal de YouTube
TELEGRAM_CHAT_ID = -1002713828219  # Grupo de Telegram
CHECK_INTERVAL = 300  # Cada 5 minutos
last_video_id = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot desde Render (variable de entorno)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ Falta la variable BOT_TOKEN en Render")

# Obtener el último video publicado
def get_latest_video():
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
    feed = feedparser.parse(feed_url)
    if feed.entries:
        video = feed.entries[0]
        return {
            "id": video.yt_videoid,
            "title": video.title,
            "url": video.link
        }
    return None

# Comando /notify → envía el último video
async def notify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = get_latest_video()
    if video:
        msg = f"📢 **Nuevo video de VIDAL:**\n🎬 {video['title']}\n🔗 {video['url']}"
        await context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ No se encontró ningún video en el canal.")

# Tarea que revisa nuevos videos
async def check_new_videos(application: Application):
    global last_video_id
    while True:
        video = get_latest_video()
        if video and video["id"] != last_video_id:
            last_video_id = video["id"]
            msg = f"📢 **Nuevo video de VIDAL:**\n🎬 {video['title']}\n🔗 {video['url']}"
            await application.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="Markdown")
            logger.info(f"Nuevo video notificado: {video['title']}")
        await asyncio.sleep(CHECK_INTERVAL)

# Iniciar el bot
async def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("notify", notify_command))

    # Iniciar verificación automática en segundo plano
    application.job_queue.run_once(lambda _: asyncio.create_task(check_new_videos(application)), 1)

    print("✅ Bot de notificación de YouTube iniciado correctamente.")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
