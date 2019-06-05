import ccxt
from ArbitrageExchange import ArbitrageExchange
import datetime
import time

''''''''''''''''configurations'''''''''''''''''
exchanges = {}
min_profit = 0.005
min_profit_usd = 0.5
freq = 3
baseCurr = 'BTC'
minInvestment = 0.01
''''''''''''''''''''''''''''''''''''''''''''''''

def print_header():
    print ('date' + "," + 'Base' + "," + 'pair' + "," + 'River' + "," + 'percProf' + "%"
           + "," + 'wBase' + "," + 'wPair' + "," + 'wRiver' + "," + 'RiverBidQty' +
           "," + 'PairBidQty' + "," + 'BaseAskQty' + "," + 'maxTrade' + "," + 'profitInBTC' + ","
           + 'profitInUSDT')


def triangular_arbitrage_explorer():
    binance = ccxt.binance()
    binanceArb = ArbitrageExchange(binance)
    binanceCurrencies = binanceArb.currencies.keys()
    binancePairs = binanceArb.symbols
    while(1):
        binanceTickers = binance.fetch_tickers()
        for pair in binancePairs:
            marketData = binance.market(pair)
            Base = str(marketData['baseId']) + "/" + baseCurr
            River = str(marketData['quoteId']) + "/" + baseCurr
            if Base in binancePairs and River in binancePairs:
                wPair = binanceTickers[pair]['ask']
                wBase = binanceTickers[Base]['bid']
                wRiver = binanceTickers[River]['bid']
                USDTBTC = 4000
                if wBase == 0:
                    continue
                profit = 1 / wBase * wPair * wRiver * 0.998 ** 3
                if profit > 1 + min_profit:
                    RiverBidQty = float(binanceTickers[River]['info']['bidQty'])
                    PairBidQty = float(binanceTickers[pair]['info']['bidQty'])
                    BaseAskQty = float(binanceTickers[Base]['info']['askQty'])
                    maxTrade = min(min(RiverBidQty, PairBidQty * wPair) / wPair, BaseAskQty) * wBase
                    if maxTrade > minInvestment:
                        profitInBTC = maxTrade * (profit - 1)
                        profitInUSDT = profitInBTC * USDTBTC
                        if profitInUSDT > min_profit_usd:
                            percProf = str((profit - 1) * 100)
                            print ((str(datetime.datetime.now()) + "," + Base + "," + str(
                                pair) + "," + River + "," + percProf + "%"
                                   + "," + str(wBase) + "," + str(wPair) + "," + str(wRiver) + "," + str(RiverBidQty) +
                                   "," + str(PairBidQty)) + "," + str(BaseAskQty) + "," + str(maxTrade) + "," + str(
                                profitInBTC) + "," \
                                  + str(profitInUSDT))
        time.sleep(freq)


# for pair in Pairs:
# g = nx.DiGraph()
# tickers = binance.fetch_tickers()
# for pair in Pairs:
# 	marketData = binance.market(pair)
# 	w = tickers[pair]['ask']
# 	if w <= 0:
# 		continue
# 	w_inv = (-1) * math.log(1.001 / w, 2.0)
# 	w = (-1) * math.log(w * 1.001, 2.0)
#
# 	g.add_edge(marketData['baseId'], marketData['quoteId'], weight=w)
# 	g.add_edge(marketData['quoteId'], marketData['baseId'], weight=w_inv)
#
# 	# print marketData['baseId'] + " " +marketData['base'] + " " + marketData['quoteId'] + " " + marketData['quote']
#
# tickers = binance.fetch_tickers()
# for pair in Pairs:
# 	marketData = binance.market(pair)
# 	w = tickers[pair]['ask']
# 	if w <= 0:
# 		continue
# 	w_inv = (-1)*math.log(1.001/w,2.0)
# 	w = (-1)*math.log(w*1.001,2.0)
#
# 	g[marketData['baseId']][marketData['quoteId']]['weight'] = w
# 	g[marketData['quoteId']][marketData['baseId']]['weight'] = w_inv
#
# # print cycles
# for cycle in cycles:
# 	cycle.append(cycle[0])
# 	if cycle[0] != 'BTC':
# 		continue
# 	if len(cycle) < 6:
# 		weights = nx.get_edge_attributes(g, 'w')
# 		sumw = sum([g[cycle[i-1]][cycle[i]]['weight'] for i in range(1, len(cycle))])
# 		print cycle
# 		if sumw < 0:
# 			profit = (math.pow(2.0,-sumw) - 1) * 100
# 			print cycle
# 	print "profit: " + str(profit) + "%"
# pos = nx.random_layout(g)
# nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap('jet'), node_size = 500)
# nx.draw_networkx_labels(g, pos)
# nx.draw_networkx_edges(g, pos, edge_color='r', arrows=True)
# labels = nx.get_edge_attributes(g,'weight')
# nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
#
# plt.show()

# # get a list of symbols
# #symbols2 = list (binance.markets.keys ()) # same as previous line
#
# #print (binance.id, symbols)               # print all symbols
# #print bitfinex.currencies
# #print binance.currencies
# #print "Bitfinex fees: " + str(bitfinex.fees)
# #print "Binance fees: " + str(binance.fees)
#
# #print bitfinex.commonCurrencies
# #print binance.commonCurrencies
#
# api_key = "3g1Gc95QaZFfCCDeszJ8Yc7FU7rJS19pWbJ8yvVIEBQBJawG2GINAzbyeM99I5ag"
# api_secret = "FVmpQxrNpkFtKK9whgZEmqc1NJ4849nsmIPSxz6Pga5CE3FME0tTqCdZ8Sgkcogp"
# client = Client(api_key, api_secret)
#
# # Get all trading pairs listed on Binance
# tradingPairs = client.get_exchange_info().get(u'symbols')

# info1 = client.get_order_book(symbol='ETHBTC')

# print "ETH_balance: " + str(ETH_balance)
#
# info2 = client.get_order_book(symbol='LTCETH')

def main():
    print_header()
    triangular_arbitrage_explorer()


if __name__ == "__main__":
    main()
