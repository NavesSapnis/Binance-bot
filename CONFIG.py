from binance.client import Client
import utils

BOT_TOKEN = "6587549219:AAF2uGQJyYjs7IoYUIDK6Keco877wkqZNSc"

CHANNEL_ID = -1001929072843
RSI_PERIODS = [6,14,21]

RSI_LOW = 23
RSI_HIGH = 77

interval = Client.KLINE_INTERVAL_15MINUTE

TRADING_PAIRS = utils.get_trading_pairs()