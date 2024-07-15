# Алгоритмы бота
import telebot
import buttons as bt
import database as db

bot = telebot.TeleBot('TOKEN')
users = {}
admins = {}

ADMIN_ID = 581727126


@bot.message_handler(commands=['start'])
def start_message(msg):
    user_id = msg.from_user.id
    check = db.check_user(user_id)
    pr_from_db = db.get_pr_id()

    if check:
        bot.send_message(user_id, 'Здравствуйте! Добро пожаловать!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=bt.main_menu(pr_from_db))
    else:
        bot.send_message(user_id, 'Здравствуйте! Давайте начнем регистрацию!\n'
                                  'Введите свое имя')
        bot.register_next_step_handler(msg, get_name)


def get_name(msg):
    user_id = msg.from_user.id
    user_name = msg.text

    bot.send_message(user_id, 'Отлично! Теперь отправьте номер!',
                     reply_markup=bt.num_button())
    bot.register_next_step_handler(msg, get_number, user_name)


@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to_cart', 'back'])
def choose_count(call):
    if call.data == 'increment':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=bt.choose_pr_count
                                      (db.get_exact_pr(users[call.message.chat.id]['pr_name'])[4], 'increment',
                                       users[call.message.chat.id]['pr_amount']))
        users[call.message.chat.id]['pr_amount'] += 1
    elif call.data == 'decrement':
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=bt.choose_pr_count
                                      (db.get_exact_pr(users[call.message.chat.id]['pr_name'])[4], 'decrement',
                                       users[call.message.chat.id]['pr_amount']))
        users[call.message.chat.id]['pr_amount'] -= 1
    elif call.data == 'to_cart':
        pr_name = db.get_exact_pr(users[call.message.chat.id]['pr_name'])[1]
        db.to_cart(call.message.chat.id, pr_name, users[call.message.chat.id]['pr_amount'])
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Товар успешно помещен в корзину!'
                                               ' Желаете что-то еще?',
                         reply_markup=bt.main_menu(db.get_pr_id()))
    elif call.data == 'back':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Перенаправляю вас обратно в меню:',
                         reply_markup=bt.main_menu(db.get_pr_id()))


@bot.callback_query_handler(lambda call: call.data in ['order', 'back', 'clear', 'cart'])
def cart_handle(call):
    text = 'Ваша корзина:\n\n'
    if call.data == 'clear':
        db.clear_cart(call.message.chat.id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Корзина очищена!')
        bot.send_message(call.message.chat.id, 'Выберите пункт меню:',
                         reply_markup=bt.main_menu(db.get_pr_id()))
    elif call.data == 'order':
        text.replace('Ваша корзина:', 'Новый заказ!')
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Отправьте локацию, куда '
                                               'вам надо доставить товары!',
                         reply_markup=bt.loc_button())
        bot.register_next_step_handler(call, get_user_loc, text)
    elif call.data == 'back':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Перенаправляю вас обратно в меню:',
                         reply_markup=bt.main_menu(db.get_pr_id()))
    elif call.data == 'cart':
        user_cart = db.show_cart(call.message.chat.id)
        total = 0.0
        for i in user_cart:
            text += (f'Товар: {i[1]}\n'
                     f'Количество: {i[2]}\n')
            total += db.get_pr_price(i[1])[0] * i[2]
        text += f'\nИтого: {total}'
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, text, reply_markup=bt.cart_buttons())


def get_user_loc(msg, text):
    user_id = msg.from_user.id
    if msg.location:
        text += f'Клиент: @{msg.from_user.username}'
        bot.send_message(1, text)
        bot.send_location(1, latitude=msg.location.latitude,
                          longitude=msg.location.longitude)
        db.make_order(user_id)
        bot.send_message(user_id, 'Ваш заказ был оформлен! Скоро с вами свяжутся специалисты!')
        bot.send_message(user_id, 'Выберите пункт меню:',
                         reply_markup=bt.main_menu(db.get_pr_id()))
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        bot.register_next_step_handler(msg, get_user_loc, text)


def get_number(msg, user_name):
    user_id = msg.from_user.id

    if msg.contact:
        user_number = msg.contact.phone_number
        db.register(user_id, user_name, user_number)
        bot.send_message(user_id, 'Регистрация прошла успешно!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Отправьте номер через кнопку!')
        bot.register_next_step_handler(msg, get_number, user_name)


@bot.callback_query_handler(lambda call: int(call.data) in [i[0] for i in db.get_all_pr()])
def choose_product(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    pr_info = db.get_exact_pr(call.data)
    bot.send_photo(call.message.chat.id, photo=pr_info[5],
                   caption=f'{pr_info[1]}\n\n'
                           f'Описание: {pr_info[2]}\n'
                           f'Цена: {pr_info[3]}\n'
                           f'Количество на складе: {pr_info[4]}',
                   reply_markup=bt.choose_pr_count(pr_info[4]))
    users[call.message.chat.id] = {'pr_name': call.data, 'pr_amount': 1}


@bot.message_handler(commands=['admin'])
def admin_message(msg):
    if msg.from_user.id == ADMIN_ID:
        bot.send_message(ADMIN_ID, 'Выберите опцию:',
                         reply_markup=bt.admin_menu())
        bot.register_next_step_handler(msg, admin_choice)
    else:
        bot.send_message(msg.from_user.id, 'Вы не админ!')


def admin_choice(msg):
    if msg.text == 'Добавить товар':
        bot.send_message(ADMIN_ID, 'Введите название продукта',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_pr_name)
    elif msg.text == 'Удалить товар':
        if db.check_pr():
            bot.send_message(ADMIN_ID, 'Выберите продукт',
                             reply_markup=bt.admin_pr(db.get_pr_id()))
            bot.register_next_step_handler(msg, confirm_delete)
        else:
            bot.send_message(ADMIN_ID, 'Продуктов в базе нет!')
            bot.register_next_step_handler(msg, admin_choice)
    elif msg.text == 'Изменить товар':
        if db.check_pr():
            bot.send_message(ADMIN_ID, 'Выберите продукт',
                             reply_markup=bt.admin_pr(db.get_pr_id()))
            bot.register_next_step_handler(msg, get_pr_attr)
        else:
            bot.send_message(ADMIN_ID, 'Продуктов в базе нет!')
            bot.register_next_step_handler(msg, admin_choice)
    elif msg.text == 'В главное меню':
        pr_from_db = db.get_pr_id()
        bot.send_message(ADMIN_ID, 'Перенаправляю вас обратно в меню',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(ADMIN_ID, 'Выберите пункт меню:',
                         reply_markup=bt.main_menu(pr_from_db))


def get_pr_name(msg):
    pr_name = msg.text
    bot.send_message(ADMIN_ID, 'Теперь введите описание')
    bot.register_next_step_handler(msg, get_pr_des, pr_name)


def get_pr_des(msg, pr_name):
    pr_des = msg.text
    bot.send_message(ADMIN_ID, 'Теперь введите кол-во товара')
    bot.register_next_step_handler(msg, get_pr_count, pr_name, pr_des)


def get_pr_count(msg, pr_name, pr_des):
    if msg.text.isnumeric():
        pr_count = int(msg.text)
        bot.send_message(ADMIN_ID, 'Теперь введите цену товара')
        bot.register_next_step_handler(msg, get_pr_price, pr_name, pr_des, pr_count)
    else:
        bot.send_message(ADMIN_ID, 'Пишите только целые числа!')
        bot.register_next_step_handler(msg, get_pr_count, pr_name, pr_des)


def get_pr_price(msg, pr_name, pr_des, pr_count):
    if msg.text.isdecimal():
        pr_price = float(msg.text)
        bot.send_message(ADMIN_ID, 'Перейдите на сайт https://postimages.org/.\n'
                                   'Загрузите фото товара и отправьте прямую на него ссылку!')
        bot.register_next_step_handler(msg, get_pr_photo,
                                       pr_name, pr_des, pr_count, pr_price)
    else:
        bot.send_message(ADMIN_ID, 'Пишите только дробные числа!')
        bot.register_next_step_handler(msg, get_pr_price, pr_name, pr_des, pr_count)


def get_pr_photo(msg, pr_name, pr_des, pr_count, pr_price):
    pr_photo = msg.text
    db.pr_to_db(pr_name, pr_des, pr_price, pr_count, pr_photo)
    bot.send_message(ADMIN_ID, 'Товар успешно добавлен! Желаете что-то ещё?',
                     reply_markup=bt.admin_menu())
    bot.register_next_step_handler(msg, admin_choice)


def confirm_delete(msg):
    pr_name = msg.text
    bot.send_message(ADMIN_ID, 'Вы точно уверены?',
                     reply_markup=bt.confirm_buttons())
    bot.register_next_step_handler(msg, delete_product, pr_name)


def delete_product(msg, pr_name):
    if msg.text == 'Да':
        db.del_pr(pr_name)
        bot.send_message(ADMIN_ID, 'Товар успешно удален!',
                         reply_markup=bt.admin_menu())
        bot.register_next_step_handler(msg, admin_choice)
    elif msg.text == 'Нет':
        bot.send_message(ADMIN_ID, 'Отменено',
                         reply_markup=bt.admin_menu())
        bot.register_next_step_handler(msg, admin_choice)


def get_pr_attr(msg):
    admins[ADMIN_ID] = msg.text
    bot.send_message(ADMIN_ID, 'Какой аттрибут продукта хотите изменить?',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(ADMIN_ID, 'Выберите аттрибут ниже',
                     reply_markup=bt.change_buttons())


@bot.callback_query_handler(lambda call: call.data in ['name', 'des', 'price', 'photo', 'back'])
def change_attr(call):
    if call.data == 'name':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Введите новое название продукта')
        attr = call.data
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'des':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Введите новое описание продукта')
        attr = call.data
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'price':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Введите новую цену продукта')
        attr = call.data
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'photo':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Введите ссылку на новое фото продукта')
        attr = call.data
        bot.register_next_step_handler(call, confirm_change, attr)
    elif call.data == 'back':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, 'Перенаправляю вас обратно в меню',
                         reply_markup=bt.admin_menu())
        bot.register_next_step_handler(call, admin_choice)


def confirm_change(msg, attr):
    new_value = msg.text
    if attr == 'price':
        db.change_pr_attr(admins[ADMIN_ID], float(new_value), attr=attr)
    else:
        db.change_pr_attr(admins[ADMIN_ID], new_value, attr=attr)
    bot.send_message(ADMIN_ID, 'Изменение прошло успещно!',
                     reply_markup=bt.admin_menu())
    bot.register_next_step_handler(msg, admin_choice)


bot.polling()
