from configs._def_main_ import *
import mysql.connector
from datetime import datetime

@rex('register')
async def register_user(client, message):
    user_id = message.from_user.id
    username = message.from_user.username

    connection = mysql.connector.connect(
        host="mysql.railway.internal",
        user="root",
        password="JXyNzSbNJJHCbVNbcdvZWxyYwvlvFLwN",
        database="railway",
        port=3306
    )
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id BIGINT PRIMARY KEY,
            rango VARCHAR(255) DEFAULT 'Free user',
            priv INT DEFAULT 0,
            dias INT DEFAULT 0,
            expiracion DATETIME DEFAULT NULL,
            ban VARCHAR(255) DEFAULT 'No',
            regist DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OnlineUsers (
            id BIGINT PRIMARY KEY
        )
    """)

    cursor.execute("SELECT id FROM OnlineUsers WHERE id = %s", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        await message.reply_text(f"<b>あ » @{username}, ya estás registrado y en línea.</b>")
    else:
        cursor.execute("INSERT INTO OnlineUsers (id) VALUES (%s)", (user_id,))
        connection.commit()

        cursor.execute("""
            INSERT IGNORE INTO Users (id, rango, priv, dias, ban, regist) 
            VALUES (%s, 'Free user', 0, 0, 'No', NOW())
        """, (user_id,))
        connection.commit()

        await message.reply_text(
            regist.format(username=username),
            reply_to_message_id=message.id
        )

    cursor.close()
    connection.close()
