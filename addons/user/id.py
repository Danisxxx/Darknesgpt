from configs._def_main_ import *

@rex('id')
async def id(_, message):
    await message.reply_text(
        idtext.format(id=message.from_user.id),
        reply_to_message_id=message.id
    )
