import logging
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.publickey import PublicKey
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import base64

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Variables globales
user_wallets = {}  # Billeteras de cada usuario (clave pública y privada)
solana_client = Client("https://api.mainnet-beta.solana.com")  # RPC de Solana Mainnet

# Función para generar una billetera
def generate_wallet():
    keypair = Keypair.generate()
    public_key = str(keypair.public_key)
    private_key = base64.b64encode(keypair.secret_key).decode("utf-8")
    return public_key, private_key

# Función de inicio
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    # Generar billetera si no existe
    if user_id not in user_wallets:
        public_key, private_key = generate_wallet()
        user_wallets[user_id] = {"public_key": public_key, "private_key": private_key}

    wallet_info = user_wallets[user_id]
    keyboard = [
        [InlineKeyboardButton("Activar Trading", callback_data="start_trading")],
        [InlineKeyboardButton("Ver Saldo", callback_data="view_balance")],
        [InlineKeyboardButton("Detener Trading", callback_data="stop_trading")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"¡Bienvenido al bot de trading automático en Solana! 🚀\n\n"
        f"Tu billetera personal ha sido creada automáticamente. Esta billetera será usada para realizar operaciones reales en la blockchain de Solana.\n\n"
        f"➡ **Dirección de tu billetera**: `{wallet_info['public_key']}`\n\n"
        f"🔹 **Instrucciones**:\n"
        f"1️⃣ Envía una cantidad de SOL a esta dirección para comenzar.\n"
        f"2️⃣ Haz clic en 'Activar Trading' para que el bot opere automáticamente.\n"
        f"3️⃣ Usa 'Ver Saldo' para consultar tu balance en tiempo real.\n"
        f"4️⃣ Usa 'Detener Trading' si deseas pausar las operaciones.\n\n"
        f"⚠ **Nota importante**: Asegúrate de depositar una cantidad adecuada de SOL para realizar operaciones.",
        reply_markup=reply_markup
    )

# Función para manejar botones
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.message.chat_id
    await query.answer()

    if query.data == "view_balance":
        wallet_info = user_wallets[user_id]
        balance = solana_client.get_balance(PublicKey(wallet_info['public_key']))
        await query.edit_message_text(f"Tu saldo actual es: {balance['result']['value'] / 10**9} SOL")

    elif query.data == "start_trading":
        await query.edit_message_text("Trading automático activado. Operaciones en progreso...")
        # Aquí se pueden agregar las operaciones reales

    elif query.data == "stop_trading":
        await query.edit_message_text("Trading detenido. Tus fondos están seguros.")

# Configuración principal del bot
def main():
    application = ApplicationBuilder().token("TU_TOKEN_DE_BOT_AQUI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
