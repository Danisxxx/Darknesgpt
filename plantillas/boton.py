from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


menu_principal = InlineKeyboardMarkup([[InlineKeyboardButton("Perfil", callback_data="perfil"), InlineKeyboardButton("Command", callback_data="command"), InlineKeyboardButton("Info", callback_data="info")]])

atras = InlineKeyboardMarkup([[InlineKeyboardButton("Atras", callback_data="atras"), InlineKeyboardButton("exit", callback_data="exit")]])

tools_buttons_page_1 = InlineKeyboardMarkup([
    [InlineKeyboardButton("Atras", callback_data="Back"), InlineKeyboardButton("Siguiente", callback_data="Next")]
])

tools_buttons_page_2 = InlineKeyboardMarkup([
    [InlineKeyboardButton("Atras", callback_data="atr2"), InlineKeyboardButton("Exit", callback_data="exit")]
])
