import csv
import math
import time

start = time.time()
masterDataFieldnames = ['N_open0', 'N_open1', 'N_open2', 'N_open3', 'N_high0', 'N_high1', 'N_high2', 'N_high3',
             'N_low0', 'N_low1', 'N_low2', 'N_low3', 'N_close0', 'N_close1', 'N_close2', 'N_close3',
             'N_vol0', 'N_vol1', 'N_vol2', 'N_vol3', 'N_rsi', 'N_adx']
#blow away data, write header
alphaFieldnames = ['N_open1', 'N_open2', 'N_open3',  'N_high1', 'N_high2', 'N_high3',
             'N_low1', 'N_low2', 'N_low3', 'N_close1', 'N_close2', 'N_close3',
             'N_vol1', 'N_vol2', 'N_vol3', 'N_rsi', 'N_adx', 'tag']
with open('alpha.csv','w') as alphafile:
        writer = csv.writer(alphafile)
        writer.writerow(alphaFieldnames)

with open('masterData.csv') as csvfile:
    reader = csv.DictReader(csvfile,fieldnames=masterDataFieldnames, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        high = .01
        medium = .004
        outputList = []
        # get tag
        today_close = math.atanh(row['N_close0'])
        yesterday_close = math.atanh(row['N_close1'])
        gainz = today_close - yesterday_close
        if (gainz >= high):
            tag = 0
        elif (gainz >= medium) & (gainz < high):
            tag = 1
        elif (gainz >= .0) & (gainz < medium):
            tag = 2
        elif (gainz >= -medium) & (gainz < .0):
            tag = 3
        elif (gainz >= -high):
            tag = 4
        else:
            tag = 5
        outputList = [row['N_open1'], row['N_open2'], row['N_open3'], row['N_high1'], row['N_high2'], row['N_high3'],
             row['N_low1'], row['N_low2'], row['N_low3'], row['N_close1'], row['N_close2'], row['N_close3'],
             row['N_vol1'], row['N_vol2'], row['N_vol3'], row['N_rsi'], row['N_adx'], tag]
        with open('alpha.csv', 'a') as alphafile:
            writer = csv.writer(alphafile)
            writer.writerow(outputList)

end = time.time()
print("{} seconds".format(end-start))
