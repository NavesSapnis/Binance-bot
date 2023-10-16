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


async def on_bot_starting(dp):
    while True:
            all_message = ""
            all_rsi = rsi.get_all_RSI()
            for symbol, nrsi in all_rsi.items():
                all_message += (f"{symbol} {nrsi}\n")
            if all_message == "":
                await bot.send_message(chat_id=CHAT_ID, text="Nothing...")
            else:
                 await bot.send_message(chat_id=CHAT_ID, text=all_message)

            

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_bot_starting, skip_updates=True)