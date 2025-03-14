from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import logging
from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")


# Настраиваем базовую конфигурацию логгера
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Создаем объект логгера
logger = logging.getLogger(__name__)

# Выводим сообщение о запуске бота
logger.info("Запуск бота")

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем объекты кнопок
button1 = KeyboardButton(text="Собак 🦮")
button2 = KeyboardButton(text="Огурцов 🥒")

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard = ReplyKeyboardMarkup(
    keyboard=[[button1, button2]], resize_keyboard=True, one_time_keyboard=True
)

################################################################################
### Второй вариант созданиия клавиатуры с помощью билдера клавиатуры ReplyKeyboardBuilder() ###
# Инициализируем билдер клавиатуры
kb_builder = ReplyKeyboardBuilder()

# Создаем список например с 10 кнопками
buttons = [KeyboardButton(text=f"Кнопка {i + 1}") for i in range(10)]

# Распаковываем список с кнопками в билдер, указываем, что
# в одном ряду должно быть 4 кнопки
kb_builder.row(*buttons, width=4)


# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text="Вот такая получается клавиатура",
        reply_markup=kb_builder.as_markup(
            resize_keyboard=True
        ),  # метод билдера as_markup() превращает билдер в объект клавиатуры ReplyKeyboardMarkup
    )


#############################################################################


# Этот хэндлер будет срабатывать на команду /start
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text="Чего кошки боятся больше?", reply_markup=keyboard)


# Этот хэндлер будет срабатывать на ответ "Собак 🦮" и удалять клавиатуру
@dp.message(F.text == "Собак 🦮")
async def procces_dog_answer(message: Message):
    await message.answer(
        text="Да, несомненно, кошки боятся собак.\nНо вы видели как они боятся огурцов?",
        # reply_markup=ReplyKeyboardRemove(),
    )


# Этот хэндлер будет срабатывать на ответ "Огурцов 🥒" и удалять клавиатуру
@dp.message(F.text == "Огурцов 🥒")
async def process_cucumber_answer(message: Message):
    await message.answer(
        text="Да, иногда кажется, что огурцов " "кошки боятся больше",
        # reply_markup=ReplyKeyboardRemove(),
    )


if __name__ == "__main__":
    dp.run_polling(bot)
