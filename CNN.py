import pandas as pd
from pandas.plotting import autocorrelation_plot
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import numpy as np
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from tensorflow.python import keras
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import Conv1D
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import math

TIME_PERIODS = 10

dataframe = pd.read_csv('SPY.csv', usecols=[5,6], engine='python')
dataset = dataframe.values
dataset = dataset.astype('float32')
dataset = np.array(dataset)
dataset = dataset.reshape(len(dataset),2,1)
labels = [dataset[0][0]]
for i in range(len(dataset)-1):
    labels.append(dataset[i+1,0])


train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
print(len(train), len(test))

BATCH_SIZE = 400
EPOCHS = 50

model = Sequential()

model.add(Conv1D(100,1,activation='relu',input_shape=(2,1)))
model.add(Dense(1))
print(model.summary())
model.compile(loss='categorical_crossentropy',
                optimizer='adam', metrics=['accuracy'])

callbacks_list = [
    keras.callbacks.ModelCheckpoint(
        filepath='best_model.{epoch:02d}-{val_loss:.2f}.h5',
        monitor='val_loss', save_best_only=True),
    keras.callbacks.EarlyStopping(monitor='acc', patience=1)
]
history = model.fit(dataset,
                      labels,
                      batch_size=BATCH_SIZE,
                      epochs=EPOCHS,
                      callbacks=callbacks_list,
                      validation_split=0.2,
                      verbose=1)