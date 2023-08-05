import unittest

from tma.analyst.kline import KlineAnalyst


class KlineAnalystTest(unittest.TestCase):
    def setUp(self):
        ts_code = '000001.SH'
        start = '20181101'
        end = '20181223'
        freq = '60min'
        self.k = KlineAnalyst(ts_code=ts_code, start=start, end=end, freq=freq)

    def test_ma(self):
        self.k.ma_info()
        self.assertIn('close_ma5', self.k.kline.columns)
        self.assertIn('close_ma10', self.k.kline.columns)
        self.assertIn('close_ma20', self.k.kline.columns)

    def test_macd(self):
        self.k.macd_info()
        self.assertEqual(self.k.results.R101.value, '-5.4205, -5.3150, -4.2152')


if __name__ == '__main__':
    unittest.main()

