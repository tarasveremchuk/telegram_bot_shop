from telegram import InputMediaPhoto
from telegram.ext import Updater, MessageHandler
from telegram import Message

import random

import dp as dp
import telebot
import webbrowser
from telebot import types
from time import sleep


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
        mygoodsChapter(message)
    elif message.text == 'ℹ️ Про нас':
        infoChapter(message)
    elif message.text == 'Орест лох':
        OrestLoh(message)

    elif message.text=='Відправити фото речей':
        sentPhotoChapter(message)

        @bot.message_handler(content_types='photo')
        def get_photo(message):
            bot.forward_message(-917631518, message.from_user.id, message.message_id)
    elif message.text=='Я відправив усі фото':
        info2Chapter(message)





    elif message.text == '🔹 Товар #1':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о первом товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #2':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о втором товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #3':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о третьем товаре...', reply_markup=markup)
    elif message.text == '🔹 Товар #4':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('💳 Купить')
        button2 = types.KeyboardButton('↩️ Назад')
        markup.row(button1, button2)
        bot.send_message(message.chat.id, 'Информация о четвертом товаре...', reply_markup=markup)
    elif message.text == '⚙️ Настройки #1':
        # Функционал не придумал
        bot.send_message(message.chat.id, 'Настройки номер 1...')
    elif message.text == '⚙️ Настройки #2':
        # Функционал не придумал
        bot.send_message(message.chat.id, 'Настройки номер 2...')
    elif message.text == '💳 Купить' or message.text == '✏️ Написати менеджеру':
        # Сюда можете ввести свою ссылку на Телеграмм, тогда пользователя будет перекидывать к вам в личку
        webbrowser.open('https://t.me/p01us')
    elif message.text == '↩️ Назад':
        goodsChapter(message)
    elif message.text == '↩️ Назад до меню':
        welcome(message)
    # Если пользователь написал свое сообщение, то бот рандомно генерирует один из возможных вариантов ответа
    # Добавлять и редактировать варианты ответов можно в списке answers
    else:
        bot.send_message(message.chat.id, answers[random.randint(0, 3)])

# Функция, отвечающая за раздел товаров
def goodsChapter(message):
    # Кнопки для товаров
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
    # button1 = types.KeyboardButton('⚙️ Настройки #1')
    # button2 = types.KeyboardButton('⚙️ Настройки #2')

    # markup.row(button1, button2)
    button3 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button3)
    bot.send_message(message.chat.id, 'Тут має бути список ваших речей:', reply_markup=markup)
def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # button1 = types.KeyboardButton('⚙️ Настройки #1')
    # button2 = types.KeyboardButton('⚙️ Настройки #2')

    # markup.row(button1, button2)
    button3 = types.KeyboardButton('↩️ Назад до меню')
    markup.row(button3)
    bot.send_message(message.chat.id, '🔻 Для початку ви маєте відправити нам фото речі, яку ви бажаєте продати, натиснувши на кнопку "Продати річ".\n\n'
                                      '🔻 Фото будуть автоматично переслані одному з наших працівників, який розгляне вашу пропозицію та запропонує вам найкращу ціну, роблячи це максимально швидко.\n\n'
                                      '🔻Статус вашої пропозиції ви можете переглянути натиснувши кнопку “Мої речі”.\n\n'
                                      '🔻Як тільки ви підтвердите ціну, запропоновану нашим працівником, у вас буде можливість обрати між трьома видами доставки:\n'
                                      '💳 Доставка через систему\n'
                                      '🚚 Доставка наложним платежем\n'
                                      '💰 Доставка повною оплатою\n\n'
                                      '🔻Після того як ви успішно відправите товар, вам потрібно буде прикріпити номер накладної …\n\n'
                                      '🔻Гроші будуть якомога швидше перераховані вашу картку,після того як ми отримаємо ваш товар.', reply_markup=markup)

# Функция, отвечающая за раздел помощи
def sentPhotoChapter(message):
    bot.send_message(-917631518, f'Користувач @{message.from_user.username} надсилає фото свого товару')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('Я відправив усі фото')
    markup.row(button2)
    bot.send_message(message.chat.id, '📌 Будь ласка, відправте нам наступні фото:', reply_markup=markup)
    bot.send_message(message.chat.id,
                     '🔻 Фото цілої речі (ззаду та спереду).\n🔻 Фото верхніх бирок\n🔻 Фото нижніх бирок (якщо такі є)\n🔻 Фото недоліків ', reply_markup=markup)




def info2Chapter(message):
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
    bot.send_message(message.chat.id, 'Текст.\nТекст.', reply_markup=markup)

def OrestLoh(message):
    bot.send_message(message.chat.id, 'Так я з вами згоден,що Орест Лох, а також він МАВПА!')




# Строчка, чтобы программа не останавливалась
bot.polling(none_stop=True)