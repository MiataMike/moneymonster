import csv
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import pandas as pd
import math
import time
from time import strftime
from time import gmtime

apikey = 'DONT1C40C86U80WO'
#apikey = 'HB012PXU24EQA3JL'

#setup alphavantage API
ts = TimeSeries(key=apikey,output_format='pandas', indexing_type='date')
ti = TechIndicators(key=apikey, output_format='pandas')

#normalizes daily gains w.r.t. ema
def normalizeDay(pointList, emaList, day):
    point = pointList[len(pointList)-day]
    daily_ema = emaList['EMA'][len(emaList)-day]
    return math.tanh((point-daily_ema)/daily_ema)

#similarly normalizes volume
def normalizeVol(pointList, day):
    point = pointList[len(pointList)-day]
    sma_vol = pointList.mean()
    return math.tanh((point-sma_vol)/sma_vol)

##lets normalize all data
#dayNum = 1
def normalize(dayNum):
    N_open0 = normalizeDay(daydata['1. open'],emadata,dayNum)
    N_open1 = normalizeDay(daydata['1. open'],emadata,dayNum + 1)
    N_open2 = normalizeDay(daydata['1. open'],emadata,dayNum + 2)
    N_open3 = normalizeDay(daydata['1. open'],emadata,dayNum + 3)

    N_high0 = normalizeDay(daydata['2. high'],emadata,dayNum)
    N_high1 = normalizeDay(daydata['2. high'],emadata,dayNum + 1)
    N_high2 = normalizeDay(daydata['2. high'],emadata,dayNum + 2)
    N_high3 = normalizeDay(daydata['2. high'],emadata,dayNum + 3)

    N_low0 = normalizeDay(daydata['3. low'],emadata,dayNum)
    N_low1 = normalizeDay(daydata['3. low'],emadata,dayNum + 1)
    N_low2 = normalizeDay(daydata['3. low'],emadata,dayNum + 2)
    N_low3 = normalizeDay(daydata['3. low'],emadata,dayNum + 3)

    N_close0 = normalizeDay(daydata['4. close'],emadata,dayNum)
    N_close1 = normalizeDay(daydata['4. close'],emadata,dayNum + 1)
    N_close2 = normalizeDay(daydata['4. close'],emadata,dayNum + 2)
    N_close3 = normalizeDay(daydata['4. close'],emadata,dayNum + 3)

    N_vol0 = normalizeVol(daydata['5. volume'],dayNum)
    N_vol1 = normalizeVol(daydata['5. volume'],dayNum + 1)
    N_vol2 = normalizeVol(daydata['5. volume'],dayNum + 2)
    N_vol3 = normalizeVol(daydata['5. volume'],dayNum + 3)

    N_rsi = rsidata['RSI'][len(rsidata)-dayNum]/100
    N_adx = adxdata['ADX'][len(adxdata)-dayNum]/100
    N_all = [N_open0, N_open1, N_open2,  N_high0, N_high1, N_high2,
             N_low0, N_low1, N_low2, N_close0, N_close1, N_close2,
             N_vol0, N_vol1, N_vol2, N_rsi, N_adx]
    return N_all

#setup target ticker list
sp100 = []
with open('data/constituents_csvSP100.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        sp100.append(row[0])
print(sp100)

#format data in slices ready for inferencing
for ticker in sp100:
    readabletime = strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    print('getting data for {} at {}'.format(ticker,readabletime))
    daydata, daymeta_data = ts.get_daily(symbol=ticker, outputsize='full')
    emadata, emameta_data = ti.get_ema(symbol=ticker)
    rsidata, rsimeta_data = ti.get_rsi(symbol=ticker)
    adxdata, adxmeta_data = ti.get_adx(symbol=ticker)
    with open('data/slices/{}.csv'.format(ticker), mode='w') as csvfile:
        alphaFieldnames = ['N_open1', 'N_open2', 'N_open3',  'N_high1', 'N_high2', 'N_high3',
                 'N_low1', 'N_low2', 'N_low3', 'N_close1', 'N_close2', 'N_close3',
                 'N_vol1', 'N_vol2', 'N_vol3', 'N_rsi', 'N_adx']
        pointWriter = csv.writer(csvfile)
        pointWriter.writerow(alphaFieldnames)
        pointWriter.writerow(normalize(1)) #this line just looks at the most recent day
    #print("Hold your horses cowboy")
    #wait to limit API calls to 5/min
    time.sleep(60) 
