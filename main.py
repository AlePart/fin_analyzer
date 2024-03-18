

import datetime as dt

from finstat import FinSeries
from finstat import FinSeriesData
import random
import finstat.Stats as Stats
import yfinance as yf
import json




def printCorrelation(operations : json):
    all_data = dict()
    for operation in operations:
        all_data[operation["ticker"]] = yf.download(operation["ticker"])
        
    common_start_date = dt.datetime(1970, 1, 1)
    ser = FinSeries()
    for( key, value) in all_data.items():
        if(common_start_date < value[0:1].index[0]):
            common_start_date = value[0:1].index[0]

    for( key, value) in all_data.items():
        data1 = FinSeriesData()
        data1.name = key
        for index, row in value.iterrows():
            data1.add(index.date(), row["Adj Close"])
        ser.addData(data1)

    Stats.corr(ser.getData())

if __name__ == "__main__":

    operations_file = "operations.json"
    file = open(operations_file, "r")
    operations = json.load(file)
    file.close()
    printCorrelation(operations)
    



    


