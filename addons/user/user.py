from datetime import datetime
import random
from configs._def_main_ import *
from pyrogram import Client

# ///hola/// Configuración del Owner, canal y el bot administrador
OWNER_ID = 7202754124
CHANNEL_ID = -1002385679696
BOT_TOKEN = "7598417720:AAFxF0E1COsem5DY9glYav9urxaGACK1PC8"  # Reemplaza con el token del bot @Exzzex_bot
EXZZEX_BOT = Client("exzzex_bot", bot_token=BOT_TOKEN)

# ///hola/// Listas de nombres y apellidos aleatorios
random_names = ["Carlos", "María", "Juan", "Ana", "Luis", "Lucía"]
random_surnames = ["Pérez", "García", "Rodríguez", "López", "Martínez", "Sánchez"]

@rex('drop')
async def drop_card(client, message):
    """
    Comando .drop que envía la tarjeta al canal usando el bot @Exzzex_bot.
    """
    # Verifica que el comando responda a un mensaje
    if not message.reply_to_message:
        await message.reply("Por favor, responde a un mensaje que contenga una tarjeta.")
        return

    # Extraer el texto del mensaje respondido
    original_text = message.reply_to_message.text

    # Buscar la tarjeta en el texto (después de "CC:")
    card_line = [line for line in original_text.splitlines() if line.startswith("CC:")]
    if not card_line:
        await message.reply("No se encontró ninguna tarjeta en el mensaje.")
        return

    # Extrae la tarjeta quitando el "CC: "
    card = card_line[0].replace("CC:", "").strip()

    # Generar nombre, apellido, correo y fecha aleatorios
    name = random.choice(random_names)
    surname = random.choice(random_surnames)
    email = f"{name.lower()}.{surname.lower()}@example.com"
    today = datetime.now().strftime("%d-%m-%Y")

    # Obtener información del usuario que ejecutó el comando
    username = message.from_user.username or "Desconocido"
    user_id = message.from_user.id

    # Formatear el mensaje para enviar al canal
    channel_message = (
        f"CC: {card} / {name} {surname} | {email} | {today} "
        f"Username: @{username}"
    )

    # Enviar el mensaje al canal usando el bot @Exzzex_bot
    async with EXZZEX_BOT:
        await EXZZEX_BOT.send_message(CHANNEL_ID, channel_message)

    # Notificar al Owner
    owner_notification = f"El Usuario @{username} envió una Live al canal."
    await client.send_message(OWNER_ID, owner_notification)

    # Confirmación para el usuario
    await message.reply("La tarjeta ha sido enviada al canal correctamente.")
