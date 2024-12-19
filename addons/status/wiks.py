from configs._def_main_ import *
import sqlite3

def get_tool_status(tool_name):
    conn = sqlite3.connect('db/tools.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Name, Active, Reason, Date FROM Tools WHERE Name = ?', (tool_name,))
    tool_data = cursor.fetchone()
    conn.close()

    if not tool_data or tool_data[1] == "OFF":
        return wiks.format(
            tools=tool_name,
            date=tool_data[3] if tool_data else "No disponible",
            reason=tool_data[2] if tool_data else "No especificado"
        )
