import logging

from aiogram import Bot, Dispatcher, executor, types
from app_bot.config import Config as AppConfig
from app_bot.utils import is_valid_url, get_screenshot

logging.basicConfig(level=logging.INFO)

bot = Bot(token=AppConfig.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Введите url.")


@dp.message_handler()
async def echo(message: types.Message):

    if is_valid_url(message.text):
        file = get_screenshot(message.text)
        if file is not None:
            await message.answer_document(open(file, mode="rb"))
            # await message.answer(f'Правильный url: {message.text}')

    else:
        await message.answer(f'Не верный url: {message.text}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)