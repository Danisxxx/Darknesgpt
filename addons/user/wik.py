from configs._def_main_ import *
import aiohttp
from bs4 import BeautifulSoup
import sqlite3

def check_tool_status(tool_name):
    conn = sqlite3.connect('db/tools.db')
    cursor = conn.cursor()
    cursor.execute('SELECT Active, Reason, Date FROM Tools WHERE Name = ?', (tool_name,))
    tool_data = cursor.fetchone()
    conn.close()
    if tool_data and tool_data[0] == "OFF":
        return tool_data  
    return None

def get_user_privileges(user_id):
    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
    table_exists = cursor.fetchone()
    if not table_exists:
        conn.close()
        return None, None, False
    cursor.execute('SELECT RANGO, PRIVILEGIOS FROM Users WHERE ID = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return user_data[0], user_data[1], True
    return None, None, True

@rex('wik')
async def bot(client, message):
    rango, _, db_exists = get_user_privileges(message.from_user.id)

    if not db_exists:
        await message.reply_text(
            dbtext,
            reply_to_message_id=message.id
        )
        return

    if rango is None or rango.lower() == "usuario":
        await message.reply_text(
            Not_authorize,
            reply_to_message_id=message.id
        )
        return

    tool_status = check_tool_status("wik")
    if tool_status is not None:
        formatted_disabled = wiks.format(
            tools="wik",
            date=tool_status[2] if tool_status[2] else "No disponible",
            reason=tool_status[1] if tool_status[1] else "No especificado"
        )
        await message.reply_text(
            formatted_disabled,
            reply_to_message_id=message.id
        )
        return

    if len(message.command) < 2:
        await message.reply_text(
            "<b>Tools: Wiki Busqueda</b>",
            reply_to_message_id=message.id
        )
        return

    query = " ".join(message.command[1:])
    search_url = f"https://es.m.wikipedia.org/w/index.php?search={query}&title=Especial%3ABuscar&profile=advanced&fulltext=1&ns0=1&ns100=1&ns104=1"

    loading_message = await message.reply_text(
        "Buscando contenido...",
        reply_to_message_id=message.id
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status != 200:
                    await loading_message.edit_text("Hubo un problema al buscar en Wikipedia.")
                    return
                html_content = await response.text()

        soup = BeautifulSoup(html_content, 'html.parser')
        result = soup.find('div', class_='mw-search-result-heading')

        if not result:
            await loading_message.edit_text("No se encontraron resultados.")
            return

        result_title = result.get_text(strip=True)
        result_link = f"https://es.m.wikipedia.org{result.a['href']}"

        formatted_result = f"<b>Search Wikipedia Result: {query}\nResult: {result_title}\nLink: {result_link}</b>"
        await loading_message.edit_text(formatted_result)

    except Exception:
        await loading_message.edit_text("Ocurrió un error inesperado. Por favor, intenta de nuevo más tarde.")
