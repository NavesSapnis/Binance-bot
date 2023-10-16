from binance.client import Client
import pandas as pd
import ta


def get_RSI(token):
    client = Client()
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
                    rsi_data[symbol] = float(last_rsi)
                else:
                    pass
            except:
                pass

    return dict(sorted(rsi_data.items(), key=lambda item: item[1]))



