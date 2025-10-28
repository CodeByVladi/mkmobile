# Bot de Telegram - Mortal Kombat Mobile

## Descripción
Bot de Telegram para consultar información de packs de Mortal Kombat Mobile y recibir notificaciones de nuevos videos.

## Fecha de Creación
28 de octubre de 2025

## Características
- Consulta de packs disponibles de MK Mobile
- Búsqueda de packs específicos
- Visualización de videos recientes
- Sistema de suscripción para notificaciones de nuevos videos
- Base de datos PostgreSQL para almacenar packs y videos

## Tecnologías
- Python 3.11
- python-telegram-bot
- PostgreSQL (via SQLAlchemy)
- psycopg2-binary

## Estructura del Proyecto
- `main.py` - Bot de Telegram con comandos y lógica principal
- `database.py` - Modelos de base de datos y conexión
- `.gitignore` - Archivos ignorados por git

## Comandos del Bot
- `/start` - Mensaje de bienvenida
- `/help` - Ayuda
- `/packs` - Ver todos los packs disponibles
- `/pack [nombre]` - Buscar un pack específico
- `/videos` - Ver videos recientes
- `/subscribe` - Suscribirse a notificaciones
- `/unsubscribe` - Desuscribirse
- `/addpack` - Agregar nuevo pack (admin)
- `/addvideo` - Agregar nuevo video y notificar suscriptores (admin)

## Configuración

### Secretos Necesarios (Secrets)
1. **TELEGRAM_BOT_TOKEN** (Obligatorio)
   - Ve a Telegram y busca @BotFather
   - Envía /newbot y sigue las instrucciones
   - Copia el token y agrégalo en Secrets con la clave TELEGRAM_BOT_TOKEN

2. **ADMIN_CHAT_IDS** (Obligatorio para comandos de admin)
   - Para obtener tu chat ID, habla con @userinfobot en Telegram
   - Agrega tu chat ID en Secrets con la clave ADMIN_CHAT_IDS
   - Si hay múltiples admins, separa los IDs con comas: 123456789,987654321
   - Si no se configura, los comandos /addpack y /addvideo estarán deshabilitados por seguridad

### Base de Datos
- DATABASE_URL se configura automáticamente por Replit
- Las tablas se crean automáticamente al iniciar el bot
- Para agregar datos de ejemplo, ejecuta: `python example_data.py`

## Cambios Recientes
- 28/10/2025: Creación inicial del bot
  - Integración con PostgreSQL
  - Comandos para consultar packs
  - Sistema de notificaciones de videos
  - Suscripción de usuarios
