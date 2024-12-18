from configs._def_main_ import *
from pyrogram import Client
import logging

apid = 27533879 
apihash = '80029e88381fe5c63e364687906458a0' 
token = '7598417720:AAFxF0E1COsem5DY9glYav9urxaGACK1PC8' 

dark = Client(
    "Darkness",
    api_id=apid,
    api_hash=apihash,
    bot_token=token,
    plugins=dict(root='addons')
)

@dark.on_callback_query()
def callback_privates(client, callback_query):
    reply_message = callback_query.message.reply_to_message
    if reply_message is not None and reply_message.from_user is not None:
        if reply_message.from_user.id != callback_query.from_user.id:
            callback_query.answer("Abre tu propio Menú ⚠️")
            return
    callback_query.continue_propagation()

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    print("Bot on")
    dark.run()
