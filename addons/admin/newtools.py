from configs._def_main_ import *
import pymysql
from datetime import datetime

db_config = {
    "host": "mysql.railway.internal",
    "user": "root",
    "password": "JXyNzSbNJJHCbVNbcdvZWxyYwvlvFLwN",
    "database": "railway",
    "port": 3306
}

def ensure_table_exists():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Command (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            command VARCHAR(255) NOT NULL,
            status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
            reason VARCHAR(255) DEFAULT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            owner VARCHAR(255) NOT NULL
        );
        """
        
        cursor.execute(create_table_query)
        conn.commit()
    except pymysql.MySQLError as err:
        print(f"Error al crear la tabla: {err}")
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@rex('add')
async def add(_, message):
    ensure_table_exists()

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        return await message.reply_text("Uso: /add <nombre_del_tools> <comando>")
    
    name, command = args[1], args[2]
    owner = message.from_user.username or "Desconocido"

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO Command (name, command, status, reason, owner)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        cursor.execute(insert_query, (name, command, 'active', None, owner))
        conn.commit()
        await message.reply_text(f"Comando {name} agregado. Comando /{command}")
    except pymysql.MySQLError as err:
        await message.reply_text(f"Error al agregar el comando: {err}")
    finally:
        if conn.open:
            cursor.close()
            conn.close()
