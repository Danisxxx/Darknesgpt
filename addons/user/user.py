from datetime import datetime, timedelta
from collections import Counter
import pytz
import asyncio
from configs._def_main_ import *

# ///hola/// Diccionario para contar mensajes de cada usuario
user_messages = Counter()

# ///hola/// Owner ID y canal donde llegan los mensajes
OWNER_ID = 7202754124
CHANNEL_ID = -1002385679696

# ///hola/// Zona horaria de Venezuela
VENEZUELA_TZ = pytz.timezone('America/Caracas')

# ///hola/// Variable global para la hora de corte
cutoff_hour = 22  # Por defecto, las 10 PM

@rex('time')
async def set_cutoff_time(client, message):
    """
    Configura la hora de corte con el comando Time <hora>.
    """
    global cutoff_hour
    try:
        # ///hola/// Obtiene la hora proporcionada por el usuario
        new_hour = int(message.text.split()[1])
        if 0 <= new_hour <= 23:
            cutoff_hour = new_hour
            await message.reply(f"La hora de corte ha sido configurada a las {new_hour}:00 hora Venezuela.")
        else:
            await message.reply("Por favor, ingresa una hora válida entre 0 y 23.")
    except (IndexError, ValueError):
        await message.reply("Uso incorrecto del comando. Ejemplo: Time 8")

async def process_message(client, message):
    """
    Procesa los mensajes enviados al canal.
    """
    # ///hola/// Verifica si el mensaje contiene "Checked By"
    if "Checked By:" in message.text:
        # ///hola/// Extrae el nombre, username e ID del usuario
        checked_by_line = [line for line in message.text.splitlines() if "Checked By:" in line][0]
        name = checked_by_line.split(":")[1].split("[")[0].strip()  # Extrae el nombre
        username = message.from_user.username or "Desconocido"  # Obtiene el username
        user_id = message.from_user.id  # Obtiene el ID del usuario

        # ///hola/// Actualiza el contador de mensajes del usuario
        user_messages[(name, username, user_id)] += 1

        # ///hola/// Cuenta total del día para el usuario
        total_messages = user_messages[(name, username, user_id)]

        # ///hola/// Formato del mensaje al Owner
        notification = (
            f"Name = {name} = Username = @{username} - ID = {user_id}\n"
            f"El Usuario @{username} - {user_id} Dropeo Una Live. En total del día lleva {total_messages}."
        )
        await client.send_message(OWNER_ID, notification)

async def send_daily_summary(client):
    """
    Enviar resumen diario de usuarios que enviaron mensajes al canal.
    """
    global cutoff_hour

    while True:
        # ///hola/// Obtiene la hora actual en Venezuela
        now = datetime.now(VENEZUELA_TZ)
        next_run = (now + timedelta(days=1)).replace(hour=cutoff_hour, minute=0, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()

        # ///hola/// Espera hasta la hora configurada
        await asyncio.sleep(sleep_time)

        # ///hola/// Genera la lista de usuarios ordenados por cantidad de mensajes
        today = now.strftime('%d-%m-%Y')
        sorted_users = user_messages.most_common()
        summary = [
            f"Name = {user[0]} = Username = @{user[1]} - ID = {user[2]} Dropeo {count} Live(s)"
            for user, count in sorted_users
        ]
        summary_message = f"Tiempo Finalizado {today}:\n\n" + "\n".join(summary)

        # ///hola/// Envía el resumen al Owner
        await client.send_message(OWNER_ID, summary_message)

        # ///hola/// Limpia el contador para el próximo día
        user_messages.clear()
