import random
from datetime import datetime
from pyrogram import Client
from configs._def_main_ import *

CHANNEL_ID = -1002385679696
OWNER_ID = 7202754124

@rex('drop')
async def drop_card(client, message):
    try:
        if not message.reply_to_message:
            await message.reply("Por favor, responde a un mensaje que contenga una tarjeta.")
            return

        # Verifica si el mensaje proviene de un bot
        if message.reply_to_message.from_user.is_bot:
            try:
                # Reenvía el mensaje al canal
                await message.reply_to_message.forward(CHANNEL_ID)
            except Exception as e:
                await message.reply(f"Error al reenviar el mensaje de un bot: {str(e)}")
                return
        else:
            try:
                # Si el mensaje proviene de un usuario, también lo reenvía al canal
                await message.reply_to_message.forward(CHANNEL_ID)
            except Exception as e:
                await message.reply(f"Error al reenviar el mensaje: {str(e)}")
                return

        # Notificar al owner
        owner_notification = f"El Usuario @{message.from_user.username} envió una Live al canal."
        await client.send_message(OWNER_ID, owner_notification)

        await message.reply("La tarjeta ha sido enviada al canal correctamente.")

    except Exception as e:
        await message.reply(f"Ha ocurrido un error: {str(e)}")
