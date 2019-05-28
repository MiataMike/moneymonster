import pandas as pd
from pandas.plotting import autocorrelation_plot
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import Conv1D
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import math

#ts = TimeSeries(key='DONT1C40C86U80WO',output_format='pandas', indexing_type='date')
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
dataframe = pd.read_csv('CVX.csv', usecols=[5], engine='python')
dataset = dataframe.values
dataset = dataset.astype('float32')
#HaS[4]['Open'].plot()
#plt.show()


# normalize the dataset
maxx = max(dataset)
minn = min(dataset)
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

def create_dataset(dataset, look_back):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

# split into train and test sets
train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(len(train), len(test))

look_back = 3
trainX, trainY = create_dataset(train, look_back)
testX, testY = create_dataset(test, look_back)


# reshape input to be [samples, time steps, features]
trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
#
#
# # create and fit the LSTM network
model = Sequential()
model.add(Dense(4,input_shape=(1, look_back),activation='relu'))
model.add(LSTM(100))
model.add(Dense(4,activation='tanh'))
model.add(Dense(1))
model.compile(optimizer='rmsprop',
              loss='mean_absolute_error')
model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=2)

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform([trainY])
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform([testY])
# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:,0]))
print('Test Score: %.2f RMSE' % (testScore))
# shift train predictions for plotting
trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict
# shift test predictions for plotting
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(look_back*2)+1:len(dataset)-1, :] = testPredict
# plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()