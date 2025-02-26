import os
import telebot
import requests
import random

# Configuración del bot de Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

# Plantillas de mensajes
MESSAGES = [
    "🔥 ¡No te lo pierdas! {title} está en oferta. 💸\n\n💰 Antes: {old_price}\n✅ Ahora: {new_price}\n\n🛒 ¡Aprovecha esta oferta aquí! 👇\n🔗 {affiliate_link}",
    "🚀 ¡Oferta especial en {title}! 🎯\n\nAntes costaba {old_price}, pero ahora solo {new_price}. 💥\n\n🔗 ¡Compra ahora antes de que se agote! {affiliate_link}",
    "🎉 ¡Descuento disponible en {title}! 🎉\n\n🔻 Antes: {old_price}\n🔺 Ahora: {new_price}\n\nNo dejes pasar esta ganga. Compra aquí: {affiliate_link}",
    "🔥 ¡Descuento increíble en {title}! 🔥\n\n💲 Antes: {old_price}\n💲 Ahora: {new_price}\n\n🔗 Consíguelo ya aquí: {affiliate_link}",
    "🛒 ¡Oferta limitada en {title}! 🕒\n\n💸 Precio anterior: {old_price}\n🔥 Ahora solo: {new_price}\n\nAprovecha la oportunidad: {affiliate_link}",
]

# Función para obtener información del producto
def get_product_info(url):
    product_info = {
        "title": "Ejemplo de Producto",
        "image": "https://image-url.com/product.jpg",
        "old_price": "50 USD",
        "new_price": "35 USD",
        "affiliate_link": url  # Usamos directamente el enlace que envías
    }
    return product_info

# Comando /producto para recibir información del producto
@bot.message_handler(commands=["producto"])
def send_product_info(message):
    try:
        url = message.text.split(" ")[1]  # Extraer el enlace del mensaje
        product = get_product_info(url)

        # Elegir una plantilla aleatoria
        text = random.choice(MESSAGES).format(**product)

        # Enviar mensaje con imagen
        bot.send_photo(CHAT_ID, product["image"], caption=text, parse_mode="MarkdownV2")

    except IndexError:
        bot.send_message(CHAT_ID, "❌ Debes enviar un enlace después de /producto")

# Iniciar el bot
print("Bot iniciado...")
bot.polling()
