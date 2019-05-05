import pandas as pd
from pandas.plotting import autocorrelation_plot
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
ts = TimeSeries(key='DONT1C40C86U80WO',output_format='pandas', indexing_type='date')
#data, meta_data = ts.get_intraday(symbol='MSFT',interval='1min', outputsize='compact')
#print(data["4. close"])
#data.plot()
#data["4. close"].plot()
#plt.show()
#ti = TechIndicators(key='DONT1C40C86U80WO', output_format='pandas')
#data, meta_data = ti.get_bbands(symbol='MSFT', interval='60min', time_period=60)
#data.plot()
#plt.title('BBbands indicator for  MSFT stock (60 min)')
#plt.show()

#print(data)
#null = input("press enter to continue")
#df=pd.DataFrame(data)
#print(df.iloc[2]['Real Upper Band'])

##get test data
HaS = []
yahooCharts = ["3436.T.csv","CVX (1).csv","ITX.MC.csv","XLF.csv","GPRO.csv"]
for chartname in yahooCharts:
    HaS.append(pd.read_csv(chartname))
HaS[1]['Open'].plot()
plt.show()