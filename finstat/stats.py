import pandas as pd
from finstat import FinSeries as FinSeries
from finstat import FinSeriesData as FinSeriesData
import matplotlib.pyplot as plt
import seaborn as sns


def corr(data: list[FinSeriesData], filename=""):

    dataframes = pd.DataFrame()
    for d in data:
        d.sort()
        if dataframes.empty:
            dataframes = pd.DataFrame({'dates': d.dates, d.name: d.values})
        else:
            df_temp = pd.DataFrame({'dates': d.dates, d.name: d.values})
            dataframes = pd.merge(dataframes, df_temp, on='dates', how='outer')

    dataframes = dataframes.set_index('dates')
    corr = dataframes.corr()
    plt.figure("Correlation Matrix - " + filename)
    sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title("Correlation")

    return corr


def mean(data: FinSeriesData):
    return sum(data.values) / len(data.values)


def median(data: FinSeriesData):
    data.sort()
    if len(data.values) % 2 == 0:
        return (data.values[len(data.values) // 2] + data.values[len(data.values) // 2 - 1]) / 2
    else:
        return data.values[len(data.values) // 2]


def mode(data: FinSeriesData):
    data.sort()
    count = {}
    for i in data.values:
        if i in count:
            count[i] += 1
        else:
            count[i] = 1
    return max(count, key=count.get)


def var(data: FinSeriesData):
    mean = sum(data.values) / len(data.values)
    return sum((x - mean) ** 2 for x in data.values) / len(data.values)


def std(data: FinSeriesData):
    return var(data) ** 0.5
