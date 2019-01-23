from poloniex_wrapper import poloniex, createTimeStamp

exchange = poloniex(APIKey='test', Secret='test')
x = exchange.returnTicker()
print(x.keys())