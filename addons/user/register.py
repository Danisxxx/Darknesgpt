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
            id INT PRIMARY KEY,
            rango VARCHAR(255) DEFAULT 'Free user',
            priv INT DEFAULT 0,
            dias INT DEFAULT 0,
            expiracion DATETIME DEFAULT NULL,
            ban VARCHAR(255) DEFAULT 'No',
            regist DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("INSERT IGNORE INTO Users (id, rango, priv, dias, ban, regist) VALUES (%s, 'Free user', 0, 0, 'No', NOW())", (user_id,))
    connection.commit()

    cursor.close()
    connection.close()

    # Verificar si es una respuesta a otro mensaje
    reply_to_message_id = message.reply_to_message.message_id if message.reply_to_message else None

    await message.reply_text(
        regist.format(username=username),
        reply_to_message_id=reply_to_message_id
    )
