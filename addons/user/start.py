from configs._def_main_ import *
import sqlite3

@rex('start')
async def start_command(client, message):
    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        ID INTEGER PRIMARY KEY,
        RANGO TEXT,
        PRIVILEGIOS INTEGER DEFAULT 0,
        DIAS INTEGER,
        BAN TEXT DEFAULT 'NO',
        SPAM INTEGER,
        REGIST TEXT
    )''')

    cursor.execute('SELECT * FROM Users WHERE ID = ?', (message.from_user.id,))
    user = cursor.fetchone()

    if user is None:
        cursor.execute('''
        INSERT INTO Users (ID, RANGO, DIAS, SPAM, REGIST, BAN, PRIVILEGIOS)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (message.from_user.id, 'Usuario', 0, 0, 'Sí', 'NO', 0))

    conn.commit()
    conn.close()

    await message.reply_text(
        start, 
        reply_markup=menu_principal,  
        reply_to_message_id=message.id
    )
