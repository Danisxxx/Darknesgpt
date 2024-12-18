from configs._def_main_ import *

@rexbt('exit')
async def exit_callback(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("""
<b>Guapo bai! 🌩
━━━━━━━━━━━━━━━━━
No Fue un gusto que me toques</b>.""")
