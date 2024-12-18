from configs._def_main_ import *
import aiohttp
from bs4 import BeautifulSoup

@rex('wik')
async def bot(client, message):
    if len(message.command) < 2:
        await message.reply_text("Por favor, proporciona un término de búsqueda.")
        return

    query = " ".join(message.command[1:])
    url = f"https://es.m.wikipedia.org/w/index.php?search={query}&title=Especial%3ABuscar&profile=advanced&fulltext=1&ns0=1&ns100=1&ns104=1"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                await message.reply_text("Hubo un problema al buscar en Wikipedia.")
                return
            html_content = await response.text()

    soup = BeautifulSoup(html_content, 'html.parser')
    result = soup.find('div', class_='mw-search-result-heading')
    if not result:
        await message.reply_text("No se encontraron resultados.")
        return

    result_link = f"https://es.m.wikipedia.org{result.a['href']}"

    async with session.get(result_link) as response:
        if response.status != 200:
            await message.reply_text("Hubo un problema al obtener el contenido del artículo.")
            return
        article_content = await response.text()

    article_soup = BeautifulSoup(article_content, 'html.parser')
    paragraphs = article_soup.find_all('p')
    full_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

    if not full_text:
        await message.reply_text("El artículo no contiene información suficiente.")
        return

    formatted_result = wik.format(
        busqueda=query,
        result=f"<a href='{result_link}'>{result.get_text(strip=True)}</a>",
        resultado=full_text
    )
    await message.reply_text(formatted_result, disable_web_page_preview=True)
