import logging

from aiogram import Bot, Dispatcher, executor, types
from app_bot.config import Config as AppConfig

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=AppConfig.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):

    # TODO: url validation

    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)