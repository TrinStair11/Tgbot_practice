import telebot
import buttons
import requests
import translate

bot = telebot.TeleBot('7240982693:AAHhRGhTJP6JMOe65T_mhRwPrf29RvPVkFk')


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.chat)
    bot.send_message(message.chat.id, f'Добро пожаловать, {message.chat.first_name}!',
                     reply_markup=buttons.reply_buttons())


@bot.message_handler(content_types=['text'])
def user_message(message):
    print(f'{message.chat.first_name}: {message.text}')
    if message.text.lower() == "википедия":
        bot.send_message(message.chat.id, f'Введите слово для поиска в Википедии: ')
        bot.register_next_step_handler(message, wiki)
    elif message.text.lower() == "перевод":
        bot.send_message(message.chat.id, 'Русско-немецкий переводчик. Введите фразу для перевода: ')
        bot.register_next_step_handler(message, start_translation)
    else:
        bot.reply_to(message, message.text)


def start_translation(message):
    bot.send_message(message.chat.id, translate.translate_text(message.text, 'ru', 'de'))


def wiki(message):
    url = f'https://ru.wikipedia.org/wiki/{message.text.lower()}'
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        bot.send_message(message.chat.id, url)
    else:
        bot.send_message(message.chat.id, f'Статья "{message.text}" не найдена!')


bot.polling(non_stop=True)
