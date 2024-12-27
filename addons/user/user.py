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

        if not message.reply_to_message.text.startswith("CC:"):
            await message.reply("No se encontró ninguna tarjeta en el mensaje.")
            return

        try:
            await message.reply_to_message.forward(CHANNEL_ID)
        except Exception as e:
            await message.reply(f"Error al reenviar al canal: {str(e)}")
            return

        owner_notification = f"El Usuario @{message.from_user.username} envió una Live al canal."
        await client.send_message(OWNER_ID, owner_notification)

        await message.reply("La tarjeta ha sido reenviada al canal correctamente.")

    except Exception as e:
        await message.reply(f"Ha ocurrido un error: {str(e)}")
