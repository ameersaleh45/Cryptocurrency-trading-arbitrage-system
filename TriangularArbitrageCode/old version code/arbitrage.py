from binance.client import Client
import time
import networkx as nx
import matplotlib.pyplot as plt
import ccxt

print(ccxt.exchanges)

hitbtc = ccxt.hitbtc({'verbose': True})
bitmex = ccxt.bitmex()
huobi  = ccxt.huobi()
binancce = ccxt.binance( {'apiKey': '3g1Gc95QaZFfCCDeszJ8Yc7FU7rJS19pWbJ8yvVIEBQBJawG2GINAzbyeM99I5ag',
  						  'secret': 'FVmpQxrNpkFtKK9whgZEmqc1NJ4849nsmIPSxz6Pga5CE3FME0tTqCdZ8Sgkcogp',})
'''
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'timeout': 30000,
    'enableRateLimit': True,
})

'''
print(bitmex.id, bitmex.load_markets())
#print(huobi.id, huobi.load_markets())
'''
print(hitbtc.fetch_order_book(hitbtc.symbols[0]))
print(bitmex.fetch_ticker('BTC/USD'))
print(huobi.fetch_trades('LTC/CNY'))

print(exmo.fetch_balance())

# sell one bitcoin for market price and receive usd right now
print(exmo.id, exmo.create_market_sell_order('BTC/USD', 1))

# limit buy BTC/EUR, you pay 2500 euro and receive 1 bitcoin  when the order is closed
print(exmo.id, exmo.create_limit_buy_order('BTC/EUR', 1, 2500.00))

# pass/redefine custom exchange-specific order params: type, amount, price, flags, etc...
kraken.create_market_buy_order('BTC/USD', 1, {'trading_agreement': 'agree'})
'''
'''
api_key = "3g1Gc95QaZFfCCDeszJ8Yc7FU7rJS19pWbJ8yvVIEBQBJawG2GINAzbyeM99I5ag"
api_secret = "FVmpQxrNpkFtKK9whgZEmqc1NJ4849nsmIPSxz6Pga5CE3FME0tTqCdZ8Sgkcogp"

BTC_balance = 1;


client = Client(api_key, api_secret)

#Get all trading pairs listed on binance
tradingPairs = client.get_exchange_info().get(u'symbols')


info1 = client.get_order_book(symbol='ETHBTC')

print "max bid: " + str(info1['bids'][0])
print "min ask: " + str(info1['asks'][0])

ETH_balance = BTC_balance/float(info1['asks'][0][0])

print "ETH_balance: " + str(ETH_balance)

info2 = client.get_order_book(symbol='LTCETH')
print "max bid: " + str(info2['bids'][0])
print "min ask: " + str(info2['asks'][0])

LTC_balance = ETH_balance/float(info2['asks'][0][0])

print "LTC_balance: " + str(LTC_balance)


info3 = client.get_order_book(symbol='LTCBTC')
print "max bid: " + str(info3['bids'][0])
print "min ask: " + str(info3['asks'][0])

FINAL_BITCOIN_BALANCE = LTC_balance*float(info3['asks'][0][0])

print "FINAL_BITCOIN_BALANCE: " + str(FINAL_BITCOIN_BALANCE)



i = 0
listOfPairs = []
while i<len(tradingPairs):
	listOfPairs.append(tradingPairs[i].get(u'symbol'))
	i+=1
#print listOfPairs

#get tradeing vales

#build weighted graph to find triangular arbitrage opportunities

g = nx.DiGraph()

for i in listOfPairs[:10]:
	#print "checking " + i
	if len(client.get_order_book(symbol=i)['asks']) > 0:
		w = client.get_order_book(symbol=i)['asks'][0][0]
		winv = 1/float(w)
		#print i + " : " + w
	else: 
		#print "ERROR: " + i
		continue;


	if str(i).endswith("USDT"):
		g.add_edge(i[:-4], "USDT", weight = w)
		g.add_edge("USDT", i[:-4],  weight =winv)
	else:
		g.add_edge(i[:-3], i[-3:], weight = w)
		g.add_edge(i[-3:], i[:-3],  weight = winv)


pos = nx.random_layout(g)
nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap('jet'), node_size = 500)
nx.draw_networkx_labels(g, pos)
nx.draw_networkx_edges(g, pos, edge_color='r', arrows=True)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)

plt.show()
'''
