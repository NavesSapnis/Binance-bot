from time import *
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from string import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import rsi


logging.basicConfig(level=logging.INFO)
bot = Bot(token='6587549219:AAF2uGQJyYjs7IoYUIDK6Keco877wkqZNSc')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
CHAT_ID = -1001929072843
MY_ID = 720116934




@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    if(message.chat.id == MY_ID):
        while True:
            all_message = ""
            all_rsi = rsi.get_all_RSI()
            for symbol, nrsi in all_rsi.items():
                all_message += (f"{symbol} {nrsi}\n")
            await bot.send_message(chat_id=CHAT_ID, text=all_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
