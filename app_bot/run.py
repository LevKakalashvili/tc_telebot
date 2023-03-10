import logging

from aiogram import Bot, Dispatcher, executor, types

from config import Config as AppConfig
from utils import screenshot_maker as scm

logging.basicConfig(level=logging.INFO)

bot = Bot(token=AppConfig().BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer("Введите адрес сайта (url) в формате:\nhttps://url\nhttp://url")


@dp.message_handler()
async def echo(message: types.Message):
    success, data = scm.make_sreeenshot(url=message.text)
    if success:
        with open(data["file"], mode="rb") as f:
            await message.answer_document(f)
        await message.answer(f"Код ответа: {data['status_code']}")
    else:
        await message.answer(data["message"])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
