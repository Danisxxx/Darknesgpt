from configs._def_main_ import *
import pymysql

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

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        return await message.reply_text(offtext3, reply_to_message_id=message.id)
    
    command = args[1]
    reason = args[2] if len(args) > 2 else "<b>No especificada</b>"
    date_now = datetime.now().strftime("%Y-%m-%d")

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        select_query = "SELECT * FROM Command WHERE command = %s"
        cursor.execute(select_query, (command,))
        tool = cursor.fetchone()
        
        if not tool:
            return await message.reply_text(offtext4, reply_to_message_id=message.id)
        
        status = tool[3]  
        usage = tool[2]

        if status == 'inactive':
            return await message.reply_text(offtext1.format(command=command), reply_to_message_id=message.id)
        
        update_query = """
        UPDATE Command 
        SET status = 'inactive', reason = %s, date = %s 
        WHERE command = %s
        """
        cursor.execute(update_query, (reason, date_now, command))
        conn.commit()

        reply_message_text = offtext2.format(name=tool[1], command=usage, reason=reason, date=date_now)
        
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
        return await message.reply_text(ontext, reply_to_message_id=message.id)
    
    command = args[1]

    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        select_query = "SELECT * FROM Command WHERE command = %s"
        cursor.execute(select_query, (command,))
        tool = cursor.fetchone()
        
        if not tool:
            return await message.reply_text(onntext4, reply_to_message_id=message.id)
        
        status = tool[3]  
        usage = tool[2]

        if status == 'active':
            return await message.reply_text(onntext1.format(command=command), reply_to_message_id=message.id)

        update_query = """
        UPDATE Command 
        SET status = 'active', reason = NULL, date = NULL 
        WHERE command = %s
        """
        cursor.execute(update_query, (command,))
        conn.commit()

        reply_message_text = onntext2.format(name=tool[1], command=usage, reason="<b>No especificada</b>", date=datetime.now().strftime('%Y-%m-%d'))
        
        await message.reply_text(reply_message_text, reply_to_message_id=message.id)
        
    except pymysql.MySQLError as err:
        await message.reply_text(f"<b>Error:</b> {err}", reply_to_message_id=message.id)
    finally:
        if conn.open:
            cursor.close()
            conn.close()
