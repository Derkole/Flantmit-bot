import os
import threading
import telebot
from telebot import types
from flask import Flask

# Получаем токен из переменных окружения Render
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Простой Flask-сервер, чтобы Render видел открытый порт
app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health():
    return "Bot is running", 200

# Обработчик команды /start (показывает меню)
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Общение", callback_data="chat")
    btn2 = types.InlineKeyboardButton("Важная информация", callback_data="important")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "chat":
        text = "Сегодня на мите будет общение"
    elif call.data == "important":
        text = "Сегодня на мите будет важная информация"
    else:
        return
    
    # Отправляем сообщение в тот же чат, где нажали кнопку
    bot.send_message(call.message.chat.id, text)
    # Убираем "часики" на кнопке
    bot.answer_callback_query(call.id)

# Запуск бота в отдельном потоке, чтобы он не блокировал Flask
def run_bot():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # Запускаем бота в фоне
    threading.Thread(target=run_bot, daemon=True).start()
    # Запускаем Flask-сервер на порту, который даёт Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
