import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from database import init_db, get_session, MKPack, Video, Subscriber

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Admin chat IDs (configure this with your Telegram user ID)
ADMIN_IDS = set()
admin_ids_env = os.getenv('ADMIN_CHAT_IDS', '')
if admin_ids_env:
    ADMIN_IDS = set(admin_ids_env.split(','))

def is_admin(chat_id: str) -> bool:
    """Check if user is an admin. Returns False if no admins are configured."""
    if len(ADMIN_IDS) == 0:
        logger.warning("ADMIN_CHAT_IDS not configured - admin commands are disabled")
        return False
    return chat_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"¡Hola {user.mention_html()}! 👋\n\n"
        f"Soy tu bot de Mortal Kombat Mobile.\n\n"
        f"Comandos disponibles:\n"
        f"/start - Mostrar este mensaje\n"
        f"/packs - Ver todos los packs disponibles\n"
        f"/pack [nombre] - Buscar un pack específico\n"
        f"/videos - Ver videos recientes\n"
        f"/subscribe - Suscribirse a notificaciones de nuevos videos\n"
        f"/unsubscribe - Desuscribirse de notificaciones\n"
        f"/help - Ayuda\n"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "📱 Bot de Mortal Kombat Mobile\n\n"
        "Comandos disponibles:\n\n"
        "/packs - Muestra todos los packs disponibles en MK Mobile\n"
        "/pack <nombre> - Busca información de un pack específico\n"
        "/videos - Muestra los videos más recientes\n"
        "/subscribe - Recibe notificaciones cuando haya nuevos videos\n"
        "/unsubscribe - Deja de recibir notificaciones\n"
        "/addpack - [Admin] Agregar un nuevo pack\n"
        "/addvideo - [Admin] Agregar un nuevo video\n"
    )

async def list_packs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all available MK Mobile packs"""
    session = get_session()
    try:
        packs = session.query(MKPack).filter_by(available=True).all()
        
        if not packs:
            await update.message.reply_text(
                "😔 No hay packs disponibles en este momento.\n"
                "Usa /addpack para agregar uno."
            )
            return
        
        message = "🎮 <b>Packs de Mortal Kombat Mobile</b>\n\n"
        for pack in packs:
            # Determinar el costo
            if pack.souls_cost > 0:
                cost = f"👻 {pack.souls_cost} almas"
            elif pack.crystals_cost > 0:
                cost = f"💎 {pack.crystals_cost} cristales"
            elif pack.price > 0:
                cost = f"💰 ${pack.price} {pack.currency}"
            else:
                cost = "🎁 Gratis"
            
            message += f"📦 <b>{pack.name}</b>\n   {cost}\n"
            
            if pack.description:
                message += f"   📝 {pack.description[:100]}...\n"
            message += "\n"
        
        await update.message.reply_html(message)
    finally:
        session.close()

async def search_pack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search for a specific pack"""
    if not context.args:
        await update.message.reply_text(
            "Por favor, especifica el nombre del pack.\n"
            "Ejemplo: /pack Scorpion"
        )
        return
    
    search_term = ' '.join(context.args)
    session = get_session()
    try:
        packs = session.query(MKPack).filter(
            MKPack.name.ilike(f'%{search_term}%')
        ).all()
        
        if not packs:
            await update.message.reply_text(
                f"❌ No se encontró ningún pack con '{search_term}'"
            )
            return
        
        message = f"🔍 <b>Resultados para '{search_term}':</b>\n\n"
        for pack in packs:
            # Determinar el costo
            if pack.souls_cost > 0:
                cost = f"👻 {pack.souls_cost} almas"
            elif pack.crystals_cost > 0:
                cost = f"💎 {pack.crystals_cost} cristales"
            elif pack.price > 0:
                cost = f"💰 ${pack.price} {pack.currency}"
            else:
                cost = "🎁 Gratis"
            
            message += f"📦 <b>{pack.name}</b>\n   {cost}\n"
            
            if pack.description:
                message += f"   📝 {pack.description}\n"
            message += "\n"
        
        await update.message.reply_html(message)
    finally:
        session.close()

async def list_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List recent videos"""
    session = get_session()
    try:
        videos = session.query(Video).order_by(Video.published_at.desc()).limit(5).all()
        
        if not videos:
            await update.message.reply_text(
                "😔 No hay videos disponibles.\n"
                "Usa /addvideo para agregar uno."
            )
            return
        
        message = "🎬 <b>Videos Recientes</b>\n\n"
        for video in videos:
            date = video.published_at.strftime('%d/%m/%Y')
            message += (
                f"▶️ <b>{video.title}</b>\n"
                f"   📅 {date}\n"
                f"   🔗 {video.url}\n"
            )
            if video.description:
                message += f"   📝 {video.description[:100]}...\n"
            message += "\n"
        
        await update.message.reply_html(message)
    finally:
        session.close()

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Subscribe to video notifications"""
    chat_id = str(update.effective_chat.id)
    username = update.effective_user.username or "Usuario"
    
    session = get_session()
    try:
        existing = session.query(Subscriber).filter_by(chat_id=chat_id).first()
        
        if existing:
            if existing.active:
                await update.message.reply_text(
                    "✅ Ya estás suscrito a las notificaciones!"
                )
            else:
                existing.active = True
                session.commit()
                await update.message.reply_text(
                    "✅ Te has suscrito nuevamente a las notificaciones de videos!"
                )
        else:
            subscriber = Subscriber(chat_id=chat_id, username=username)
            session.add(subscriber)
            session.commit()
            await update.message.reply_text(
                "✅ ¡Te has suscrito a las notificaciones!\n"
                "Recibirás un mensaje cuando haya nuevos videos."
            )
    finally:
        session.close()

async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unsubscribe from video notifications"""
    chat_id = str(update.effective_chat.id)
    
    session = get_session()
    try:
        subscriber = session.query(Subscriber).filter_by(chat_id=chat_id).first()
        
        if subscriber and subscriber.active:
            subscriber.active = False
            session.commit()
            await update.message.reply_text(
                "❌ Te has desuscrito de las notificaciones."
            )
        else:
            await update.message.reply_text(
                "❌ No estabas suscrito a las notificaciones."
            )
    finally:
        session.close()

async def add_pack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new pack (admin command)"""
    chat_id = str(update.effective_chat.id)
    
    if not is_admin(chat_id):
        await update.message.reply_text(
            "❌ No tienes permisos para usar este comando.\n"
            "Solo los administradores pueden agregar packs."
        )
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /addpack <nombre> <precio> [almas] [descripción]\n"
            "Ejemplo: /addpack \"Diamond Pack\" 29.99 800 \"Pack con personajes diamante\""
        )
        return
    
    try:
        name = context.args[0]
        price = float(context.args[1])
        souls_cost = int(context.args[2]) if len(context.args) > 2 else None
        description = ' '.join(context.args[3:]) if len(context.args) > 3 else None
        
        session = get_session()
        try:
            pack = MKPack(
                name=name,
                price=price,
                souls_cost=souls_cost,
                description=description
            )
            session.add(pack)
            session.commit()
            
            await update.message.reply_text(
                f"✅ Pack '{name}' agregado exitosamente!"
            )
        finally:
            session.close()
    except (ValueError, IndexError) as e:
        await update.message.reply_text(
            f"❌ Error al agregar pack: {str(e)}\n"
            "Verifica el formato del comando."
        )

async def add_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add a new video and notify subscribers"""
    chat_id = str(update.effective_chat.id)
    
    if not is_admin(chat_id):
        await update.message.reply_text(
            "❌ No tienes permisos para usar este comando.\n"
            "Solo los administradores pueden agregar videos."
        )
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso: /addvideo <título> <url> [descripción]\n"
            "Ejemplo: /addvideo \"Nuevo personaje\" https://youtu.be/xxx \"Video sobre nuevo personaje\""
        )
        return
    
    try:
        title = context.args[0]
        url = context.args[1]
        description = ' '.join(context.args[2:]) if len(context.args) > 2 else None
        
        session = get_session()
        try:
            video = Video(
                title=title,
                url=url,
                description=description
            )
            session.add(video)
            session.commit()
            
            # Get the video ID before closing session
            video_id = video.id
            
            await update.message.reply_text(
                f"✅ Video '{title}' agregado exitosamente!"
            )
            
            session.close()
            
            # Notify subscribers (outside of session)
            await notify_subscribers(context, video_id)
            
        except Exception as inner_error:
            session.rollback()
            raise inner_error
        finally:
            if session.is_active:
                session.close()
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error al agregar video: {str(e)}"
        )

async def notify_subscribers(context: ContextTypes.DEFAULT_TYPE, video_id: int):
    """Notify all subscribers about a new video"""
    session = get_session()
    try:
        # Get video and subscribers
        video = session.query(Video).filter_by(id=video_id).first()
        if not video:
            logger.error(f"Video with ID {video_id} not found")
            return
        
        subscribers = session.query(Subscriber).filter_by(active=True).all()
        
        message = (
            f"🎬 <b>¡Nuevo Video!</b>\n\n"
            f"▶️ <b>{video.title}</b>\n"
            f"🔗 {video.url}\n"
        )
        if video.description:
            message += f"📝 {video.description}\n"
        
        # Track successful and failed notifications
        success_count = 0
        fail_count = 0
        
        for subscriber in subscribers:
            try:
                await context.bot.send_message(
                    chat_id=subscriber.chat_id,
                    text=message,
                    parse_mode='HTML'
                )
                success_count += 1
            except Exception as e:
                logger.error(f"Error notifying {subscriber.chat_id}: {e}")
                fail_count += 1
        
        # Mark video as notified
        video.notified = True
        session.commit()
        
        logger.info(f"Notified {success_count} subscribers, {fail_count} failures")
        
    except Exception as e:
        logger.error(f"Error in notify_subscribers: {e}")
        session.rollback()
    finally:
        session.close()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables!")
        print("\n" + "="*60)
        print("ERROR: TELEGRAM_BOT_TOKEN no está configurado!")
        print("="*60)
        print("\nPara configurar tu token de Telegram:")
        print("1. Ve a la pestaña de Secretos (🔒 en la barra lateral)")
        print("2. Agrega un nuevo secreto:")
        print("   - Clave: TELEGRAM_BOT_TOKEN")
        print("   - Valor: Tu token de @BotFather")
        print("\nPara obtener un token:")
        print("1. Abre Telegram y busca @BotFather")
        print("2. Envía /newbot y sigue las instrucciones")
        print("3. Copia el token y agrégalo a Secretos")
        print("="*60 + "\n")
        return
    
    # Initialize database
    try:
        init_db()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")
        return
    
    application = Application.builder().token(token).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("packs", list_packs))
    application.add_handler(CommandHandler("pack", search_pack))
    application.add_handler(CommandHandler("videos", list_videos))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("addpack", add_pack))
    application.add_handler(CommandHandler("addvideo", add_video))
    
    application.add_error_handler(error_handler)
    
    logger.info("Bot started successfully! Press Ctrl+C to stop.")
    print("\n" + "="*60)
    print("✅ Bot de Mortal Kombat Mobile está funcionando!")
    print("="*60)
    print("\n¡Ve a Telegram y busca tu bot para comenzar a chatear!")
    print("="*60 + "\n")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
