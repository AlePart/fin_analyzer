

import datetime as dt

from finstat import FinSeries
from finstat import FinSeriesData
import random
import finstat.Stats as Stats


if __name__ == "__main__":
    ser = FinSeries()
    data1 = FinSeriesData()
    data1.name = "data1"
    data2 = FinSeriesData()
    data2.name = "data2"
    data3 = FinSeriesData()
    data3.name = "data3"

    for j in range(1000):
        now = dt.datetime.now()
        now = now - dt.timedelta(days=j)
        data1.add(now.date(),  j)
    for j in range(1000):
        now = dt.datetime.now()
        now = now - dt.timedelta(days=j)
        data2.add(now.date(),  random.randint(0, 10))
    
    for j in range(1400):
        now = dt.datetime.now()
        now = now - dt.timedelta(days=j)
        data3.add(now.date(),  random.randint(-30, 40))
    


    ser.addData(data1)
    ser.addData(data2)
    ser.addData(data3)
    Stats.corr(ser.getData())

