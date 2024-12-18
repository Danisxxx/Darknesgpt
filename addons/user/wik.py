from configs._def_main_ import *
import aiohttp
from bs4 import BeautifulSoup

def check_tool_status(tool_name):
    try:
        with open("plantillas/tools.txt", "r") as file:
            for line in file:
                if line.startswith(f"{tool_name} ="):
                    status = line.split("=", 1)[1].strip()
                    return status == "ONN ✅"
    except FileNotFoundError:
        return False
    return False

@rex('wik')
async def bot(client, message):
    if not check_tool_status("wik"):
        formatted_disabled = Comm.format(
            tools="wik",
            date="{date}",
            reason="{reason}"
        )
        await message.reply_text(
            formatted_disabled,
            reply_to_message_id=message.id
        )
        return

    if len(message.command) < 2:
        await message.reply_text(
            "Por favor, proporciona un término de búsqueda.",
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

        async with aiohttp.ClientSession() as session:
            async with session.get(result_link) as response:
                if response.status != 200:
                    await loading_message.edit_text("Hubo un problema al obtener el contenido del artículo.")
                    return
                article_content = await response.text()

        article_soup = BeautifulSoup(article_content, 'html.parser')
        paragraphs = article_soup.find_all('p')
        full_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

        if not full_text:
            await loading_message.edit_text("El artículo no contiene información suficiente.")
            return

        formatted_result = wik.format(
            busqueda=query,
            result=f"<a href='{result_link}'>{result_title}</a>",
            resultado=full_text
        )
        await loading_message.edit_text(
            formatted_result,
            disable_web_page_preview=True
        )
    except Exception as e:
        await loading_message.edit_text("Ocurrió un error inesperado. Por favor, intenta de nuevo más tarde.")
