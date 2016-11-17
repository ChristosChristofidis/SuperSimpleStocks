import datetime
import operator
import uuid
from pprint import pprint


class SuperSimpleStocks(object):
    stocks = {
        'TEA': {'Symbol': 'TEA', 'Type': 'Common', 'Last_Dividend': 0, 'Fixed_Dividend': 'blank', 'Par_Value': 100},
        'POP': {'Symbol': 'POP', 'Type': 'Common', 'Last_Dividend': 8, 'Fixed_Dividend': 'blank', 'Par_Value': 100},
        'ALE': {'Symbol': 'ALE', 'Type': 'Common', 'Last_Dividend': 23, 'Fixed_Dividend': 'blank', 'Par_Value': 60},
        'GIN': {'Symbol': 'GIN', 'Type': 'Preferred', 'Last_Dividend': 8, 'Fixed_Dividend': 0.02, 'Par_Value': 100},
        'JOE': {'Symbol': 'JOE', 'Type': 'Common', 'Last_Dividend': 13, 'Fixed_Dividend': 'blank', 'Par_Value': 250},
    }

    def __init__(self):
        self.stock_trades = []

    def dividend_yield(self, symbol, market_price):
        market_price = float(market_price)

        if SuperSimpleStocks.stocks[symbol]['Type'] == 'Common':
            last_dividend = SuperSimpleStocks.stocks[symbol]['Last_Dividend']
            return last_dividend / market_price

        elif SuperSimpleStocks.stocks[symbol]['Type'] == 'Preferred':
            fixed_dividend = SuperSimpleStocks.stocks[symbol]['Fixed_Dividend']
            par_value = SuperSimpleStocks.stocks[symbol]['Par_Value']

            return (fixed_dividend * par_value) / market_price

    def pe_ratio(self, symbol, market_price):
        if SuperSimpleStocks.stocks[symbol]['Last_Dividend']:
            return market_price / self.dividend_yield(symbol, market_price)
        else:
            return None

    def add_trade_record(self, symbol, buy_sell, price, quantity):

        timestamp = datetime.datetime.now().__str__()
        id = uuid.uuid4().__str__()

        if symbol in self.stocks.keys():
            self.stock_trades.append(
                {'id': id, 'Symbol': symbol, 'Type': buy_sell, 'Price': price, 'Timestamp': timestamp,
                 'Quantity': quantity})
        else:
            print "\nBad value for symbol : %s\n" % symbol
            raise ValueError

    def volume_weighted_stock_price(self, symbol, min=15):

        numerator = sum([i['Price'] * i['Quantity'] for i in self.stock_trades if (
            datetime.datetime.now() - datetime.datetime.strptime(i['Timestamp'],
                                                                 "%Y-%m-%d %H:%M:%S.%f")) < datetime.timedelta(
            minutes=min) and i['Symbol'] == symbol])
        denominator = sum([i['Quantity'] for i in self.stock_trades if (
            datetime.datetime.now() - datetime.datetime.strptime(i['Timestamp'],
                                                                 "%Y-%m-%d %H:%M:%S.%f")) < datetime.timedelta(
            minutes=min) and i['Symbol'] == symbol])

        denominator = float(denominator)

        return numerator / denominator

    def all_share_index(self):

        stock_prices = list({self.volume_weighted_stock_price(symbol=i['Symbol']) for i in self.stock_trades})

        length_index = float(len(stock_prices))

        prices_product = reduce(operator.mul, stock_prices, 1)

        result = prices_product ** (1 / length_index)

        return result


if __name__ == '__main__':

    import random

    a = SuperSimpleStocks()

    for j in xrange(2):
        stock_symbols = a.stocks.keys()
        random.shuffle(stock_symbols)
        for i in stock_symbols:
            buy_sell = random.choice(['Buy', 'Sell'])
            a.add_trade_record(i, buy_sell, random.randint(1, 10), random.randint(1, 100))

    print "== Trade Records ==\n"
    pprint(a.stock_trades)
    temp = [i['Symbol'] for i in a.stock_trades]

    print "\n== Volume Weighted Stock Prices ==\n"
    for i in set(temp):
        print "%s: %s" % (i, a.volume_weighted_stock_price(i))

    print "\n== GBCE All Share Index ==\n"
    print "%s" % (a.all_share_index())
    print
