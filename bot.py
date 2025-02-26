import os
import requests
import telegram
from telegram.ext import Updater, CommandHandler

# Cargar variables de entorno
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AFFILIATE_ID = os.getenv("ALIEXPRESS_AFFILIATE_ID")

bot = telegram.Bot(token=TOKEN)

def get_product_info(product_url):
    """Obtiene la información del producto de AliExpress."""
    response = requests.get(f"https://api.aliexpress.com/product?url={product_url}&aff_id={AFFILIATE_ID}")
    data = response.json()
    
    if not data.get("success"):
        return None

    return {
        "title": data["title"],
        "old_price": data["old_price"],
        "new_price": data["new_price"],
        "image": data["image_url"],
        "url": data["affiliate_link"]
    }

def send_product(update, context):
    """Comando de Telegram para publicar un producto en el canal."""
    if len(context.args) == 0:
        update.message.reply_text("Por favor, envía un enlace de AliExpress.")
        return

    product_url = context.args[0]
    product = get_product_info(product_url)

    if not product:
        update.message.reply_text("No se pudo obtener la información del producto.")
        return

    # Crear mensaje dinámico
    message = f"🔥 *{product['title']}* 🔥\n"
    message += f"💲 Antes: {product['old_price']}\n"
    message += f"✅ Ahora: {product['new_price']}\n"
    message += f"[Comprar aquí]({product['url']})"

    # Enviar mensaje con imagen
    bot.send_photo(chat_id=CHAT_ID, photo=product["image"], caption=message, parse_mode="Markdown")

# Configurar el bot
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("publicar", send_product))

# Iniciar el bot
updater.start_polling()
updater.idle()
