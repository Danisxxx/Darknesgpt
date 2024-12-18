from configs._def_main_ import *
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')

@rex('ai')
async def bot(client, message):
    if len(message.command) > 1:
        prompt = " ".join(message.command[1:])
        response = generator(prompt, max_length=100)
        await message.reply_text(response[0]['generated_text'])
    else:
        await message.reply_text("Envía un texto después del comando.")
