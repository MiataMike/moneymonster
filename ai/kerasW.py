import numpy as np
import keras
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD

filename = 'data/weekly_input_data.csv'
def grab_data(filename):
    alphadata = pd.read_csv(filename)
    alpha = alphadata.sample(frac=1)
    alpha = alpha.sample(frac=1)
    alpha = alpha.sample(frac=1)
    alpha.columns = range(0,9)
    trainLen=int(len(alpha)*.7)


    x_train = alpha.iloc[0:trainLen,0:8]
    y_train = alpha.iloc[0:trainLen,8]
#y_train = keras.utils.to_categorical(y_train)
    x_test = alpha.iloc[trainLen:len(alpha),0:8]
    y_test = alpha.iloc[trainLen:len(alpha),8]
#y_test = keras.utils.to_categorical(y_test)
    return x_train, x_test, y_train, y_test

x_train, x_test, y_train, y_test = grab_data(filename)

model = Sequential()
model.add(Dense(8,input_dim=8))
model.add(Dense(200,activation='tanh'))
model.add(Dropout(.4))
model.add(Dense(200,activation='tanh'))
model.add(Dropout(.4))
model.add(Dense(200,activation='tanh'))
#model.add(Dropout(.4))
model.add(Dense(20,activation='softmax'))
#model.add(Dropout(.3))
model.add(Dense(1,activation='linear'))

sgd = SGD(lr=0.00001, decay=1e-6, momentum=0.9, nesterov=True)
rms = keras.optimizers.RMSprop(lr = 1e-2, rho=0.9, epsilon=1e-9, decay=1e-6)
model.compile(loss='mean_squared_error',
              optimizer='adam')
def run_fit(epochs):
    model.fit(x_train, y_train,
          epochs=epochs,
          batch_size=1024)
    score = model.evaluate(x_test, y_test, batch_size=128)
    print(score)

    model.save('ai/wains.h5')

run_fit(100)
