from configs._def_main_ import *
import sqlite3
from datetime import datetime

def update_tools_status(tool_name, status, reason=None, date=None):
    tools_file = "plantillas/tools.txt"
    try:
        with open(tools_file, "r") as file:
            lines = file.readlines()

        updated_lines = []
        tool_found = False
        for line in lines:
            if line.startswith(f"{tool_name} ="):
                updated_lines.append(f"{tool_name} = {status}\n")
                if status == "OFF ❌":
                    updated_lines.append(f"Review: {date}\n")
                    updated_lines.append(f"Razon: {reason}\n")
                tool_found = True
            elif not line.startswith(("Review:", "Razon:")):
                updated_lines.append(line)

        if not tool_found:
            updated_lines.append(f"{tool_name} = {status}\n")
            if status == "OFF ❌":
                updated_lines.append(f"Review: {date}\n")
                updated_lines.append(f"Razon: {reason}\n")

        with open(tools_file, "w") as file:
            file.writelines(updated_lines)

        return True
    except Exception as e:
        return False

@rex(['off', 'onn'])
async def tools_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Por favor, proporciona el nombre de la herramienta.")
        return

    command = message.command[0].lower()
    tool_name = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No especificado"
    current_date = datetime.now().strftime('%d-%m-%Y')

    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT PRIVILEGIOS FROM Users WHERE ID = ?', (message.from_user.id,))
    user_privileges = cursor.fetchone()
    conn.close()

    if not user_privileges or user_privileges[0] < 3:
        await message.reply_text(
            "[後] No cuentas con los privilegios suficientes para realizar esta acción",
            reply_to_message_id=message.id
        )
        return

    if command == "off":
        if update_tools_status(tool_name, "OFF ❌", reason=reason, date=current_date):
            from plantillas.plant import Comm
            formatted_message = Comm.format(
                tools=tool_name,
                date=current_date,
                reason=reason
            )
            await message.reply_text(
                f"La herramienta {tool_name} ha sido desactivada.",
                reply_to_message_id=message.id
            )
            await message.reply_text(formatted_message, reply_to_message_id=message.id)
        else:
            await message.reply_text(
                f"Hubo un problema al desactivar la herramienta {tool_name}.",
                reply_to_message_id=message.id
            )
    elif command == "onn":
        if update_tools_status(tool_name, "ONN ✅"):
            await message.reply_text(
                f"La herramienta {tool_name} ha sido activada.",
                reply_to_message_id=message.id
            )
        else:
            await message.reply_text(
                f"Hubo un problema al activar la herramienta {tool_name}.",
                reply_to_message_id=message.id
            )
