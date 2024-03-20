import datetime as dt
import yfinance as yf
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys

from finstat import FinSeriesData
from finstat import FinSeries
from finstat import settings
from finstat import stats


def correlation(operations: json, filename=""):
    all_data = dict()
    for operation in operations:
        all_data[operation["ticker"]] = yf.download(operation["ticker"])

    common_start_date = dt.datetime(1970, 1, 1)
    ser = FinSeries()
    for (key, value) in all_data.items():
        if (common_start_date < value[0:1].index[0]):
            common_start_date = value[0:1].index[0]

    for (key, value) in all_data.items():
        data1 = FinSeriesData()
        data1.name = key
        for index, row in value.iterrows():
            data1.add(index.date(), row["Adj Close"])
        ser.addData(data1)

    stats.corr(ser.getData(), filename)


def invested_pie(operations, filename=""):
    invested = 0

    for operation in operations:
        price = get_buy_or_open_price(operation)
        invested += operation["quantity"] * price

    perc = dict()
    for operation in operations:
        perc[operation["ticker"]] = operation["quantity"] * \
            get_buy_or_open_price(operation) / invested * 100

    plt.figure("Allocation - " + filename)
    plt.pie(perc.values(), labels=perc.keys(), autopct='%1.1f%%')
    plt.title("Allocation")


def get_buy_or_open_price(operation):
    if "price" in operation:
        return operation["price"]
    else:

        market_data = yf.download(operation["ticker"], start=operation["date"], end=dt.date.fromisoformat(
            operation['date']) + dt.timedelta(days=30))

        return market_data["Open"].iloc[0]


def portfolio_gains(operations, filename=""):

    position_data = get_position_data(operations)

    dataframes = pd.DataFrame()
    for key, value in position_data.items():
        if dataframes.empty:
            dataframes = pd.DataFrame(
                {'dates': value.index, key: value.values})
        else:
            df_temp = pd.DataFrame({'dates': value.index, key: value.values})
            dataframes = pd.merge(dataframes, df_temp, on='dates', how='outer')

    dataframes = dataframes.set_index('dates')
    dataframes = dataframes.pct_change()
    dataframes = dataframes.fillna(0)
    dataframes = dataframes + 1
    dataframes = dataframes.cumprod()
    dataframes = dataframes - 1
    dataframes = dataframes * 100

    plt.figure("Portfolio Gains - " + filename)
    sns.lineplot(data=dataframes, x=dataframes.index, y=dataframes.sum(axis=1))
    plt.ylabel("Gains (%)")
    plt.xlabel("Date")
    plt.title("Portfolio Gains")


def get_position_data(operations):
    position_data = dict()
    for operation in operations:
        market_data = yf.download(
            operation["ticker"], start=operation["date"], end=dt.datetime.now() - dt.timedelta(days=1))

        if operation["adj_close"] == True:
            position_data[operation["ticker"]
                          ] = market_data["Adj Close"] * operation["quantity"]
        else:
            position_data[operation["ticker"]
                          ] = market_data["Close"] * operation["quantity"]

    if "price" in operation:
        position_data[operation["ticker"]
                      ].iloc[0] = operation["price"] * operation["quantity"]

    return position_data


def portfolio_history(operations, filename=""):
    position_data = get_position_data(operations)
    dataframes = pd.DataFrame()

    for key, value in position_data.items():
        if dataframes.empty:
            dataframes = pd.DataFrame(
                {'dates': value.index, key: value.values})
        else:
            df_temp = pd.DataFrame({'dates': value.index, key: value.values})
            dataframes = pd.merge(dataframes, df_temp, on='dates', how='outer')

    plt.figure("Portfolio History - " + filename)
    dataframes = dataframes.set_index('dates')
    sns.lineplot(data=dataframes, x=dataframes.index, y=dataframes.sum(axis=1))
    plt.ylabel("Portfolio Value")
    plt.xlabel("Date")
    plt.title("Portfolio History")


def check_operations(operations: list[dict]) -> bool:
    print("*** Verifying operations ***")
    for operation in operations:
        print(operation)
        for field in settings.OPERATION_FIELDS:
            if field not in operation:
                print(f"Error: Operation must have {field} field")
                return False
    print("*** Operations are correct ***")
    return True


def current_assets_gain_loss_perc(operations, filename=""):
    gain_loss = dict()
    for operation in operations:
        market_data = yf.download(
            operation["ticker"], start=operation["date"], end=dt.datetime.now() - dt.timedelta(days=1))
        if operation["adj_close"] == True:
            gain_loss[operation["ticker"]] = (
                market_data["Adj Close"].iloc[-1] - get_buy_or_open_price(operation)) / get_buy_or_open_price(operation) * 100
        else:
            gain_loss[operation["ticker"]] = (
                market_data["Close"].iloc[-1] - get_buy_or_open_price(operation)) / get_buy_or_open_price(operation) * 100

    plt.figure("Current Assets Gain/Loss - " + filename)
    sns.barplot(x=list(gain_loss.keys()), y=list(gain_loss.values()))
    plt.ylabel("Gain/Loss")
    plt.xlabel("Ticker")
    plt.title("Current Assets Gain/Loss")


if __name__ == "__main__":

    operations_files = []
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:

            operations_files.append(arg)
    else:
        operations_files.append("operations.json")

    for path in operations_files:
        print(f"Processing file: {path}")
        with open(path, "r") as f:
            operations = json.load(f)
            if check_operations(operations) == False:
                exit(1)

            correlation(operations, f.name)
            invested_pie(operations, f.name)
            portfolio_history(operations, f.name)
            portfolio_gains(operations, f.name)
            current_assets_gain_loss_perc(operations, f.name)

    plt.show(block=False)

    input("Press Enter to exit...")
    plt.close("all")
