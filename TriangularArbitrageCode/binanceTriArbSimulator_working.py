import ccxt
from ArbitrageExchange import ArbitrageExchange
import datetime
import time

''''''''''''''''configurations'''''''''''''''''
exchanges = {}
min_profit = -1
min_profit_usd = -1
freq = 5
minInvestment = 0.00
baseCurr = 'BTC'
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
        s = baseCurr + "/USDT"
        USDTBase = binanceTickers[s]['ask']
        for pair in binancePairs:
            marketData = binance.market(pair)
            Base = str(marketData['baseId']) + "/" + baseCurr
            River = str(marketData['quoteId']) + "/" + baseCurr
            if Base in binancePairs and River in binancePairs:
                wBase = binanceTickers[Base]['ask']
                wPair = binanceTickers[pair]['bid']
                wRiver = binanceTickers[River]['bid']
                if wBase == 0:
                    continue
                profit = 1 / wBase * wPair * wRiver * 0.998 ** 3
                if profit > 1 + min_profit:
                    RiverBidQty = float(binanceTickers[River]['info']['bidQty'])
                    PairBidQty = float(binanceTickers[pair]['info']['bidQty'])
                    BaseAskQty = float(binanceTickers[Base]['info']['askQty'])
                    maxTrade = min(min(RiverBidQty, PairBidQty * wPair) / wPair, BaseAskQty) * wBase
                    if maxTrade > minInvestment:
                        profitInBase = maxTrade * (profit - 1)
                        profitInUSDT = profitInBase * USDTBase
                        if profitInUSDT > min_profit_usd:
                            percProf = str((profit) * 100)
                            print ((str(datetime.datetime.now()) + "," + Base + "," + str(
                                pair) + "," + River + "," + percProf + "%"
                                   + "," + str(wBase) + "," + str(wPair) + "," + str(wRiver) + "," + str(RiverBidQty) +
                                   "," + str(PairBidQty)) + "," + str(BaseAskQty) + "," + str(maxTrade) + "," + str(
                                profitInBase) + "," \
                                  + str(profitInUSDT))
        time.sleep(freq)

def main():
    print_header()
    triangular_arbitrage_explorer()


if __name__ == "__main__":
    main()
