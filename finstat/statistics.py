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

