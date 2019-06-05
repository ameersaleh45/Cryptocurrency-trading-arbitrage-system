class ArbitrageExchange:
    def __init__(self, exchange):
        exchange.load_markets()
        self.symbols = exchange.symbols
        self.currencies = exchange.currencies
        self.commonCurrencies = exchange.commonCurrencies


