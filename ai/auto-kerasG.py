import numpy as np
import keras
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD

filename = 'data/gains.csv'
def grab_data(filename):
    alphadata = pd.read_csv(filename)
    alpha = alphadata.sample(frac=1)
    alpha = alpha.sample(frac=1)
    alpha = alpha.sample(frac=1)
    alpha.columns = range(0,18)
    trainLen=int(len(alpha)*.7)


    x_train = alpha.iloc[0:trainLen,0:17]
    y_train = alpha.iloc[0:trainLen,17]
#y_train = keras.utils.to_categorical(y_train)
    x_test = alpha.iloc[trainLen:len(alpha),0:17]
    y_test = alpha.iloc[trainLen:len(alpha),17]
#y_test = keras.utils.to_categorical(y_test)
    return x_train, x_test, y_train, y_test


def run_fit(epochs):
    model.fit(x_train, y_train,
          epochs=epochs,
          batch_size=2280)
    score = model.evaluate(x_test, y_test, batch_size=128)
    print(score)
    F = pd.read_csv('data/slices/F.csv')
    print("F    will:{}".format(model.predict(F.values)))
    GPRO = pd.read_csv('data/slices/VTI.csv')
    print("VTI  will: {}".format(model.predict(GPRO.values)))
    TSLA = pd.read_csv('data/slices/TSLA.csv')
    print("TSLA will: {}".format(model.predict(TSLA.values)))
    BEN = pd.read_csv('data/slices/BEN.csv')
    print("BEN  will: {}".format(model.predict(BEN.values)))



model = load_model('ai/gains.h5')
x_train, x_test, y_train, y_test = grab_data(filename)
run_fit(100)
