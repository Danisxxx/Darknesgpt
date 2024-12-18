from configs._def_main_ import *
from transformers import pipeline

generator = pipeline('text-generation', model='gpt2')

@rex('ai')
async def bot(client, message):
    if len(message.command) > 1:
        prompt = " ".join(message.command[1:])
        response = generator(prompt, max_length=50, num_return_sequences=1)
        reply = response[0]['generated_text']
        await message.reply_text(reply)
    else:
        await message.reply_text("Envía un texto después del comando.")
