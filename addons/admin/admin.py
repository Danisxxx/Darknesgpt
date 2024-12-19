from configs._def_main_ import *
import sqlite3

@rex('rol')
async def admin_callback(client, message):
    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()

    cursor.execute('SELECT PRIVILEGIOS FROM Users WHERE ID = ?', (message.from_user.id,))
    user_privileges = cursor.fetchone()

    if user_privileges and user_privileges[0] >= 3:
        args = message.text.split()

        if len(args) == 1:
            await message.reply("<b>Uso incorrecto. Usa /admin ID RANGO</b>", reply_to_message_id=message.id)
        elif len(args) == 3:
            user_id = args[1]
            rank = args[2]

            cursor.execute('UPDATE Users SET RANGO = ? WHERE ID = ?', (rank, user_id))
            conn.commit()

            await message.reply(f"<b>El usuario con ID <code>{user_id}</code> se le asignó el rango <code>{rank}</code></b>", reply_to_message_id=message.id)
        else:
            await message.reply("<b>Uso incorrecto. Usa /admin ID RANGO</b>", reply_to_message_id=message.id)
    else:
        await message.reply("<b>[<a href=tg://user?id=>後</a>] Que Haces, ? No estas autorizado</b>", reply_to_message_id=message.id)
    
    conn.close()
