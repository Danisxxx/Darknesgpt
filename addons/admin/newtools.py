from configs._def_main_ import *
import mysql.connector

db_config = {
    "host": "mysql.railway.internal",
    "user": "root",
    "password": "JXyNzSbNJJHCbVNbcdvZWxyYwvlvFLwN",
    "database": "railway",
    "port": 3306
}

@rex('newtools')
async def newtools(_, message):
    args = message.text.split(maxsplit=4)
    if len(args) < 5:
        return await message.reply_text("Uso: /newtools <name> <command> <status> <owner>")

    name, command, status, owner = args[1], args[2], args[3], args[4]

    if status not in ['active', 'inactive']:
        return await message.reply_text("El estado debe ser 'active' o 'inactive'.")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO Toolslist (name, command, status, owner)
        VALUES (%s, %s, %s, %s);
        """
        
        cursor.execute(insert_query, (name, command, status, owner))
        conn.commit()
        await message.reply_text(f"Herramienta '{name}' añadida con éxito.")
    except mysql.connector.Error as err:
        await message.reply_text(f"Error al añadir la herramienta: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
