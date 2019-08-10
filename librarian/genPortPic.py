import csv
import matplotlib.pyplot as plt

#this file is manually edited each week to include number of days and profits
f = open('data/portfolio.csv')
datareader=csv.reader(f)

days = []
portfolio = []

for i in datareader:
    days.append(i[0])
    portfolio.append(float(i[1])+100000)

plt.style.use('dark_background')
plt.plot(days,portfolio,'g')
plt.xlabel('Days')
plt.ylabel('$')
plt.title('Portfolio Value')

plt.savefig('data/portfolio.png')


