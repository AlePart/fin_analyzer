import unittest
import finstat.fin_series as s
import datetime as dt


class TestSeries(unittest.TestCase):
    def test_series_add(self):

        ser = s.FinSeries()
        data = s.FinSeriesData()
        for j in range(10):
            now = dt.datetime.now()
            now = now - dt.timedelta(days=j)
            data.add(now,  j)

        ser.addData(data)
        d = ser.getData()[0]
        self.assertEqual(len(d.dates), 10)
        self.assertEqual(len(d.values), 10)


if __name__ == '__main__':
    unittest.main()
