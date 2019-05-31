import numpy as np
import keras
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD

alpha = pd.read_csv('alpha.csv')
alpha.sample(frac=1)
alpha.columns = range(0,18)

x_train = alpha.iloc[:,1:16]
y_train = alpha.iloc[:,17]

model = Sequential()
model.add(Dense(16,input_dim=17,activation='relu'))
model.add(Dropout(.1))
model.add(Dense(8,activation='sigmoid'))
model.add(Dropout(.1))
model.add(Dense(6,activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)
score = model.evaluate(x_test, y_test, batch_size=128)
