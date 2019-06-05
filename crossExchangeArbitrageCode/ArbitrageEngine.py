import ccxt
from ArbitrageExchange import ArbitrageExchange
from datetime import datetime
import time
from ArbitrageCfg import exchangesDir
from ArbitrageCfg import coins
from ArbitrageCfg import exchanges_list
from ArbitrageCfg import limitThreshold_per
from ArbitrageCfg import min_profit_per
from ArbitrageCfg import baseCurrencies



while 1:
    exchanges = exchanges_list.copy()
    clients = {str(e): getattr(ccxt, e.lower())() for e in exchanges}
    print("connected successfully..." + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("start fetching tickers...")

    # fetching all tickers from specified exchanges
    tickers = {}
    for e in exchanges:
        try:
            tickers[e] = clients[e].fetch_tickers()
        except:
            print("couldn't fetch ticker from: " + str(e))
            exchanges.remove(e)

    print("fetched tickers successfully...")

    # finding arbitrage opportunities
    for baseCurr, baseCurrData in baseCurrencies.items():
        print(baseCurr)
        for src in exchanges:
            print("Arbitraging source exchange: " + str(src))
            for dst in exchanges:
                for coin in coins:
                    pair = coin + "/" + baseCurr
                    if src == dst:
                        continue
                    try:
                        wask = tickers[src][pair]['ask']
                        wbid = tickers[dst][pair]['bid']
                        profit = ((wbid / wask) - 1) * 100
                    except:
                        continue
                    if profit > 0:
                        try:
                            srcBook = clients[src].fetch_order_book(pair)
                            dstBook = clients[dst].fetch_order_book(pair)
                        except:
                            continue
                        sizeI = len(srcBook['asks'])
                        sizeJ = len(dstBook['bids'])
                        possible_profit = True
                        old_profit = 1
                        i, j = 0, 0
                        step_invest = baseCurrData['min_invest']

                        srcValue, srcAmount, dstValue, dstAmount = 0, 0, 0, 0
                        oldSrcValue, oldSrcAmount, oldDstValue, oldDstAmount = -1, -1, -1, -1

                        curr_profit = 0
                        while possible_profit:
                            while srcValue < step_invest and sizeI > i:
                                amount = min(srcBook['asks'][i][1],
                                             (baseCurrData['max_invest'] - srcValue) / srcBook['asks'][i][0])
                                srcValue = srcValue + amount * srcBook['asks'][i][0]
                                srcAmount += amount
                                i += 1
                            if i == sizeI:
                                possible_profit = False
                                curr_profit = old_profit
                                srcValue = oldSrcValue
                                srcAmount = oldSrcAmount
                                dstValue = oldDstValue
                                dstAmount = oldDstAmount
                                break

                            while srcAmount > dstAmount and sizeJ > j:
                                amount = min(dstBook['bids'][j][1], (srcAmount - dstAmount))
                                dstValue = dstValue + amount * dstBook['bids'][j][0]
                                dstAmount += amount
                                j += 1

                            if j == sizeJ:
                                possible_profit = False
                                curr_profit = old_profit
                                srcValue = oldSrcValue
                                srcAmount = oldSrcAmount
                                dstValue = oldDstValue
                                dstAmount = oldDstAmount
                                break

                            curr_profit = dstValue / srcValue
                            if curr_profit < old_profit:
                                possible_profit = False
                                curr_profit = old_profit
                                srcValue = oldSrcValue
                                srcAmount = oldSrcAmount
                                dstValue = oldDstValue
                                dstAmount = oldDstAmount
                                break
                            old_profit = curr_profit
                            oldDstAmount = dstAmount
                            oldDstValue = dstValue
                            oldSrcValue = srcValue
                            oldSrcAmount = srcAmount
                            step_invest += baseCurrData['step']

                        if srcValue < baseCurrData['min_invest']:
                            continue
                        srcAmount_orig = srcAmount
                        ## Adding fees
                        srcAmount *= (1 - exchangesDir[src]['tradingFees'])
                        try:
                            srcAmount -= exchangesDir[src]['withdrawalFees'][coin]
                        except:
                            continue

                        dstAmount, dstValue, j = 0, 0, 0
                        while srcAmount > dstAmount and sizeJ > j:
                            amount = min(dstBook['bids'][j][1], (srcAmount - dstAmount))
                            dstValue = dstValue + amount * dstBook['bids'][j][0]
                            dstAmount += amount
                            j += 1

                        dstValue *= (1 - exchangesDir[dst]['tradingFees'])
                        try:
                            dstValue -= exchangesDir[dst]['withdrawalFees'][baseCurr]
                        except:
                            continue
                        profitInBase = dstValue - srcValue
                        profitInPer = (dstValue / srcValue - 1) * 100
                        if profitInPer > min_profit_per:
                            if profit > limitThreshold_per:
                                print("---ALERT!--- CHECK RELIABILITY")
                            print("estimated initial profit: " + str(profit) + "%")
                            print(
                                "trading: " + str(coin) + " srcExchange: " + str(src) + " dstExchange: " + str(dst))
                            print("srcValue: " + str(
                                srcValue) + baseCurr + " invested " + "amount of altcoin: " + str(
                                srcAmount_orig))
                            print("dstValue: " + str(
                                dstValue) + baseCurr + " after selling " + "amount of altcoin: " + str(
                                dstAmount))
                            print("final Amount: " + str(dstValue) + " initial Amount: " + str(
                                srcValue) + " profit in " + baseCurr + ": " + str(profitInBase) + " %: " + str(
                                profitInPer))

                            answer = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ',' + str(profit) + ',' + str(
                                baseCurr) + ',' + str(coin) + ',' + str(src) + ',' + str(dst) + ',' + str(
                                srcValue) + ',' + str(srcAmount_orig) + ',' + str(dstValue) + ',' + str(
                                dstAmount) + ',' + str(dstValue) + ',' + str(srcValue) + ',' + str(
                                profitInBase) + ',' + str(
                                profitInPer)
                            print(answer)
