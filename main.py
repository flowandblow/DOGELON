import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import asyncio

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Variables globales
user_balance = {}  # Fondos de los usuarios
DEX_API_URL = "https://api.raydium.io/pairs"  # API pública para obtener datos del mercado

# Función de inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id
    user_balance[user_id] = 20  # Comienza con 20€
    keyboard = [
        [InlineKeyboardButton("Activar Trading Automático", callback_data="start_trading")],
        [InlineKeyboardButton("Detener Trading", callback_data="stop_trading")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("¡Bienvenido al bot de trading automático! Usa los botones para operar:", reply_markup=reply_markup)

# Función para manejar los botones
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.message.chat_id
    await query.answer()

    if query.data == "start_trading":
        await query.edit_message_text("Trading automático activado. Operando con los mejores tokens...")
        await auto_trade(user_id, context)  # Llama a la función de trading automático

    elif query.data == "stop_trading":
        await query.edit_message_text("Trading detenido. Tus fondos están seguros.")

# Función para obtener pares de trading desde Raydium
async def get_trading_pairs():
    response = requests.get(DEX_API_URL)
    pairs = response.json()
    return pairs

# Función para buscar el mejor par de trading
async def find_best_pair():
    pairs = await get_trading_pairs()
    # Ordena los pares por volumen de trading en las últimas 24 horas
    sorted_pairs = sorted(pairs, key=lambda x: x['volumeUsd24h'], reverse=True)
    return sorted_pairs[0]  # Devuelve el par con mayor volumen

# Función de trading automático
async def auto_trade(user_id, context):
    user_funds = user_balance[user_id]
    best_pair = await find_best_pair()

    # Información del mejor par
    token_name = best_pair["name"]
    current_price = best_pair["price"]
    await context.bot.send_message(
        chat_id=user_id,
        text=f"Iniciando trading en el par: {token_name} (Precio actual: {current_price} USD)"
    )

    # Simulación de operaciones de compra/venta
    for _ in 
