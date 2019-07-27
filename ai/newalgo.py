import robin_stocks as r
import csv
import math
import time
from options import time_tools as tt
from options import black_scholes
import datetime

import hmac, base64, struct, hashlib, time

def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def get_totp_token(secret):
    return get_hotp_token(secret, intervals_no=int(time.time())//30)

secret = 'VX54TGA5MDA6MZZZ'
mfa_code = get_totp_token(secret)

print(mfa_code)


##read password from local file
f = open("rh-password","r")
password = f.readline()
f.close()
password = password.rstrip('\n')
r.login('mwtvy4@mst.edu',password)

def call_algo(ticker):
    stock_price = tt.curr_price(ticker)
    risk_free = .035
    percent_year = 15/260
    volatility = tt.hist_vol(ticker,60)
    weekly_volatility = volatility / math.sqrt(19)
    strike_price = stock_price * (1 + weekly_volatility)
#    print("{}/{} with {} days and {}".format(ticker, strike, percent_year,strike_price)) 
    call_price = black_scholes.call(stock_price, strike_price, risk_free, percent_year, volatility)
    breakeven = strike_price + call_price
    probability = black_scholes.prob(stock_price, breakeven, risk_free, percent_year, volatility)
    print("Report for {}".format(ticker))
    print("{0:.3g}% probability of profit".format(probability*100))
    print("stock price: {}".format(stock_price))
    print("strike price: {}".format(strike_price))
    print("target price: {}".format(breakeven))


#get the date
    monday = datetime.date.today()
    nineteenDays = datetime.timedelta(21)
    friday = monday + nineteenDays #this is the friday 3 trading days away from monday
    expiration_date = friday.isoformat()

#get the price
    prices = r.find_tradable_options_for_stock(ticker,'call',info = None)
    floats = []
    for price in prices:
        if( price['expiration_date'] == expiration_date):
            floats.append(float(price['strike_price']))
    floats.sort()
    last_strike = -1
    for test_strike in floats:
        if(test_strike < strike_price):
            last_strike = test_strike


    RH_option = r.get_option_market_data(ticker,expiration_date,last_strike,'call')

    print("RH strike price: {}".format(last_strike))
    print("{}% probability of RH profit".format(float(RH_option['chance_of_profit_long'])*100))
    print("RH option price: ${}\n".format(RH_option['adjusted_mark_price']))
    print("buy {} contracts\n".format(20/(float(RH_option['adjusted_mark_price'])*100)))
    return


def put_algo(ticker):
    stock_price = tt.curr_price(ticker)
    risk_free = .035
    percent_year = 15/260
    volatility = tt.hist_vol(ticker,60)
    weekly_volatility = volatility / math.sqrt(19)
    strike_price = stock_price * (1-weekly_volatility)
#    print("{}/{} with {} days and {}".format(ticker, strike, percent_year,strike_price)) 
    put_price = black_scholes.put(stock_price, strike_price, risk_free, percent_year, volatility)
    breakeven = strike_price - put_price
    probability = 1 - black_scholes.prob(stock_price, breakeven, risk_free, percent_year, volatility)
    print("Report for {}".format(ticker))
    print("{0:.3g}% probability of profit".format(probability*100))
    print("stock price: {}".format(stock_price))
    print("strike price: {}".format(strike_price))
    print("target price: {}".format(breakeven))

#get the date
    monday = datetime.date.today()
    nineteenDays = datetime.timedelta(21)
    friday = monday + nineteenDays #this is the friday 3 trading days away from monday
    expiration_date = friday.isoformat()

#get the price
    prices = r.find_tradable_options_for_stock(ticker,'put',info = None)
    floats = []
    for price in prices:
        if( price['expiration_date'] == expiration_date):
            floats.append(float(price['strike_price']))
    floats.sort()
    last_strike = -1
    for test_strike in floats:
        if(test_strike < strike_price):
            last_strike = test_strike


    RH_option = r.get_option_market_data(ticker,expiration_date,last_strike,'put')

    print("RH strike price: {}".format(last_strike))
    print("{}% probability of RH profit".format(float(RH_option['chance_of_profit_long'])*100))
    print("RH option price: ${}\n".format(RH_option['adjusted_mark_price']))
    print("buy {} contracts\n".format(20/(float(RH_option['adjusted_mark_price'])*100)))
    return


top5 = []
with open('data/top5.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        top5.append(row[0])
for ticker in top5:
    call_algo(ticker)
    time.sleep(30)

bottom5 = []
with open('data/bottom5.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        bottom5.append(row[0])
for ticker in bottom5:
    put_algo(ticker)
    time.sleep(30)


