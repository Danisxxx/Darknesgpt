import random
from datetime import datetime
from pyrogram import Client
from configs._def_main_ import *

CHANNEL_ID = -1002385679696
OWNER_ID = 7202754124

random_names = ["Juan", "Carlos", "Lucía", "Ana", "Pedro"]
random_surnames = ["González", "Pérez", "López", "Martínez", "Rodríguez"]

@rex('drop')
async def drop_card(client, message):
    try:
        # Verifica si el mensaje es una respuesta a otro mensaje
        if not message.reply_to_message:
            await message.reply("Por favor, responde a un mensaje que contenga una tarjeta.")
            return

        original_text = message.reply_to_message.text
        card_line = [line for line in original_text.splitlines() if line.startswith("CC:")]
        
        if not card_line:
            await message.reply("No se encontró ninguna tarjeta en el mensaje.")
            return

        # Extrae el número de la tarjeta
        card = card_line[0].replace("CC:", "").strip()

        # Generación de datos aleatorios
        name = random.choice(random_names)
        surname = random.choice(random_surnames)
        email = f"{name.lower()}.{surname.lower()}@example.com"
        today = datetime.now().strftime("%d-%m-%Y")

        # Información del usuario que envió el mensaje
        username = message.from_user.username or "Desconocido"
        user_id = message.from_user.id

        # Formato del mensaje que se enviará al canal
        channel_message = (
            f"CC: {card} / {name} {surname} | {email} | {today} "
            f"Username: @{username}"
        )

        # Intentamos enviar el mensaje al canal
        try:
            # Enviamos el mensaje al canal utilizando el ID del canal
            await client.send_message(CHANNEL_ID, channel_message)
        except Exception as e:
            await message.reply(f"Error al enviar al canal: {str(e)}")
            return

        # Notificación al propietario (OWNER_ID)
        owner_notification = f"El Usuario @{username} envió una Live al canal."
        await client.send_message(OWNER_ID, owner_notification)

        # Confirmación de que la tarjeta fue enviada correctamente
        await message.reply("La tarjeta ha sido enviada al canal correctamente.")

    except Exception as e:
        # Si ocurre un error, lo capturamos y mostramos un mensaje
        await message.reply(f"Ha ocurrido un error: {str(e)}")
