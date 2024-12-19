from configs._def_main_ import *
import sqlite3
from datetime import datetime

def initialize_tools_db():
    conn = sqlite3.connect('db/tools.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tools (
            Name TEXT PRIMARY KEY,
            Tools TEXT NOT NULL,
            Active TEXT DEFAULT 'ONN',
            Reason TEXT DEFAULT 'No especificada',
            Date TEXT DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()

def update_tool_status(name, tool, status, reason=None, date=None):
    conn = sqlite3.connect('db/tools.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Name FROM Tools WHERE Name = ?', (name,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute('''
            UPDATE Tools
            SET Active = ?, Reason = ?, Date = ?
            WHERE Name = ?
        ''', (status, reason, date, name))
    else:
        cursor.execute('''
            INSERT INTO Tools (Name, Tools, Active, Reason, Date)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, tool, status, reason, date))

    conn.commit()
    conn.close()

@rex(['off', 'onn'])
async def tools_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("<b>[<a href=tg://user?id=>後</a>] Use: Onn or Off Tools > Reason</b>", reply_to_message_id=message.id, disable_web_page_preview=True)
        return

    command = message.command[0].lower()
    tool_name = message.command[1]
    reason = " ".join(message.command[2:]) if len(message.command) > 2 else "No especificada"
    current_date = datetime.now().strftime('%d-%m-%Y')

    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT PRIVILEGIOS FROM Users WHERE ID = ?', (message.from_user.id,))
    user_privileges = cursor.fetchone()
    conn.close()

    if not user_privileges or user_privileges[0] < 3:
        await message.reply_text(
            "<b>[<a href=tg://user?id=>後</a>] Que Haces, ? No estas autorizado</b>",
            reply_to_message_id=message.id, disable_web_page_preview=True
        )
        return

    if command == "off":
        update_tool_status(tool_name, tool_name, "OFF", reason, current_date)
        await message.reply_text(
            f"<b>[<a href=tg://user?id=>後</a>] Tools <code>{tool_name}</code> ha sido apagado.</b>",
            reply_to_message_id=message.id, disable_web_page_preview=True
        )
    elif command == "onn":
        update_tool_status(tool_name, tool_name, "ONN", "No especificada", None)
        await message.reply_text(
            f"<b>[<a href=tg://user?id=>後</a>] Tools > <code>{tool_name}</code> ha sido Encendido.</b>",
            reply_to_message_id=message.id, disable_web_page_preview=True
        )

initialize_tools_db()
