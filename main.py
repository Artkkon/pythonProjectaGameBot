import telebot
import random
from time import sleep
from variables import token


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    # Приветственное сообщение
    bot.reply_to(message, 'Привет! 😊 Я - бот, который будет играть с тобой в "Камень, Ножницы, Бумага"')

    # Создаем клавиатуру с кнопками
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton('Камень', callback_data='Камень')
    button2 = telebot.types.InlineKeyboardButton('Ножницы', callback_data='Ножницы')
    button3 = telebot.types.InlineKeyboardButton('Бумага', callback_data='Бумага')
    markup.add(button1, button2, button3)

    # Отправляем сообщение с клавиатурой
    bot.send_message(message.chat.id, "Твой ход!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['Камень', 'Ножницы', 'Бумага'])
def game_logic(call):
    user_choice = call.data
    choices = ['Камень', 'Ножницы', 'Бумага']
    bot_choice = random.choice(choices)

    # Определение результата
    if user_choice == bot_choice:
        result = "Ничья! 😐"
    elif (user_choice == 'Камень' and bot_choice == 'Ножницы') or \
         (user_choice == 'Ножницы' and bot_choice == 'Бумага') or \
         (user_choice == 'Бумага' and bot_choice == 'Камень'):
        result = "Ты победил! 🎉"
    else:
        result = "Я победил! 🤖"
    sleep(1)
    # Формируем сообщение с результатом
    response = f"Ты выбрал: {user_choice}\nЯ выбрал: {bot_choice}\n{result}"
    bot.send_message(call.message.chat.id, response)

    # Показываем клавиатуру снова для новой игры
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton('Камень', callback_data='Камень')
    button2 = telebot.types.InlineKeyboardButton('Ножницы', callback_data='Ножницы')
    button3 = telebot.types.InlineKeyboardButton('Бумага', callback_data='Бумага')
    markup.add(button1, button2, button3)
    bot.send_message(call.message.chat.id, "Твой ход! Сыграем еще раз?", reply_markup=markup)

bot.polling(none_stop=True)
