from configs._def_main_ import *
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

@rex('ai')
async def bot(client, message):
    if len(message.command) > 1:
        prompt = " ".join(message.command[1:])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{prompt}"}]
        )
        reply = response['choices'][0]['message']['content']
        await message.reply_text(reply)
    else:
        await message.reply_text("Envía un texto después del comando.")
