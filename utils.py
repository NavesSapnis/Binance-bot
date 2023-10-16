from single import *


def get_trading_pairs():
    futures_info = client.futures_exchange_info()
    perpetual_trading_pairs = []
    for symbol_info in futures_info['symbols']:
        symbol = symbol_info['symbol']
        status = symbol_info['status']
        contract_type = symbol_info['contractType']
        if status == 'TRADING' and contract_type == 'PERPETUAL':
            perpetual_trading_pairs.append(symbol)
    return perpetual_trading_pairs