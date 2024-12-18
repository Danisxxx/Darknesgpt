from configs._def_main_ import *

@rexbt('command')
async def command_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(tools, reply_markup=tools_buttons_page_1)

@rexbt('Next')
async def next_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(tools2, reply_markup=tools_buttons_page_2)

@rexbt('Back')
async def back_callback(client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(start, reply_markup=menu_principal)

@rexbt('atr2')
async def back2_callback(client, callback_query: CallbackQuery):
    await callback_query.edit_message_text(tools, reply_markup=tools_buttons_page_1)
