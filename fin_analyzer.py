

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
import sys




def correlation(operations : json):
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

def invested_pie(operations):
    invested = 0
    
    for operation in operations:
        price = get_buy_or_open_price(operation)
        invested += operation["quantity"] * price
            

    perc = dict()
    for operation in operations:
        perc[operation["ticker"]] = operation["quantity"] * get_buy_or_open_price(operation) / invested * 100

    plt.figure()
    plt.pie(perc.values(), labels=perc.keys(), autopct='%1.1f%%')
    plt.title("Allocation")

def get_buy_or_open_price(operation):
    if "price" in operation :
        return operation["price"]
    else:
        
        market_data = yf.download(operation["ticker"], start=operation["date"] , end=dt.date.fromisoformat(operation['date']) + dt.timedelta(days=1))
        return  market_data["Open"].iloc[0]
    


def portfolio_gains(operations):

    position_data = get_position_data(operations)

    dataframes = pd.DataFrame()
    for _, value in position_data.items():
        if dataframes.empty:
            dataframes = pd.DataFrame({'dates': value.index, value.name: value.values})
        else:
            df_temp = pd.DataFrame({'dates': value.index, value.name: value.values})
            dataframes = pd.merge(dataframes, df_temp, on='dates', how='outer')

    dataframes = dataframes.set_index('dates')
    dataframes = dataframes.pct_change()
    dataframes = dataframes.fillna(0)
    dataframes = dataframes + 1
    dataframes = dataframes.cumprod()
    dataframes = dataframes - 1
    dataframes = dataframes * 100

    plt.figure()
    sns.lineplot(data=dataframes, x=dataframes.index, y=dataframes.sum(axis=1))
    plt.ylabel("Gains (%)")
    plt.xlabel("Date")
    plt.title("Portfolio Gains")

def get_position_data(operations):
    position_data = dict()
    for operation in operations:
        market_data = yf.download(operation["ticker"], start=operation["date"] , end=dt.datetime.now()- dt.timedelta(days=1))
            
        if operation["adj_close"] == True:
            position_data[operation["ticker"]] = market_data["Adj Close"] * operation["quantity"]
        else:
            position_data[operation["ticker"]] = market_data["Close"] * operation["quantity"]

    if "price" in operation :  
        position_data[operation["ticker"]].iloc[0] = operation["price"] * operation["quantity"]

            
    return position_data


def portfolio_history(operations):
    position_data = get_position_data(operations)
    dataframes = pd.DataFrame()
    for _, value in position_data.items():
        if dataframes.empty:
            dataframes = pd.DataFrame({'dates': value.index, value.name: value.values})
        else:
            df_temp = pd.DataFrame({'dates': value.index, value.name: value.values})
            dataframes = pd.merge(dataframes, df_temp, on='dates', how='outer')
    
    plt.figure()
    dataframes = dataframes.set_index('dates')
    sns.lineplot(data=dataframes, x=dataframes.index, y=dataframes.sum(axis=1))
    plt.ylabel("Portfolio Value")
    plt.xlabel("Date")
    plt.title("Portfolio History")
    

def check_operations(operations) :
    print("*** Verifying operations ***")
    for operation in operations:
        print(operation)
        if "date" not in operation:
            print("Error: Operation must have a date")
            return False
        if "ticker" not in operation:
            print("Error: Operation must have a ticker")
            return False
        if "quantity" not in operation:
            print("Error: Operation must have a quantity")
            return False
        if "adj_close" not in operation:
            print("Error: Operation must have a adj_close flag")
            return False
    print("*** Operations are correct ***")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        operations_file = sys.argv[1]
    else:
        operations_file = "operations.json"

    file = open(operations_file, "r")
    operations = json.load(file)
    file.close()
    if check_operations(operations) == False:
        exit(1)

    correlation(operations)
    invested_pie(operations)
    portfolio_history(operations)
    portfolio_gains(operations)

    plt.show()

    

   
        
    

    

    

    
    
    

    



    


