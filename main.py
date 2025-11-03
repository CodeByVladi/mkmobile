import asyncio
import feedparser
import time
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ======================
# CONFIGURACIÓN
# ======================
TOKEN = "8257718995:AAE0WKI_ZuYtvgzS6fe7kVkbKvFpWv0ZQgY"
CHANNEL_ID = "@VIDALTYT11k"  # Tu canal de YouTube (username)
YOUTUBE_RSS = "https://www.youtube.com/feeds/videos.xml?channel_id=UCYpVz5dM2pRWb6TQF7gB8zA"
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


async def check_new_videos(app):
    """Verifica periódicamente si hay un nuevo video."""
    global last_video_id
    while True:
        video = get_latest_video()
        if video and video["id"] != last_video_id:
            last_video_id = video["id"]
            text = f"📢 Nuevo video subido:\n\n🎬 *{video['title']}*\n🔗 {video['link']}"
            try:
                await app.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode="Markdown")
                print(f"📤 Notificado: {video['title']}")
            except Exception as e:
                print(f"⚠️ Error al enviar mensaje: {e}")
        await asyncio.sleep(60)  # Revisa cada minuto


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

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("notify", notify))

    # Ejecutar verificación de videos en segundo plano
    asyncio.create_task(check_new_videos(app))

    print("✅ Bot iniciado correctamente y escuchando comandos...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

    async def run():
        await main()

    try:
        asyncio.get_event_loop().create_task(run())
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        print("🛑 Bot detenido manualmente")

