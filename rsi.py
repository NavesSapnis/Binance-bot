from binance.client import Client
import ta
import pandas as pd
import CONFIG
import numpy as np
from single import *


def get_rsi_for_pair(pair, period):
    klines = client.futures_klines(symbol=pair, interval=CONFIG.interval)
    df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    df["close"] = pd.to_numeric(df["close"])
    rrsi = ta.momentum.RSIIndicator(close=df["close"], window=period).rsi()
    rrsi = np.array(round(rrsi.iloc[-2:],2))
    if ((rrsi[1] <= 70 and rrsi[0] >= 70) or (rrsi[0] <= 30 and rrsi[1] >= 30)):
        return [True, rrsi]
    else:
        return [False, rrsi]