import json
import os
from secrets import token_urlsafe
from telebot import TeleBot, types
from faker import Faker

# Инициализация бота (ЗАМЕНИ НА СВОЙ ТОКЕН!)
TOKEN = 'токен'
bot = TeleBot(TOKEN, parse_mode='html')

# Инициализация Faker (для пользователей и карт)
faker_ru = Faker('ru_RU')  # для пользователей
faker_en = Faker()         # для карт

# Путь к стикеру в Google Colab
STICKER_PATH = '/content/sticker.webp'  

# ===== Клавиатуры =====
# Главное меню
main_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.row(
    types.KeyboardButton("🙎‍♂️ Сгенерировать пользователей"),
    types.KeyboardButton("💳 Сгенерировать карту")
)

# Меню выбора количества пользователей
user_count_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
user_count_keyboard.row(
    types.KeyboardButton("1️⃣"), types.KeyboardButton("2️⃣")
)
user_count_keyboard.row(
    types.KeyboardButton("5️⃣"), types.KeyboardButton("🔟")
)

# Меню выбора типа карты
card_type_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
card_type_keyboard.row(
    types.KeyboardButton("VISA"), types.KeyboardButton("Mastercard")
)
card_type_keyboard.row(
    types.KeyboardButton("Maestro"), types.KeyboardButton("JCB")
)

def send_welcome_sticker(chat_id):
    """Отправляет стикер из файла"""
    try:
        with open(STICKER_PATH, 'rb') as sticker_file:
            bot.send_sticker(chat_id, sticker_file)
        return True
    except Exception as e:
        print(f"Ошибка при отправке стикера: {e}")
        return False

# ===== Обработчики команд =====
@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    # Отправляем стикер
    if not send_welcome_sticker(message.chat.id):
        bot.send_message(message.chat.id, "🚀 Добро пожаловать!")
    
    # Отправляем приветственное сообщение
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Я бот для генерации тестовых данных. Выбери действие:",
        reply_markup=main_menu_keyboard
    )

@bot.message_handler(func=lambda msg: True)
def unknown_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Не понимаю команду. Используй кнопки или /start.",
        reply_markup=main_menu_keyboard
    )

# ===== Запуск бота в Colab =====
def main():
    # Проверяем наличие стикера
    if not os.path.exists(STICKER_PATH):
        print(f"⚠ Внимание: стикер не найден по пути {STICKER_PATH}")
        print("Загрузите файл стикера в Colab через левую панель (значок папки)")
    
    print("Бот запущен! Для остановки нажмите Ctrl+C")
    bot.infinity_polling()

if __name__ == '__main__':
    # Установка необходимых библиотек в Colab
    try:
        import google.colab
        print("Обнаружена среда Google Colab")
        !pip install pyTelegramBotAPI faker
        print("Библиотеки успешно установлены!")
    except:
        pass
    
    main()