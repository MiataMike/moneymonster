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
y_train = keras.utils.to_categorical(y_train)
x_test = alpha.iloc[trainLen:len(alpha),0:17]
y_test = alpha.iloc[trainLen:len(alpha),17]
y_test = keras.utils.to_categorical(y_test)

model = Sequential()
model.add(Dense(17,input_dim=17,activation='relu'))
#model.add(Dropout(.001))
model.add(Dense(64,activation='relu'))
model.add(Dropout(.9))
model.add(Dense(32,activation='relu'))
model.add(Dropout(.9))
model.add(Dense(16,activation='relu'))
model.add(Dropout(.9))
model.add(Dense(8,activation='relu'))
model.add(Dense(6,activation='softmax'))

sgd = SGD(lr=0.5, decay=1e-8, momentum=0, nesterov=True)
#rms = keras.optimizers.RMSprop(lr = 0.001, rho=0.9, epsilon=None, decay=0.0)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['categorical_accuracy'])

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)
score = model.evaluate(x_test, y_test, batch_size=128)
print(score)
F = pd.read_csv('F.csv')
print("F will:     {}".format(model.predict(F.values)))
GPRO = pd.read_csv('GPRO.csv')
print("GOPRO will: {}".format(model.predict(GPRO.values)))
