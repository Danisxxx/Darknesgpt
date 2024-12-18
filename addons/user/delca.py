import os
import shutil
from configs._def_main_ import *

@rex('delca')
async def delca_callback(client, message):
    # Enviar mensaje indicando que la caché está siendo eliminada
    sent_message = await message.reply("<b>Cache eliminando...</b>", reply_to_message_id=message.id)

    # Directorio raíz del bot
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Recorrer los subdirectorios para encontrar los __pycache__
    pycache_found = False
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".pyc") or filename == "__pycache__":
                pycache_found = True
                file_path = os.path.join(dirpath, filename)
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Eliminar directorios __pycache__
                    else:
                        os.remove(file_path)  # Eliminar archivos .pyc
                except Exception as e:
                    await sent_message.edit(f"<b>Error al eliminar cache: {e}</b>")
                    return

    # Respuesta final
    if pycache_found:
        await sent_message.edit("<b>Cache eliminada correctamente.</b>")
    else:
        await sent_message.edit("<b>No se encontraron archivos de caché para eliminar.</b>")
