from configs._def_main_ import *
import sqlite3
from plantillas.plant import dbtext

@rex('my')
async def my_info_callback(client, message):
    try:
        conn = sqlite3.connect('db/user.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
        table_exists = cursor.fetchone()

        if not table_exists:
            await message.reply(dbtext, reply_to_message_id=message.id) 
            return

        cursor.execute('SELECT RANGO, BAN FROM Users WHERE ID = ?', (message.from_user.id,))
        user_data = cursor.fetchone()

        if user_data:
            rank = user_data[0]
            ban = user_data[1]
            perfil_info = Perfil.format(name=message.from_user.first_name, id=message.from_user.id, idioma=message.from_user.language_code, rank=rank, ban=ban)
            await message.reply(perfil_info, reply_to_message_id=message.id)
        else:
            await message.reply(dbtext, reply_to_message_id=message.id) 

        conn.close()

    except Exception as e:
        await message.reply(f"<b>Error: {str(e)}</b>", reply_to_message_id=message.id)
        

