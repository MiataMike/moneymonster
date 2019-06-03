import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

model = keras.models.load_model('hains.h5')

guesses = []
price_predictions= []
price_close = []
filename = input("what stock would you like to backtest?")
F = pd.read_csv('{}back.csv'.format(filename))
#print("F    will:{}".format(model.predict(F.values)))
for day in range(len(F)):
    Ftmp = F.iloc[day].values[0:17]
    closing = F.iloc[day,17]
    input = np.reshape(Ftmp,(-1,len(Ftmp)))
    guess = model.predict(input)
    guesses.append(guess)
    price_close.append(closing)

price_predictions.append(price_close[0]) #initialize guess
for day in range(0,len(guesses)-1):
    gain = (guesses[day][0][0] + 100) / 100
    price_predictions.append(price_close[day] * gain)


error = []
for i in range(len(price_close)):
    error.append(price_close[i] - price_predictions[i])




x = range(30)
y = range(8,12)
fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(price_close, label='price')
ax1.plot(price_predictions[0:len(price_close)], label='prediction')
plt.legend()
plt.show()
ax1.plot(error)
plt.show()
