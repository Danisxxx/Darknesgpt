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

AUTHORIZED_USER_ID = 7202754124

@rex('off')
async def off(_, message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        return await message.reply_text(Not_authorize)

    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        return await message.reply_text("Uso: .off <nombre> [razón]")
    
    name = args[1]
    reason = args[2] if len(args) > 2 else "No especificada"
    date_now = datetime.now().strftime("%d-%m-%Y")

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        select_query = "SELECT * FROM Toolslist WHERE name = %s"
        cursor.execute(select_query, (name,))
        tool = cursor.fetchone()
        
        if not tool:
            return await message.reply_text("Ese comando no existe en mi DB.")
        
        update_query = """
        UPDATE Toolslist 
        SET status = 'Apagado', reason = %s, date = %s 
        WHERE name = %s
        """
        cursor.execute(update_query, (reason, date_now, name))
        conn.commit()
        await message.reply_text(f"Tools Name > {name} Apagado <")
    except pymysql.MySQLError as err:
        await message.reply_text(f"Error: {err}")
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@rex('onn')
async def onn(_, message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        return await message.reply_text(Not_authorize)

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text("Uso: .onn <nombre>")
    
    name = args[1]

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        select_query = "SELECT * FROM Toolslist WHERE name = %s"
        cursor.execute(select_query, (name,))
        tool = cursor.fetchone()
        
        if not tool:
            return await message.reply_text("Ese comando no existe en mi DB.")
        
        update_query = """
        UPDATE Toolslist 
        SET status = 'Encendido', reason = NULL, date = NULL 
        WHERE name = %s
        """
        cursor.execute(update_query, (name,))
        conn.commit()
        await message.reply_text(f"Tools Name > {name} Encendido <")
    except pymysql.MySQLError as err:
        await message.reply_text(f"Error: {err}")
    finally:
        if conn.open:
            cursor.close()
            conn.close()
