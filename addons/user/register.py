from configs._def_main_ import *
import mysql.connector
from datetime import datetime

@rex('register')
async def register_user(client, message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Conectar a la base de datos MySQL
    connection = mysql.connector.connect(
        host="mysql.railway.internal",
        user="root",
        password="JXyNzSbNJJHCbVNbcdvZWxyYwvlvFLwN",
        database="railway",
        port=3306
    )
    cursor = connection.cursor()

    # Crear la tabla Users si no existe
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

    # Crear la tabla OnlineUsers si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OnlineUsers (
            id INT PRIMARY KEY
        )
    """)

    # Verificar si el usuario ya está registrado en la tabla OnlineUsers
    cursor.execute("SELECT id FROM OnlineUsers WHERE id = %s", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Si el usuario ya está en la tabla, mostrar un mensaje
        await message.reply_text(f"<b>あ » @{username}, ya estás registrado En La Base De Datos</b>")
    else:
        # Si no está registrado, insertarlo en la tabla OnlineUsers
        cursor.execute("INSERT INTO OnlineUsers (id) VALUES (%s)", (user_id,))
        connection.commit()

        # Insertar el usuario en la tabla Users si no existe
        cursor.execute("""
            INSERT IGNORE INTO Users (id, rango, priv, dias, ban, regist) 
            VALUES (%s, 'Free user', 0, 0, 'No', NOW())
        """, (user_id,))
        connection.commit()

        # Responder con el mensaje de registro
        await message.reply_text(
            regist.format(username=username),
            reply_to_message_id=message.id
        )

    # Cerrar la conexión
    cursor.close()
    connection.close()
