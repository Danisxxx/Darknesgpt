from configs._def_main_ import *
import sqlite3

@rex('setpri')
async def setpri_command(client, message):
    if str(message.from_user.id) != "7202754124":
        await message.reply_text(
            "<b>[<a href=tg://user?id=>後</a>] Que Haces, ? No estas autorizado</b>".format(message.from_user.id)
        )
        return

    if len(message.command) < 3:
        await message.reply_text("<b>Admin > setpri user:id > Nv</b>")
        return

    user_id = message.command[1]
    privileges = message.command[2]

    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE ID = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        await message.reply_text("<b>El ID proporcionado no existe en la base de datos.</b>")
        conn.close()
        return

    cursor.execute('UPDATE Users SET PRIVILEGIOS = ? WHERE ID = ?', (privileges, user_id))
    conn.commit()
    conn.close()

    await message.reply_text(f"<b>[<a href=tg://user?id=>後</a>] Privilegio actualizado</b>")
