import pandas as pd
from finstat import FinSeries as FinSeries
import matplotlib.pyplot as plt
import seaborn as sns


def corr(data : any):

    dataframes = pd.DataFrame()
    for d in data:
        d.sort()
        if dataframes.empty:
            dataframes = pd.DataFrame({'dates': d.dates, 'values': d.values})
        else:
            df_temp = pd.DataFrame({'dates': d.dates, 'values': d.values})
            dataframes = pd.merge(dataframes, df_temp, on='dates', how='outer')
    
    dataframes = dataframes.set_index('dates')
   # print(dataframes)
    corr = dataframes.corr()
    sns.heatmap(corr, annot=True)
    plt.show()
    

        
    
    
    
        
    
        