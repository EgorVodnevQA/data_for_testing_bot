import json
from secrets import token_urlsafe
from telebot import TeleBot, types
from faker import Faker
import os

# Инициализация бота (ЗАМЕНИ НА СВОЙ ТОКЕН!)
TOKEN = 'Твой токен'
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
    types.KeyboardButton("🙍‍♂️ Сгенерировать пользователей"),
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
    """Пытается отправить стикер из файла"""
    try:
        if os.path.exists(STICKER_PATH):
            with open(STICKER_PATH, 'rb') as sticker:
                bot.send_sticker(chat_id, sticker)
            return True
        return False
    except Exception as e:
        print(f"Ошибка при отправке стикера: {e}")
        return False

# ===== Обработчики команд =====
@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
    # Пытаемся отправить стикер
    send_welcome_sticker(message.chat.id)
    
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Я бот для генерации тестовых данных. Выбери действие:",
        reply_markup=main_menu_keyboard
    )

@bot.message_handler(func=lambda msg: msg.text == "🙍‍♂️ Сгенерировать пользователей")
def ask_user_count(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Сколько пользователей сгенерировать?",
        reply_markup=user_count_keyboard
    )

@bot.message_handler(func=lambda msg: msg.text in ["1️⃣", "2️⃣", "5️⃣", "🔟"])
def generate_users(message: types.Message):
    payload_len = {
        "1️⃣": 1,
        "2️⃣": 2,
        "5️⃣": 5,
        "🔟": 10
    }[message.text]

    total_payload = []
    for _ in range(payload_len):
        user_info = faker_ru.simple_profile()
        user_info['phone'] = f'+7{faker_ru.msisdn()[3:]}'
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    payload_str = json.dumps(total_payload, indent=2, ensure_ascii=False, default=str)
    
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>{payload_str}</code>",
        reply_markup=main_menu_keyboard
    )

@bot.message_handler(func=lambda msg: msg.text == "💳 Сгенерировать карту")
def ask_card_type(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери тип карты:",
        reply_markup=card_type_keyboard
    )

@bot.message_handler(func=lambda msg: msg.text in ["VISA", "Mastercard", "Maestro", "JCB"])
def generate_card(message: types.Message):
    card_type = message.text.lower()
    card_number = faker_en.credit_card_number(card_type)
    
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Тестовая карта {card_type}:\n<code>{card_number}</code>",
        reply_markup=main_menu_keyboard
    )

@bot.message_handler(func=lambda msg: True)
def unknown_message(message: types.Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Не понимаю команду. Используй кнопки или /start.",
        reply_markup=main_menu_keyboard
    )

# ===== Запуск бота =====
def main():
    # Проверка наличия стикера
    if not os.path.exists(STICKER_PATH):
        print(f"⚠ Стикер не найден по пути: {STICKER_PATH}")
        print("Загрузите файл стикера (webp) в папку /content в Google Colab")
    
    bot.infinity_polling()

if __name__ == '__main__':
    # Установка зависимостей для Colab
    try:
        import google.colab
        !pip install pyTelegramBotAPI faker
    except:
        pass
    
    main()
