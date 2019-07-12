import csv
import math
import time
import numpy

#timer function start
start = time.time()

print("Processing data")
#field names for input data csv (masterData.csv)
masterFile = 'data/masterData.csv'
masterDataFieldnames = [ 'N_close0', 'N_close1', 'N_close2', 'N_close3',
             'N_vol0', 'N_vol1', 'N_vol2', 'N_vol3', 'N_rsi', 'N_adx']

#blow away data, write header for output
#note: alpha is a legacy name
alphaFieldnames = [ 'N_close1', 'N_close2', 'N_close3',
             'N_vol1', 'N_vol2', 'N_vol3', 'N_rsi', 'N_adx', 'tag']
with open('data/weekly_input_data.csv','w') as alphafile:
        writer = csv.writer(alphafile)
        writer.writerow(alphaFieldnames)

#process each line in masterData
with open(masterFile) as csvfile:
    reader = csv.DictReader(csvfile,fieldnames=masterDataFieldnames, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        outputList = []
        # get tag
        today_close = math.atanh(row['N_close0'])
        yesterday_close = math.atanh(row['N_close1'])
        gainz = today_close - yesterday_close
        tag = gainz*100
        #this nasty line is just translating the fields from the input file masterData to the output format
        outputList = [row['N_close1'], row['N_close2'], row['N_close3'],
             row['N_vol1'], row['N_vol2'], row['N_vol3'], row['N_rsi'], row['N_adx'], tag]
        with open('data/weekly_input_data.csv', 'a') as alphafile:
            #check for NaNs in volume, this was a bug
            if(numpy.isnan(row['N_vol3']) != True):
                writer = csv.writer(alphafile)
                writer.writerow(outputList)
#stop timer
end = time.time()
print("Processing complete")
print("{} seconds\n".format(end-start))
