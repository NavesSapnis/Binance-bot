from binance.client import Client
import pandas as pd
import ta


client = Client()

def get_RSI(token):
    interval = Client.KLINE_INTERVAL_15MINUTE
    symbol = token+"USDT"
    klines = client.futures_klines(symbol=symbol, interval=interval)
    df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
    df["close"] = pd.to_numeric(df["close"])

    rsi_period = 6
    df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=rsi_period).rsi()

    last_rsi = round(df["rsi"].iloc[-1],2)
    return float(last_rsi)


def get_all_RSI():
    client = Client()
    exchange_info = client.futures_exchange_info()
    symbols = [symbol['symbol'] for symbol in exchange_info['symbols']]

    rsi_data = {}

    for symbol in symbols:
        if symbol.endswith("USDT"):
            interval = Client.KLINE_INTERVAL_15MINUTE
            try:
                klines = client.futures_klines(symbol=symbol, interval=interval)
                df = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"])
                df["close"] = pd.to_numeric(df["close"])
                
                rsi_period = 6
                df["rsi"] = ta.momentum.RSIIndicator(close=df["close"], window=rsi_period).rsi()
                
                last_rsi = round(df["rsi"].iloc[-1], 2)
                if(last_rsi!=100 and (last_rsi<=25 or last_rsi>=75)):
                    ratios = calculate_volume_ratios(fetch_ohlcv_binance(symbol))
                    prev_prev_to_current, previous_to_current = ratios
                    if(prev_prev_to_current < 0.55 or previous_to_current < 0.55):
                        rsi_data[symbol] = float(last_rsi)
                else:
                    pass
            except:
                pass

    return dict(sorted(rsi_data.items(), key=lambda item: item[1]))


def fetch_ohlcv_binance(symbol):

    # Получаем текущее время
    end_time = client.get_server_time()["serverTime"]
    start_time = end_time - (3 * 15 * 60 * 1000)

    ohlcv = client.futures_klines(symbol=symbol, interval="15m", startTime=start_time, endTime=end_time, limit=3)
    return ohlcv



def calculate_volume_ratios(volumes):
    # Проверка, что у нас есть данные о прошлых объемах
    if len(volumes) < 3:
        return None  # Недостаточно данных

    # Получение объемов прошлой, позапрошлой и настоящей свечи
    current_volume = float(volumes[-1][5])  # Объем текущей свечи
    previous_volume = float(volumes[-2][5])  # Объем прошлой свечи
    prev_prev_volume = float(volumes[-3][5])  # Объем позапрошлой свечи

    # Вычисление соотношения позапрошлого объема к настоящему и прошлого к настоящему
    prev_prev_to_current_ratio = prev_prev_volume / current_volume
    previous_to_current_ratio = previous_volume / current_volume

    return prev_prev_to_current_ratio, previous_to_current_ratio

#НЕОБХОДИМО ТЕСТИРОВАНИЕ