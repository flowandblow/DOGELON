import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Lista de tokens predefinidos
TOKENS = [
    "TOKEN_1_AQUI",
    "TOKEN_2_AQUI",
    "TOKEN_3_AQUI"
]

# Seleccionar un token aleatorio al iniciar
TELEGRAM_TOKEN = random.choice(TOKENS)

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Función de inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Bienvenido al bot dinámico!")

# Configuración principal del bot
def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
