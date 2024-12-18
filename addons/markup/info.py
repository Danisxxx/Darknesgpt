from configs._def_main_ import *

@rexbt('info')
async def info_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(info, reply_markup=atras)
