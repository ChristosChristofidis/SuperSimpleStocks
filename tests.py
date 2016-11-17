import unittest

from SuperSimpleStocks import SuperSimpleStocks


class Tests(unittest.TestCase):
    def setUp(self):
        self.a = SuperSimpleStocks()

    def test_stock_type(self):
        with self.assertRaises(ValueError):
            self.a.add_trade_record('None', 'Sell', 1, 2)

    def test_add_record_trades(self):
        self.a.add_trade_record('TEA', 'Buy', 10, 100)
        self.a.add_trade_record('POP', 'Sell', 33, 4)
        self.assertEqual(len(self.a.stock_trades), 2)
        self.assertEqual(self.a.stock_trades[0]['Price'], 10)
        self.assertEqual(self.a.stock_trades[-1]['Price'], 33)

    def test_dividend_yield(self):
        to_be_tested = self.a.dividend_yield('TEA', 100)
        self.assertEqual(to_be_tested, 0)
        to_be_tested = self.a.dividend_yield('POP', 10)
        self.assertEqual(to_be_tested, 0.8)

    def test_pe_ratio(self):
        to_be_tested = self.a.pe_ratio('TEA', 10)
        self.assertEqual(to_be_tested, None)
        to_be_tested = self.a.pe_ratio('POP', 10)
        self.assertEqual(to_be_tested, 12.5)

    def test_volume_weighted_stock_price(self):
        self.a.add_trade_record('TEA', 'Buy', 30, 2)
        self.a.add_trade_record('TEA', 'Sell', 25, 7)
        to_be_tested = self.a.volume_weighted_stock_price('TEA')
        self.assertAlmostEquals(to_be_tested, 26.1111111)


if __name__ == '__main__':
    unittest.main()
