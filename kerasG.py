import numpy as np
import keras
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD

alphadata = pd.read_csv('alpha.csv')
alpha = alphadata.sample(frac=1)
alpha.columns = range(0,18)

trainLen=int(len(alpha)*.7)


x_train = alpha.iloc[0:trainLen,0:17]
y_train = alpha.iloc[0:trainLen,17]
#y_train = keras.utils.to_categorical(y_train)
x_test = alpha.iloc[trainLen:len(alpha),0:17]
y_test = alpha.iloc[trainLen:len(alpha),17]
#y_test = keras.utils.to_categorical(y_test)

model = Sequential()
model.add(Dense(17,input_dim=17)
#model.add(Dropout(.001))
model.add(Dense(20,activation='tanh'))
model.add(Dense(1,activation='linear'))

sgd = SGD(lr=0.00001, decay=1e-6, momentum=0.9, nesterov=True)
rms = keras.optimizers.RMSprop(lr = 1e-4, rho=0.9, epsilon=1e-9, decay=1e-6)
model.compile(loss='mean_squared_error',
              optimizer=rms,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)
score = model.evaluate(x_test, y_test, batch_size=128)
print(score)
F = pd.read_csv('F.csv')
print("F will:     {}".format(model.predict(F.values)))
GPRO = pd.read_csv('GPRO.csv')
print("GOPRO will: {}".format(model.predict(GPRO.values)))
