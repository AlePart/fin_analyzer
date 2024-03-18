

import datetime as dt

from finstat import FinSeries
from finstat import FinSeriesData
import random
import finstat.Stats as Stats
import yfinance as yf
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd




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
    invested = 0
    for operation in operations:
        invested += operation["quantity"] * operation["price"]

    perc = dict()
    for operation in operations:
        perc[operation["ticker"]] = operation["quantity"] * operation["price"] / invested * 100

    plt.figure()
    plt.pie(perc.values(), labels=perc.keys(), autopct='%1.1f%%')
 


    #portfolio history
    position_data = dict()
    for operation in operations:
        print(operation["date"])
        market_data = yf.download(operation["ticker"], start=operation["date"])
        position_data[operation["ticker"]] = market_data["Adj Close"] * operation["quantity"]

    dataframes = pd.DataFrame()
    for _, value in position_data.items():
        if dataframes.empty:
            dataframes = pd.DataFrame({'dates': value.index, value.name: value.values})
        else:
            df_temp = pd.DataFrame({'dates': value.index, value.name: value.values})
            dataframes = pd.merge(dataframes, df_temp, on='dates', how='outer')
    
    print(dataframes.info())

    plt.figure()
    dataframes = dataframes.set_index('dates')
    sns.lineplot(data=dataframes, x=dataframes.index, y=dataframes.sum(axis=1))
    plt.show()

    

   
        
    

    

    

    
    
    

    



    


