from configs._def_main_ import *

@rexbt('atras')
async def atras_callback(client, callback_query: CallbackQuery):
   
    await callback_query.edit_message_text(start, reply_markup=menu_principal)
