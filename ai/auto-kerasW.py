import numpy as np
import keras
import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils
from keras.optimizers import SGD
import csv
import time

#start timer
start = time.time()

#this is the file with the processed time seris data (output of dataClassifierG.py)
filename = 'data/weekly_input_data.csv'
def grab_data(filename):
    alphadata = pd.read_csv(filename)
    alpha = alphadata.sample(frac=1) #scramble data order
    alpha = alpha.sample(frac=1) #scramble the scrambled data
    alpha = alpha.sample(frac=1) #""
    alpha.columns = range(0,9) #reshape array
    trainLen=int(len(alpha)*.7) #only use .7 for training data

    x_train = alpha.iloc[0:trainLen,0:8] #data
    y_train = alpha.iloc[0:trainLen,8] #tag
#y_train = keras.utils.to_categorical(y_train)
    x_test = alpha.iloc[trainLen:len(alpha),0:8] #test data
    y_test = alpha.iloc[trainLen:len(alpha),8] #test tag
#y_test = keras.utils.to_categorical(y_test)
    return x_train, x_test, y_train, y_test

#read in the data
print("loading training data")
x_train, x_test, y_train, y_test = grab_data(filename)
print("Waking AI")
#load the Keras model (start with last wee'd model)
model = load_model('ai/wains.h5')

def run_fit(epochs):
    model.fit(x_train, y_train,
          epochs=epochs,
          batch_size=2048)
    score = model.evaluate(x_test, y_test, batch_size=128)
    print(score)
    model.save('ai/wains.h5')

#TODO: time and tune to run a while
print("running 2000 iterations")
run_fit(2000)
#this takes about 12 hours

#time to inference
#create list of ticker targets
sp100 = []
with open('data/constituents_csvSP100.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        sp100.append(row[0])
#print(sp100)

#inference
print("inferencing...")
predictions = []
for ticker in sp100:
    tickerCSV = pd.read_csv('data/slices/{}.csv'.format(ticker))
    gain = model.predict(tickerCSV.values)
#    print("{} will : {}".format(ticker,gain))
    predictions.append((gain,ticker))

#rank 
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

#output to files
with open('data/top5.csv', mode = 'w') as algoOut:
    writer = csv.writer(algoOut)
    for prediction in top5:
        writer.writerow([prediction[1]])

with open('data/bottom5.csv', mode = 'w') as algoOut:
    writer = csv.writer(algoOut)
    for prediction in bottom5:
        writer.writerow([prediction[1]])

print("{} seconds\n".format(time.time()-start))
