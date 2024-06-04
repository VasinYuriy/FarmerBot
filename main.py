import asyncio
import logging
import sys
from gridfs import GridFS
from pymongo import MongoClient

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import BufferedInputFile

with open("config.txt") as f:
    TOKEN = f.read()
dp = Dispatcher()
client = MongoClient('localhost', 27017)
db = client['plants']
col = db['plants']
fs = GridFS(db)

PLANT_DICT = {
    "Береза": "birch",
    "Дуб": "oak",
    "Смородина": "currant",
}

SUPPORTED_PLANTS = {
    "Деревья": ["Береза", "Дуб"],
    "Кусты": ["Смородина"]
}

SUPPORTED_FAMILIES = ["Деревья", "Кусты"]


def get_image_by_plant(plant):
    file = fs.find_one(filter={'filename': f'{plant}.jpg'}).read()
    return BufferedInputFile(file, filename=f'{plant}.jpg')


def get_caption_by_plant(plant):
    query_filter = {"plant_name": plant}
    doc = col.find_one(filter=query_filter)
    return doc["caption"]


def get_bot_info():
    return "sample_bot_info"


def get_plants_keyboard(family):
    kb = [[]]
    row_counter = 0
    for plant in SUPPORTED_PLANTS[family]:
        if row_counter == 3:
            kb.append([])
            row_counter = 0

        kb[-1].append(types.KeyboardButton(text=plant))
        row_counter += 1
    kb.append([types.KeyboardButton(text="Назад")])
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите растение"
    )
    return keyboard


def get_families_keyboard():
    kb = [[]]
    row_counter = 0
    for family in SUPPORTED_FAMILIES:
        if row_counter == 3:
            kb.append([])
            row_counter = 0
        kb[-1].append(types.KeyboardButton(text=family))
        row_counter += 1
    kb.append([types.KeyboardButton(text="Информация о боте")])
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите раздел"
    )
    return keyboard


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    if message.text in PLANT_DICT.keys():
        plant = PLANT_DICT[message.text]
        # Send a copy of the received message
        await message.answer_photo(photo=get_image_by_plant(plant), caption=get_caption_by_plant(plant))

    elif message.text in SUPPORTED_FAMILIES:
        await message.answer("Выберите растение", reply_markup=get_plants_keyboard(message.text))

    elif message.text == "Информация о боте":
        await message.answer(get_bot_info())

    elif message.text in ("/start", "Назад"):
        await message.answer("Выберите раздел", reply_markup=get_families_keyboard())

    else:
        await message.answer("Такого растения нет в базе")


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
