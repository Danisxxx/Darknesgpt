from plantillas.plant import *
from pyrogram import Client, filters
import os
import logging
from dotenv import load_dotenv
from plantillas.boton import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def rex(bit):
    nix = Client.on_message(filters.command(bit, ["/", ".", ",", "-", "$", "%"]))
    return nix
    
def rexbt(bor):
    nox = Client.on_callback_query(filters.regex(bor))
    return nox
