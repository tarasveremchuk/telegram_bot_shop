import base64
import json
import random
from io import BytesIO
import io

import telebot
import webbrowser
from telebot import types
import sqlite3
# Считываю свой токен из файла mytoken.txt, в твоем случае это будет не нужно
# Удали 6 и 7 строчки и вместо переменной mytoken в 10 строчке напиши свой токен
# Пример: bot = telebot.TeleBot('62732:RyJidSDIdi...')
file = open('./mytoken.txt')
mytoken = file.read()
# Передаем сюда токен, который получили от FatherBot
bot = telebot.TeleBot(mytoken)
# Варианты ответов пользователю, если тот ввел непонятное боту сообщение
answers = ['Я не зрозумів,що ти хочеш сказати.', 'Вибач,я не зрозумів тебе.', 'Я не знаю цієї команди.', 'Мій творець не казав,як відповідати на цю ситуацію... >_<']

# Обработка команды /start

@bot.message_handler(commands=['start'])


def welcome(message):
    # Добавляем кнопки, которые будут появляться после ввода команды /start
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER
            )""")
    connect.commit()

    user_id = [message.chat.id]
    cursor.execute("INSERT INTO login_id VALUES (?);", user_id)
    connect.commit()


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💸 Продати річ')
    button2 = types.KeyboardButton('👕 Мої речі')
    button3 = types.KeyboardButton('🛠 Як все працює')
    button4 = types.KeyboardButton('ℹ️ Про нас')
    # Разделяю кнопки по строкам так, чтобы товары были отдельно от остальных кнопок
    markup.row(button1)
    markup.row(button2)
    markup.row(button3, button4)

    if message.text == '/start':
        # Отправляю приветственный текст
        bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}!\nВітаємо у нашому магазині одягу,де ви можете продати свої речі!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Закинув тебе в головне меню,вибирай!', reply_markup=markup)






# Обработка обычных текстовых команд, описанных в кнопках
@bot.message_handler()
def info(message):
    if message.text == '💸 Продати річ':
        goodsChapter(message)
    elif message.text == '🛠 Як все працює':
        settingsChapter(message)
    elif message.text=='👕 Мої речі':
        my_items(message)
    elif message.text == 'ℹ️ Про нас':
        infoChapter(message)
    elif message.text == 'Орест лох':
        OrestLoh(message)
    elif message.text == 'Як проходить оцінка товару?':
            OtsinkaTovaru(message)







    elif message.text=='Відправити фото речей':
        sentPhotoChapter(message)
        global last_order_number
        last_order_number = None

        @bot.message_handler(content_types='photo')
        def get_photo(message):
            conn = sqlite3.connect('photos.db')
            cursor = conn.cursor()

            # Створення таблиці для збереження фотографій
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS photos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    file BLOB,
                    order_number INTEGER
                )
            ''')
            conn.commit()

            if message.photo:
                # Отримання ідентифікатора користувача
                user_id = message.from_user.id

                # Отримання фотографії з повідомлення
                photo = message.photo[-1]

                # Отримання файлу фотографії
                file_info = bot.get_file(photo.file_id)
                file = bot.download_file(file_info.file_path)

                # Кодування фотографії в base64
                encoded_photo = base64.b64encode(file)

                global last_order_number

                # Якщо це перше фото або кнопка "Відправити фото" була натиснута, створюємо новий номер замовлення
                if last_order_number is None or message.text == 'Відправити фото речей':
                    # Оновлюємо номер замовлення
                    cursor.execute('SELECT MAX(order_number) FROM photos')
                    result = cursor.fetchone()[0]
                    if result is None:
                        last_order_number = 1
                    else:
                        last_order_number = int(result) + 1

                # Збереження фотографії в базу даних з номером замовлення
                cursor.execute('INSERT INTO photos (user_id, file, order_number) VALUES (?, ?, ?)',
                               (user_id, encoded_photo, last_order_number))
                conn.commit()

                # Відправлення фотографії до групи
                bot.send_photo(chat_id='-917631518', photo=photo.file_id)

            cursor.close()
            conn.close()

        @bot.message_handler(func=lambda message: message.text == 'Я відправив усі фото')
        def send_all_photos(message):
            conn = sqlite3.connect('photos.db')
            cursor = conn.cursor()

            # Отримання останнього номера замовлення
            cursor.execute('SELECT MAX(order_number) FROM photos')
            result = cursor.fetchone()[0]
            if result is None:
                last_order_number = 1
            else:
                last_order_number = int(result)

            # Вибірка фотографій для певного номера замовлення
            cursor.execute('SELECT file FROM photos WHERE order_number = ?', (last_order_number,))
            photo_records = cursor.fetchall()

            if photo_records:
                for photo_record in photo_records:
                    encoded_photo = photo_record[0]
                    photo_data = base64.b64decode(encoded_photo)

                    # Відправлення фотографій до групи
                    bot.send_photo(chat_id='-917631518', photo=io.BytesIO(photo_data))

            else:
                bot.reply_to(message, 'Не знайдено фотографій для відправлення!')

            cursor.close()
            conn.close()

        # -917631518
            # bot.forward_message(-917631518, message.from_user.id, message.message_id)
    elif message.text=='Я відправив усі фото':


        info2Chapter(message)







    elif message.text == '✏️ Написати менеджеру':
        # Сюда можете ввести свою ссылку на Телеграмм, тогда пользователя будет перекидывать к вам в личку
        # webbrowser.open('https://t.me/sndskup')
        username = '@sndskup'  # Замініть <user_id> на ідентифікатор користувача
        profile_link = f'{username}'
        bot.send_message(chat_id=message.chat.id, text='Натисніть на посилання, щоб написати в підтримку:',
                         disable_web_page_preview=True)
        bot.send_message(chat_id=message.chat.id, text=profile_link)
    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад до меню':
        welcome(message)
    # Если пользователь написал свое сообщение, то бот рандомно генерирует один из возможных вариантов ответа
    # Добавлять и редактировать варианты ответов можно в списке answers
    else:
        bot.send_message(message.chat.id, answers[random.randint(0, 3)])


def goodsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Речі,які ми купуємо')
    button2 = types.KeyboardButton('Відправити фото речей')
    button3 = types.KeyboardButton('Як проходить оцінка товару?')
    button4 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button1)
    markup.row(button2)
    markup.row(button3)
    markup.row(button4)
    bot.send_message(message.chat.id, 'Ви перейшли у розділ "Продати річ" ', reply_markup=markup)
def mygoodsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button3 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button3)
    bot.send_message(message.chat.id, 'Тут має бути список ваших речей:', reply_markup=markup)
def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button3 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button3)
    bot.send_message(message.chat.id, '📸 Натисніть кнопку "Продати річ" і надішліть нам фото вашої речі.\n\n'
                                      '🚀 Наші працівники швидко розглянуть вашу пропозицію та запропонують найкращу ціну.\n\n'
                                      '👀 Ви зможете переглянути статус вашої пропозиції, натиснувши кнопку "Мої речі".\n\n'
                                      '💳 Якщо ви погоджуєтесь з запропонованою ціною, оберіть один з трьох способів доставки:\n'
                                      '  - Доставка через систему\n'
                                      '  - Доставка наложним платежем\n'
                                      '  - Доставка повною оплатою\n\n'
                                      '📦 Після відправки товару, прикріпіть номер накладної...\n\n'
                                      '💸 Ми швидко перерахуємо гроші на вашу карту після отримання товару.', reply_markup=markup)

# Функция, отвечающая за раздел помощи
def sentPhotoChapter(message):
    # bot.send_message(-917631518, f'Користувач @{message.from_user.username} надсилає фото свого товару')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('Я відправив усі фото')
    markup.row(button2)
    bot.send_message(message.chat.id, '📌 Будь ласка, відправте нам наступні фото:', reply_markup=markup)
    bot.send_message(message.chat.id,
                     '🔻 Фото цілої речі (ззаду та спереду).\n🔻 Фото верхніх бирок\n🔻 Фото нижніх бирок (якщо такі є)\n🔻 Фото недоліків ', reply_markup=markup)




def info2Chapter(message):
    user_id = message.from_user.id


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('↩️ Назад до меню')
    markup.row( button2)

    bot.send_message(message.chat.id, '✅ Ваші фото були успішно завантажені 😌\n\n'
                                      '📍Щоб переглянути статус вашого товару перейдіть до розділу "Мої речі".\n\n'
                                      '📍Один з наших працівників розгляне вашу пропозицію та запропонує вам найкращу ціну, роблячи це максимально швидко 🚀',
                     reply_markup=markup)
def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написати менеджеру')
    button2 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button1, button2)
    bot.send_message(message.chat.id, 'Про нас 🙃\n\n'
                                      'Ми - команда експертів, які спеціалізуються на скупці різного\n'
                                      '“вінтажного”, “кежуального” та не тільки одягу. Наша мета - \n'
                                      'надати вам зручну та вигідну можливість продати непотрібні \n'
                                      'речі та отримати за них реальну вартість.\n'
                                      'Чому обрати нас? 🌟\n\n'
                                      '1️⃣ Широкий спектр речей: Ми приймаємо до розгляду \n'
                                      'різноманітні види одягу, включаючи верхній одяг, штани, \n'
                                      'інколи взуття, аксесуари та багато іншого.\n\n'
                                      '2️⃣ Справедлива оцінка: Ми цінуємо ваші товари і ретельно \n'
                                      'оцінюємо їх, враховуючи бренд, стан та популярність. Наші \n'
                                      'професіонали гарантують справедливу вартість для ваших \n'
                                      'речей.\n\n'
                                      '3️⃣ Простий процес продажу: Ми зробили процес продажу\n'
                                      'максимально простим і зручним для вас. Ви надсилаєте нам \n'
                                      'фото товару, отримуєте оцінку, погоджуєтеся з ціною та \n'
                                      'обираєте спосіб доставки. Ми стежимо за кожним кроком, щоб\n'
                                      'ви отримали гарну взаємовигідну угоду.\n\n'
                                      '4️⃣ Надійна та швидка оплата: Після прийняття вашого товару \n'
                                      'та підтвердження угоди, ми швидко перераховуємо гроші на\n'
                                      'ваш рахунок. Ми розуміємо, що час - цінний ресурс, тому ми \n'
                                      'робимо все можливе, щоб оплата була здійснена швидко та \n'
                                      'надійно.\n\n'
                                      'Ми пишаємося нашою командою експертів, яка зосереджена на \n'
                                      'вашому задоволенні та впевнена, що забезпечить вам зручний \n'
                                      'та вигідний досвід продажу. Приєднуйтесь до нашої спільноти і \n'
                                      'давайте разом знайдемо нове призначення для вашого   \n'
                                      'непотрібного одягу! 💼'
                                      '', reply_markup=markup)

def OrestLoh(message):
    bot.send_message(message.chat.id, 'Так я з вами згоден,що Орест Лох, а також він МАВПА!')

def OtsinkaTovaru(message):
    bot.send_message(message.chat.id, 'На оцінку вашого товару впливають три речі\n\n- Фірма (модель)\n- Розмір\n- Стан ')

# @bot.message_handler(commands=['send_photos'])
# def sendPhotoToGroup(message):
#     user_id = message.from_user.id
#
#     # Отримання фотографій користувача з бази даних
#     cursor.execute('SELECT file FROM photos WHERE user_id = ?', (user_id,))
#     photo_records = cursor.fetchall()
#
#     if len(photo_records) > 0:
#         photos = []
#         for record in photo_records:
#             # Розкодування фотографії з base64
#             encoded_photo = record[0]
#             photo_data = base64.b64decode(encoded_photo)
#             photos.append(BytesIO(photo_data))
#
#         # Відправка всіх фотографій в одному повідомленні
#         media_group = [types.InputMediaPhoto(media=photo) for photo in photos]
#         bot.send_media_group(chat_id='-917631518', media=media_group)
#     else:
#         bot.reply_to(message, 'Немає фотографій для відправлення!')


# Строчка, чтобы программа не останавливалась
@bot.message_handler(func=lambda message: message.text == 'Мої речі')
def my_items(message):
    conn = sqlite3.connect('photos.db')
    cursor = conn.cursor()

    # Отримання ідентифікатора користувача
    user_id = message.from_user.id

    # Отримання унікальних order_id користувача з бази даних
    cursor.execute('SELECT DISTINCT order_number FROM photos WHERE user_id = ?', (user_id,))
    order_numbers = cursor.fetchall()

    if order_numbers:
        for order_number in order_numbers:
            order_number = order_number[0]

            # Отримання першого фото для кожного order_id користувача
            cursor.execute('SELECT file FROM photos WHERE user_id = ? AND order_number = ? LIMIT 1',
                           (user_id, order_number))
            photo_record = cursor.fetchone()

            if photo_record:
                encoded_photo = photo_record[0]
                photo_data = base64.b64decode(encoded_photo)

                # Формування повідомлення з фото та текстом
                caption = f"Ваш номер замовлення: {order_number}"
                bot.send_photo(chat_id=message.chat.id, photo=io.BytesIO(photo_data), caption=caption)
            else:
                bot.reply_to(message, f"Не знайдено фото для замовлення з номером {order_number}")
    else:
        bot.reply_to(message, 'Не знайдено замовлень для відправлення!')

    cursor.close()
    conn.close()


bot.polling(none_stop=True)