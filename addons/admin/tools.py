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
        return await message.reply_text(f"<b>{Not_authorize}</b>", reply_to_message_id=message.id)

    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        return await message.reply_text("<b>Uso: .off <nombre> [razón]</b>", reply_to_message_id=message.id)
    
    name = args[1]
    reason = args[2] if len(args) > 2 else "<b>No especificada</b>"
    date_now = datetime.now().strftime("%Y-%m-%d")  # Usando formato YYYY-MM-DD

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        select_query = "SELECT * FROM Command WHERE name = %s"
        cursor.execute(select_query, (name,))
        tool = cursor.fetchone()
        
        if not tool:
            return await message.reply_text("<b>Ese comando no existe en mi DB.</b>", reply_to_message_id=message.id)
        
        usage = tool[3]  # Asumiendo que el campo 'usage' es el cuarto en la tabla
        
        update_query = """
        UPDATE Command 
        SET status = 'inactive', reason = %s, date = %s 
        WHERE name = %s
        """
        cursor.execute(update_query, (reason, date_now, name))
        conn.commit()

        reply_message_text = f"""
        <b>[⽷] Tools {name} > /{usage} Apagado</b>
        <b>Razón:</b> {reason}
        <b>Fecha de desactivación:</b> {date_now}
        """
        
        await message.reply_text(reply_message_text, reply_to_message_id=message.id)
        
    except pymysql.MySQLError as err:
        await message.reply_text(f"<b>Error:</b> {err}", reply_to_message_id=message.id)
    finally:
        if conn.open:
            cursor.close()
            conn.close()

@rex('onn')
async def onn(_, message):
    if message.from_user.id != AUTHORIZED_USER_ID:
        return await message.reply_text(f"<b>{Not_authorize}</b>", reply_to_message_id=message.id)

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text("<b>Uso: .onn <nombre></b>", reply_to_message_id=message.id)
    
    name = args[1]

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        select_query = "SELECT * FROM Command WHERE name = %s"
        cursor.execute(select_query, (name,))
        tool = cursor.fetchone()
        
        if not tool:
            return await message.reply_text("<b>Ese comando no existe en mi DB.</b>", reply_to_message_id=message.id)
        
        usage = tool[3]  # Asumiendo que el campo 'usage' es el cuarto en la tabla
        
        update_query = """
        UPDATE Command 
        SET status = 'active', reason = NULL, date = NULL 
        WHERE name = %s
        """
        cursor.execute(update_query, (name,))
        conn.commit()

        reply_message_text = f"""
        <b>[⽷] Tools {name} > /{usage} Encendido</b>
        <b>Razón:</b> No especificada
        <b>Fecha de activación:</b> {datetime.now().strftime('%Y-%m-%d')}
        """
        
        await message.reply_text(reply_message_text, reply_to_message_id=message.id)
        
    except pymysql.MySQLError as err:
        await message.reply_text(f"<b>Error:</b> {err}", reply_to_message_id=message.id)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
