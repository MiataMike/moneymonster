import numpy as np
import keras
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD
import csv

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


#x_train, x_test, y_train, y_test = grab_data(filename)
model = load_model('ai/gains.h5')

def run_fit(epochs):
    model.fit(x_train, y_train,
          epochs=epochs,
          batch_size=2280)
    score = model.evaluate(x_test, y_test, batch_size=128)
    print(score)
    model.save('ai/gains.h5')
#run_fit(2000)


sp100 = []
with open('data/constituents_csvSP100.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        sp100.append(row[0])
#print(sp100)

predictions = []
for ticker in sp100:
    tickerCSV = pd.read_csv('data/slices/{}.csv'.format(ticker))
    gain = model.predict(tickerCSV.values)
    print("{} will : {}".format(ticker,gain))
    predictions.append((gain,ticker))
predictions.sort()
top5 = []
bottom5 = []
p_len = len(predictions)-1

for i in range(0,5):
    top5.append(predictions[p_len-i])
    bottom5.append(predictions[i])
print("\n$")
print("Top 5 gains")
for i in top5:
    print("{} will gain: {}".format(i[1],i[0]))
print("~~~~")
print("Top 5 Losers")
for i in bottom5:
    print("{} will gain: {}".format(i[1],i[0]))
