import datetime as dt
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys

from finstat import FinSeriesData
from finstat import FinSeries
from finstat import settings
from finstat import statistics
from data_repository import YahooFinanceRepository as yfr
from data_repository import DataRepositoryInterface



def correlation(operations: json, repository : DataRepositoryInterface,filename=""):
    all_data = dict()
    for operation in operations:
        all_data[operation["ticker"]] = repository.get_data(operation["ticker"])

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

    return statistics.corr(ser.getData(), filename)


def invested_pie(operations, repository : DataRepositoryInterface, filename=""):
    invested = 0

    for operation in operations:
        price = get_buy_or_open_price(operation, repository)
        invested += operation["quantity"] * price
    perc = dict()
    for operation in operations:
        if operation["ticker"] not in perc:
            perc[operation["ticker"]] = operation["quantity"] * \
                get_buy_or_open_price(operation,repository)
        else:
            perc[operation["ticker"]] += operation["quantity"] * \
                get_buy_or_open_price(operation,repository)

    for key, value in perc.items():
        perc[key] = value / invested * 100

    plt.figure("Allocation - " + filename)
    plt.pie(perc.values(), labels=perc.keys(), autopct='%1.1f%%')
    plt.title("Allocation")
    return perc


def get_buy_or_open_price(operation, repository : DataRepositoryInterface):
    if "price" in operation:
        return operation["price"]
    else:

        #market_data = yf.download(operation["ticker"], start=operation["date"], end=dt.date.fromisoformat(operation['date']) + dt.timedelta(days=30))
        market_data = repository.get_data_from_date_range(operation["ticker"], operation["date"], dt.date.fromisoformat(operation['date']) + dt.timedelta(days=30))

        return market_data["Open"].iloc[0]


def portfolio_gains(operations, repository : DataRepositoryInterface,filename=""):

    position_data = get_position_data(operations, repository)

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
    return dataframes


def get_position_data(operations, repository : DataRepositoryInterface):
    position_data = dict()
    for operation in operations:
        market_data = repository.get_data_from_date_range(operation["ticker"], operation["date"], dt.datetime.now() - dt.timedelta(days=1))

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


def portfolio_history(operations, repository : DataRepositoryInterface, filename=""):
    position_data = get_position_data(operations, repository)
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
    return dataframes


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


def current_assets_gain_loss_perc(operations,repository : DataRepositoryInterface, filename=""):
    gain_loss = dict()
    for operation in operations:
        market_data = repository.get_data_from_date_range(operation["ticker"], operation["date"], dt.datetime.now() - dt.timedelta(days=1))
        if operation["adj_close"] == True:
            gain_loss[operation["ticker"]] = (
                market_data["Adj Close"].iloc[-1] - get_buy_or_open_price(operation,repository)) / get_buy_or_open_price(operation,repository) * 100
        else:
            gain_loss[operation["ticker"]] = (
                market_data["Close"].iloc[-1] - get_buy_or_open_price(operation,repository)) / get_buy_or_open_price(operation, repository) * 100

    plt.figure("Current Assets Gain/Loss - " + filename)
    sns.barplot(x=list(gain_loss.keys()), y=list(gain_loss.values()))
    plt.ylabel("Gain/Loss")
    plt.xlabel("Ticker")
    plt.title("Current Assets Gain/Loss")


def calculate_weighted_correlation(file, corr, percentage):
    weighted_corr = corr.copy()

    for key, value in percentage.items():
        weighted_corr.loc[key] = weighted_corr.loc[key] * value / 100
        weighted_corr.loc[:, key] = weighted_corr.loc[:, key] * value / 100

    for key, value in percentage.items():
        weighted_corr.loc[key, key] = None

    plt.figure("Weighted Correlation - " + file.name)
    sns.heatmap(weighted_corr, annot=True, linewidths=0.5,
                cmap='coolwarm', fmt=".4f")
    plt.ylabel("Ticker")
    plt.xlabel("Ticker")

    plt.title("Weighted Correlation")

    return weighted_corr

def calculate_weighted_correlation_gain_loss(file, weigted_corr, gain_loss):
    wc = weigted_corr.copy()
    # selet last line in gain_loss DataFrame
    
    gl = gain_loss.copy().loc[[gain_loss.index[-1]]]
    
    #W weighted corr find NaN and replace with 0
    wc = wc.fillna(0)

    #all gl values must be translated to positive 
    gl = gl + 100



    for key, value in gl.iloc[0].items():
        wc.loc[key] = wc.loc[key] * value
        wc.loc[:, key] = wc.loc[:, key] * value 
    
    for key, value in gl.items():
        wc.loc[key, key] = None
    

    
    plt.figure("Weighted Correlation Gain Loss - " + file.name)
    sns.heatmap(wc, annot=True, linewidths=0.5, fmt=".2f", cmap='PiYG')
    plt.ylabel("Ticker")
    plt.xlabel("Ticker")

    plt.title("Weighted Correlation * Gain/Loss %")

    return weighted_corr


def assets_history_perc(history, filename=""):
    position_data = history
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
    dataframes = dataframes.fillna(pd.NA)
    dataframes = dataframes + 1
    dataframes = dataframes.cumprod()
    dataframes = dataframes - 1
    dataframes = dataframes * 100
    plt.figure("Assets History - " + filename)
    dataframes_melt = dataframes.reset_index().melt(
        'dates', var_name='a', value_name='b')
    sns.lineplot(data=dataframes_melt, x='dates', y='b', hue='a')
    plt.ylabel("Gains (%)")
    plt.xlabel("Date")
    plt.title("Assets History")
    return dataframes_melt


def assets_volatility_perc(assets_history, percentage):
    volatility = dict()
    for key, value in percentage.items():
        volatility[key] = assets_history[assets_history['a'] == key]['b'].std()
    volatility_perc = dict()
    for key, value in volatility.items():
        volatility_perc[key] = value / percentage[key] * 100
    # sort
    volatility_perc = dict(
        sorted(volatility_perc.items(), key=lambda item: item[1], reverse=True))
    plt.figure("Volatility % - " + f.name)
    sns.barplot(x=list(volatility_perc.keys()),
                y=list(volatility_perc.values()))
    plt.ylabel("Volatility %")
    plt.xlabel("Ticker")
    plt.title("Volatility %")
    return volatility_perc


def weigted_correlation_volatility(f, weighted_corr, assets_vola_perc):
    for key, value in weighted_corr.items():
        weighted_corr[key] = weighted_corr[key] * assets_vola_perc[key] / 100

    plt.figure("Weighted Correlation * Volatility % - " + f.name)
    sns.heatmap(weighted_corr, annot=True, linewidths=0.5,
                cmap='coolwarm', fmt=".4f")
    plt.ylabel("Ticker")
    plt.xlabel("Ticker")
    plt.title("Weighted Correlation * Volatility %")


if __name__ == "__main__":

    operations_files = []
    repo = yfr()
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
            
            for operation in operations:
                repo.fetch(operation["ticker"])


        corr = correlation(operations, repo, f.name)
        percentage = invested_pie(operations, repo,   f.name)
        weighted_corr = calculate_weighted_correlation(f, corr, percentage)
        history = portfolio_history(operations,repo, f.name)
        gain_loss = portfolio_gains(operations,repo, f.name)
        current_assets_gain_loss_perc(operations,repo, f.name)
        assets_history = assets_history_perc(history, f.name)
        assets_vola_perc = assets_volatility_perc(assets_history, percentage)

        weigted_correlation_volatility(f, weighted_corr, assets_vola_perc)
        weighted_corr_gain_loss = calculate_weighted_correlation_gain_loss(f, weighted_corr, gain_loss )

    plt.show(block=False)

    input("Press Enter to exit...")
    plt.close("all")
