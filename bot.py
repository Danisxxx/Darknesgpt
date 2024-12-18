from configs._def_main_ import *

load_dotenv(".env")

dark = Client(
    "Darkness",
    api_id=os.getenv('API_ID'),
    api_hash=os.getenv('API_HASH'),
    bot_token=os.getenv('BOT_TOKEN'),
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
