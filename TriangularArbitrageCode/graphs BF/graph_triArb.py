import time
import networkx as nx
import matplotlib.pyplot as plt
import ccxt
from ArbitrageExchange import ArbitrageExchange
import math

binance = ccxt.binance()
binanceArb = ArbitrageExchange(binance)

# build weighted graph to find triangular arbitrage opportunities
g = nx.DiGraph()
Pairs = binanceArb.symbols
tickers = binance.fetch_tickers()
for pair in Pairs:
    marketData = binance.market(pair)
    w = tickers[pair]['ask']
    if w <= 0:
        continue
    w_inv = (-1) * math.log(1.001 / w, 2.0)
    w = (-1) * math.log(w * 1.001, 2.0)

    g.add_edge(marketData['baseId'], marketData['quoteId'], weight=w)
    g.add_edge(marketData['quoteId'], marketData['baseId'], weight=w_inv)

# print marketData['baseId'] + " " +marketData['base'] + " " + marketData['quoteId'] + " " + marketData['quote']

tickers = binance.fetch_tickers()
for pair in Pairs:
    marketData = binance.market(pair)
    w = tickers[pair]['ask']
    if w <= 0:
        continue
    w_inv = (-1) * math.log(1.001 / w, 2.0)
    w = (-1) * math.log(w * 1.001, 2.0)

    g[marketData['baseId']][marketData['quoteId']]['weight'] = w
    g[marketData['quoteId']][marketData['baseId']]['weight'] = w_inv

pos = nx.random_layout(g)
nx.draw_networkx_nodes(g, pos, cmap=plt.get_cmap('jet'), node_size=500)
nx.draw_networkx_labels(g, pos)
nx.draw_networkx_edges(g, pos, edge_color='r', arrows=True)
labels = nx.get_edge_attributes(g, 'weight')
nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

plt.show()
