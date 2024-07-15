# Кнопки
from telebot import types
import database as db


# Кнопка отправки номера
def num_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить номер📞', request_contact=True)
    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb


# Кнопка отправки локации
def loc_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Отправить локацию🌎', request_location=True)
    # Добавляем кнопки в пространство
    kb.add(but1)
    return kb


# Кнопки выбора товара
def main_menu(products):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    cart = types.InlineKeyboardButton(text='Корзина', callback_data='cart')
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}',
                                               callback_data=f'{i[0]}')
                    for i in products if i[2] > 0]
    # Добавляем кнопки в пространство
    kb.add(*all_products)
    kb.row(cart)
    return kb


# Кнопки выбора количества
def choose_pr_count(pr_amount, plus_or_minus='', amount=1):
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Создаем сами кнопки
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    to_cart = types.InlineKeyboardButton(text='В корзину', callback_data='to_cart')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    # Алгоритм изменения кол-ва товара
    if plus_or_minus == 'increment':
        if amount < pr_amount:
            count = types.InlineKeyboardButton(text=str(amount + 1), callback_data=amount)
    elif plus_or_minus == 'decrement':
        if amount > 1:
            count = types.InlineKeyboardButton(text=str(amount - 1), callback_data=amount)
    # Добавить кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(to_cart, back)
    return kb


# Кнопки корзины
def cart_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    order = types.InlineKeyboardButton(text='Оформить заказ',
                                       callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить корзину',
                                       callback_data='clear')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    # Добавить кнопки в пространство
    kb.add(order, clear)
    kb.row(back)
    return kb


## Кнопки для админки ##
# Меню админ панели
def admin_menu():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    but1 = types.KeyboardButton('Добавить товар')
    but2 = types.KeyboardButton('Удалить товар')
    but3 = types.KeyboardButton('Изменить товар')
    but4 = types.KeyboardButton('В главное меню')
    # Добавляем кнопки в пространство
    kb.add(but1, but2, but3)
    kb.row(but4)
    return kb


# Кнопки вывода товаров
def admin_pr(products):
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    all_products = [types.KeyboardButton(f'{i[1]}') for i in products]
    back = types.KeyboardButton('Назад')
    # Добавляем кнопки в пространство
    kb.add(all_products)
    kb.row(back)
    return kb


# Кнопки для изменения аттрибута
def change_buttons():
    # Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    # Создаем сами кнопки
    name = types.InlineKeyboardButton(text='Название',
                                      callback_data='name')
    des = types.InlineKeyboardButton(text='Описание',
                                     callback_data='des')
    count = types.InlineKeyboardButton(text='Количество',
                                       callback_data='count')
    price = types.InlineKeyboardButton(text='Цена',
                                       callback_data='price')
    photo = types.InlineKeyboardButton(text='Фото',
                                       callback_data='photo')
    back = types.InlineKeyboardButton(text='Назад',
                                      callback_data='back')
    # Добавляем кнопки в пространство
    kb.row(name)
    kb.add(des, count, price, photo)
    kb.row(back)
    return kb


# Кнопки подтверждения
def confirm_buttons():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    yes = types.KeyboardButton('Да')
    no = types.KeyboardButton('Нет')
    # Добавляем кнопки в пространство
    kb.add(yes, no)
    return kb