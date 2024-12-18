from configs._def_main_ import *
import sqlite3

@rexbt('perfil')
async def perfil_callback(client, callback_query: CallbackQuery):
    user = callback_query.from_user
    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()

    cursor.execute('SELECT ID, RANGO, BAN FROM Users WHERE ID = ?', (user.id,))
    user_data = cursor.fetchone()

    if user_data:
        user_id, rank, ban = user_data
    else:
        user_id, rank, ban = user.id, "USUARIO", "NO" 

    perfil_info = Perfil.format(name=user.first_name, id=user_id, idioma=user.language_code, rank=rank, ban=ban)
    await callback_query.edit_message_text(perfil_info, reply_markup=atras)

    conn.close()
