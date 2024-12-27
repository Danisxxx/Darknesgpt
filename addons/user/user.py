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

@rox('time')
async def set_cutoff_time(client, message):
    """
    Configura la hora de corte para dejar de contar mensajes.
    Uso: Time <hora>
    """
    global cutoff_hour

    # ///hola/// Verifica que se haya especificado una hora válida
    try:
        hour = int(message.text.split()[1])
        if 0 <= hour <= 23:
            cutoff_hour = hour
            await message.reply(f"La hora de corte ha sido configurada a las {hour}:00 hora Venezuela.")
        else:
            await message.reply("Por favor, ingresa una hora válida (entre 0 y 23).")
    except (IndexError, ValueError):
        await message.reply("Uso incorrecto. Ejemplo: Time 8")

async def process_message(client, message):
    """
    Procesa los mensajes enviados al canal.
    """
    global cutoff_hour

    # ///hola/// Verifica si el mensaje contiene "Checked By"
    if "Checked By:" in message.text:
        # ///hola/// Obtiene la hora actual en Venezuela
        now = datetime.now(VENEZUELA_TZ)

        # ///hola/// Si la hora actual es mayor o igual a la hora de corte, no cuenta más mensajes
        if now.hour >= cutoff_hour:
            return

        # ///hola/// Extrae el username y el ID del usuario
        checked_by_line = [line for line in message.text.splitlines() if "Checked By:" in line][0]
        username = checked_by_line.split("[")[1].split("]")[0]  # Extrae el username
        user_id = message.from_user.id  # Obtiene el ID del usuario

        # ///hola/// Actualiza el contador de mensajes del usuario
        user_messages[username] += 1

        # ///hola/// Mensaje de notificación al Owner
        notification = (
            f"{message.text}\n\n"
            f"El Usuario @{username} ID {user_id} Dropeo el Día de Hoy 20 Live"
        )
        await client.send_message(OWNER_ID, notification)

        # ///hola/// Notifica cuando un usuario envía una nueva Live
        live_notification = f"El Usuario @{username} ID Envío una nueva Live"
        await client.send_message(OWNER_ID, live_notification)

async def send_daily_summary(client):
    """
    Enviar resumen diario de usuarios que enviaron mensajes al canal.
    """
    # ///hola/// Obtiene la hora actual en Venezuela
    now = datetime.now(VENEZUELA_TZ)
    today = now.strftime('%d-%m-%Y')

    # ///hola/// Genera la lista de usuarios ordenados por cantidad de mensajes
    sorted_users = user_messages.most_common()
    summary = [f"{i + 1}. @{user} ID {count} mensajes enviados" for i, (user, count) in enumerate(sorted_users)]
    summary_message = f"Lista De Droper {today}\n\n" + "\n".join(summary)

    # ///hola/// Envía el resumen al Owner
    await client.send_message(OWNER_ID, summary_message)

    # ///hola/// Limpia el contador para el próximo día
    user_messages.clear()

async def schedule_daily_summary(client):
    """
    Programa el envío del resumen diario a la hora de corte.
    """
    global cutoff_hour

    while True:
        # ///hola/// Calcula el tiempo hasta la hora de corte
        now = datetime.now(VENEZUELA_TZ)
        next_run = (now + timedelta(days=1)).replace(hour=cutoff_hour, minute=0, second=0, microsecond=0)
        sleep_time = (next_run - now).total_seconds()

        # ///hola/// Espera hasta la hora de corte
        await asyncio.sleep(sleep_time)

        # ///hola/// Envía el resumen diario
        await send_daily_summary(client)
