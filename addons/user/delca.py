import os
import shutil
from configs._def_main_ import *

@rex('delca')
async def delca_callback(client, message):

    sent_message = await message.reply("<b>Cache eliminando...</b>", reply_to_message_id=message.id)

    root_dir = os.path.dirname(os.path.abspath(__file__))

    pycache_found = False
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".pyc") or filename == "__pycache__":
                pycache_found = True
                file_path = os.path.join(dirpath, filename)
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path) 
                    else:
                        os.remove(file_path)  
                except Exception as e:
                    await sent_message.edit(f"<b>Error al eliminar cache: {e}</b>")
                    return
                    
    if pycache_found:
        await sent_message.edit("<b>Cache eliminada correctamente.</b>")
    else:
        await sent_message.edit("<b>No se encontraron archivos de caché para eliminar.</b>")
