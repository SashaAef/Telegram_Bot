import os # Импортируем модуль ОС для безопасного получения переменных окружения (мой токен)
from dotenv import load_dotenv 

load_dotenv() # Считываем данные с .env

TOKEN = os.getenv('Bot_TOKEN')  # Присваиваем переменной значение с названием Bot_TOKEN

import telebot


bot = telebot.TeleBot(TOKEN)

user_data = {} # Создаем переменную в виде словаря с данными пользователя

@bot.message_handler(commands=['start']) # Приветствие

def send_welcome(message):

    user_name = message.from_user.first_name

    bot.reply_to(message, f'Привет, {user_name}! Я — Порфирий Пыхтин, главный укротитель бытовых катастроф в нашем апарт отеле!\n'
    'Могу принять заявку хоть на протекающую крышу, хоть на бунт выключателя — всё запишу, всё устрою, даже если проблема «непонятно что, но очень тревожно»\n'
    'Порфирий готов выручить в любой ситуации — вот какие услуги у него в арсенале:\n\n'
    '/electric - вызов электрика (спасёт от мигающих драм)\n'
    '/plumber - вызов сантехника (остановит бунт труб)\n'
    '/cleaner - вызов клининга (вернёт порядок после любых чемпионатов)')

@bot.message_handler(commands=['electric','plumber','cleaner']) # Выбор услуги

def choose_service(message):

    chat_id = message.chat.id # Сохраняем ID чата в переменную

    user_data [chat_id] = {} # Создаём место для данных конкретного пользователя
    
    user_data [chat_id] ['service'] = message.text # сохраням услугу

    if message.text == '/electric':
        bot.reply_to(message, 'Отлично! Электрик уже заряжает свой мультиметр и шепчет розеткам: «Ну, держитесь…»')
    elif message.text == '/plumber':
        bot.reply_to(message, 'Сантехник уже в резиновых сапогах и с суровым взглядом — трубы уже начали вести себя прилично.')
    else:
        bot.reply_to(message, 'Команда клининга уже трясёт тряпками так, что пыль в панике собирает чемоданы.')

    bot.send_message(chat_id,'Теперь назови номер корпуса и апартамента, чтобы супергерои знали куда спешить на помощь.\n'
    'Напиши в формате "1-111, где 1 - это номер корпуса, а 111 - номер апартамента')

    bot.register_next_step_handler(message, get_apartment) # Передача сообщения от пользователя (адрес) в функцию
    
def get_apartment (message):  # Получаем адрес

    chat_id = message.chat.id

    user_data[chat_id]['apartment'] = message.text # Сохраняем адрес

    bot.reply_to(message,'Адрес уже в блокноте.\n\n'
    'Теперь, будь добр, в двух-трех словах опиши свою проблему')

    bot.register_next_step_handler(message, get_explanation) # Передача сообщения от пользователя (объяснение проблемы) в функцию

def get_explanation(message):  # Получаем объяснение проблемы
                    
    chat_id = message.chat.id

    user_data[chat_id]['problem'] = message.text

    bot.reply_to(message,'Самое время - выбрать время на завтра. У нас три волшебных окна:\n\n'
    '/time_9_12 — с 09:00 до 12:00 пока все бодрые и не успели устать от жизни.\n'
    '/time_12_15 — с 12:00 до 15:00 самое обеденное, мастер заодно бутерброд доест и всё починит.\n'
    '/time_15_18 — с 15:00 до 18:00 когда солнце ещё светит, а проблемы уже надоели.')

@bot.message_handler(commands=['time_9_12','time_12_15','time_15_18']) # Выбор времени

def choose_time(message):  

    chat_id = message.chat.id

    user_data[chat_id]['time'] = message.text # Сохраняем время

    # Ранее сохраненные данные сохраняем в переменные
    service = user_data [chat_id]['service']  
    apartment = user_data[chat_id]['apartment']
    problem = user_data[chat_id]['problem']
    slot_time = user_data[chat_id]['time']

    bot.reply_to(message,'Заявка принята!\n\n'
    f'Услуга: {service}\n'
    f'Адрес: {apartment}\n'
    f'Проблема: {problem}\n'
    f'Время: {slot_time}\n'
    f'Мастер будет по твоему адресу. Просто сиди, пей чай и жди!')

bot.polling(none_stop=True) # Запускаем опрос сервера Telegram и не останавливаемся в случае ошибок

                
  
