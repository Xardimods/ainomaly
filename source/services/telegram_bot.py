import os
import asyncio
import telegram
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.effective_chat:
    chat_id = update.effective_chat.id
    
    if update.message:
      if update.message.text:
        await context.bot.send_message(chat_id=chat_id, text=update.message.text)

logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if update.effective_chat:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Soy AInomaly. ¡Puedo detectar anomaías!")

if __name__ == '__main__':
    if BOT_TOKEN:
      application = ApplicationBuilder().token(BOT_TOKEN).build()
    
      start_handler = CommandHandler('start', start)
      echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

      application.add_handler(start_handler)
      application.add_handler(echo_handler)

      application.run_polling()