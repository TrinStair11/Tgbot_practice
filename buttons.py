from telebot import types


def reply_buttons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Перевод')
    button2 = types.KeyboardButton('Википедия')
    keyboard.add(button1, button2)
    return keyboard
