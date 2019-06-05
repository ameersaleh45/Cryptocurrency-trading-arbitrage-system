import ccxt
from ArbitrageExchange import ArbitrageExchange
import datetime
import time

''''''''''''''''configurations'''''''''''''''''
exchanges = {}
min_profit = -1
min_profit_usd = -1
freq = 5
minInvestment = 0.000
baseCurr = 'BTC'
''''''''''''''''''''''''''''''''''''''''''''''''

def print_header():
    print ('date' + "," + 'Base' + "," + 'pair' + "," + 'River' + "," + 'percProf' + "%"
           + "," + 'wBase' + "," + 'wPair' + "," + 'wRiver' + "," + 'RiverBidQty' +
           "," + 'PairBidQty' + "," + 'BaseAskQty' + "," + 'maxTrade' + "," + 'profitInBTC' + ","
           + 'profitInUSDT')


def triangular_arbitrage_explorer():
    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': 'Z2RUPGc7FRtYtUgJXxeg5RnI7yroDmHXlKYqNde5V7tt71Vy8ql7Go8EnfLv5Buh',
        'secret': 'o9Zr7L1pBMjxwa0RuBdmiu4FUjWuwn2vHvn1iK8Hs8FMlcj2nc2TXKNJ6MohD9CG',
        'timeout': 30000,
        'enableRateLimit': True,
    })

    if exchange.has['createMarketOrder'] == False:
        print("error")
        return

    exchangeArb = ArbitrageExchange(exchange)
    exchangeCurrencies = exchangeArb.currencies.keys()
    exchangePairs = exchangeArb.symbols
    while(1):
        exchangeTickers = exchange.fetch_tickers()
        s = baseCurr + "/USDT"
        USDTBase = exchangeTickers[s]['ask']
        for pair in exchangePairs:
            marketData = exchange.market(pair)
            Base = str(marketData['baseId']) + "/" + baseCurr
            #Base = baseCurr + "/" + str(marketData['baseId'])
            River = str(marketData['quoteId']) + "/" + baseCurr
            # River =baseCurr + "/" + str(marketData['quoteId'])
            if Base in exchangePairs and River in exchangePairs:
                wBase = exchangeTickers[Base]['ask']
                wPair = exchangeTickers[pair]['bid']
                wRiver = exchangeTickers[River]['bid']
                if wBase == 0:
                    continue
                profit = 1 / wBase * wPair * wRiver * 0.999 ** 3
                if profit > 1 + min_profit:
                    RiverBidQty = float(exchangeTickers[River]['info']['bidQty'])
                    PairBidQty = float(exchangeTickers[pair]['info']['bidQty'])
                    BaseAskQty = float(exchangeTickers[Base]['info']['askQty'])
                    maxTrade = min(min(RiverBidQty, PairBidQty * wPair) / wPair, BaseAskQty) * wBase
                    if maxTrade > minInvestment:
                        profitInBase = maxTrade * (profit - 1)
                        profitInUSDT = profitInBase * USDTBase
                        if profitInUSDT > min_profit_usd:
                            # BaseBalance = exchange.fetch_balance()[baseCurr]['free']
                            # tradeBaseAmount = min(maxTrade,BaseBalance)
                            # print(exchange.id, exchange.create_market_buy_order(Base, tradeBaseAmount))
                            # print(exchange.id, exchange.create_market_sell_order(, XRPBalance['free']))
                            # pass/redefine custom exchange-specific order params: type, amount, price, flags
                            percProf = str((profit - 1) * 100)
                            print (str(datetime.datetime.now()) + "," + Base + "," + str(
                                pair) + "," + River + "," + percProf + "%"
                                   + "," + str(wBase) + "," + str(wPair) + "," + str(wRiver) + "," + str(RiverBidQty) +
                                   "," + str(PairBidQty)) + "," + str(BaseAskQty) + "," + str(maxTrade) + "," + str(
                                profitInBase) + "," \
                                  + str(profitInUSDT)
        time.sleep(freq)

def main():
    print_header()
    triangular_arbitrage_explorer()


if __name__ == "__main__":
    main()
