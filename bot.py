from time import *
import logging
from aiogram import Bot, Dispatcher, types, executor
from string import *
import rsi
import emoji
import CONFIG


logging.basicConfig(level=logging.INFO)
bot = Bot(token=CONFIG.BOT_TOKEN)
dp = Dispatcher(bot)

CHANNEL_ID = CONFIG.CHANNEL_ID



async def show_valid(dp):
    while True:
        print("Начал цикл")
        for pair in CONFIG.TRADING_PAIRS:
            print(f"Проверяю {pair}")
            try:
                show = 0
                brokes = []
                message = f"{pair}:\n"
                for period in CONFIG.RSI_PERIODS:
                    broke = rsi.get_rsi_for_pair(pair, period)
                    if (broke[1][0] < 50):
                        message += f"{emoji.emojize(':green_circle:')} Long"
                    else:
                        message += f"{emoji.emojize(':red_circle:')} Short"
                    message += f"RSI ({period}): {broke[1][0]} --> {broke[1][1]} |"
                    if broke[0]:
                        show += 1
                        message += f"{emoji.emojize(':check_mark_button:')}\n"
                    else:
                        message += f"{emoji.emojize(':cross_mark:')}\n"
                    brokes.append(broke)
                message += f"\nhttps://www.binance.com/ru/futures/{pair}"
                if (show > 1):
                    await bot.send_message(chat_id=CHANNEL_ID, text=message, disable_web_page_preview=True)
            except:
                pass

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=show_valid, skip_updates=True)