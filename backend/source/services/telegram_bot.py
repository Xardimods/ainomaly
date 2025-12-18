import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# 1. Creamos un conjunto (set) para guardar las IDs únicas de los usuarios.
# Nota: En un bot real profesional, esto debería guardarse en una base de datos 
# para no perderse si apagas la PC.
SUBSCRIBED_USERS = set()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        chat_id = update.effective_chat.id
        user_name = update.effective_user.first_name
        
        # 2. Guardamos al usuario en nuestra lista
        SUBSCRIBED_USERS.add(chat_id)
        
        logging.info(f"Nuevo usuario registrado: {user_name} ({chat_id})")
        
        await context.bot.send_message(
            chat_id=chat_id, 
            text=f"Hola {user_name}, soy AInomaly. ¡Te he registrado para recibir alertas de anomalías!"
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        chat_id = update.effective_chat.id
        if update.message and update.message.text:
            # Responde solo al usuario que escribió
            await context.bot.send_message(chat_id=chat_id, text=f"Recibido: {update.message.text}")

# 3. Función extra para simular una alerta a TODOS los usuarios
async def send_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alert_text = "🚨 ¡ANOMALÍA DETECTADA! 🚨"
    
    if not SUBSCRIBED_USERS:
        await update.message.reply_text("No hay usuarios registrados para alertar.")
        return

    # Recorremos la lista de usuarios y enviamos el mensaje a cada uno
    for user_id in SUBSCRIBED_USERS:
        try:
            await context.bot.send_message(chat_id=user_id, text=alert_text)
        except Exception as e:
            logging.error(f"No se pudo enviar alerta a {user_id}: {e}")
            
    await update.message.reply_text(f"Alerta enviada a {len(SUBSCRIBED_USERS)} usuarios.")

if __name__ == '__main__':
    if BOT_TOKEN:
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        start_handler = CommandHandler('start', start)
        alert_handler = CommandHandler('alerta', send_alert) # Nuevo comando
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

        application.add_handler(start_handler)
        application.add_handler(alert_handler)
        application.add_handler(echo_handler)

        print("AInomaly está corriendo...")
        application.run_polling()