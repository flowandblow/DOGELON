import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Variable global para fondos de usuario (simulada)
user_balance = {}

# Función de inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_balance[user_id] = 20  # Comienza con 20€
    keyboard = [
        [InlineKeyboardButton("Activar Trading", callback_data="start_trading")],
        [InlineKeyboardButton("Detener Trading", callback_data="stop_trading")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("¡Bienvenido al bot de trading! Usa los botones para operar:", reply_markup=reply_markup)

# Manejador de botones
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.message.chat_id
    await query.answer()

    if query.data == "start_trading":
        await query.edit_message_text("Trading activado. Operando con 20€ iniciales...")
        # Simulación de una operación de trading
        profit = user_balance[user_id] * 0.1  # Ganancia del 10%
        user_balance[user_id] += profit
        await context.bot.send_message(
            chat_id=user_id,
            text=f"Operación completada. Nuevos fondos: {user_balance[user_id]:.2f}€"
        )

    elif query.data == "stop_trading":
        await query.edit_message_text("Trading detenido. Tus fondos están seguros.")

# Configuración principal del bot
def main():
    # Sustituye "TU_TOKEN_DE_BOT_AQUI" por el token de tu bot de BotFather
    application = ApplicationBuilder().token("TU_TOKEN_DE_BOT_AQUI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
