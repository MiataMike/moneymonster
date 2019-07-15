import csv
import math
import time
from options import time_tools as tt
from options import black_scholes
#get current price
def put_algo(ticker):
    stock_price = tt.curr_price(ticker)
    risk_free = .035
    percent_year = 15/260
    volatility = tt.hist_vol(ticker,60)
    weekly_volatility = volatility / math.sqrt(50)
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
    print("buy {} contracts\n".format(10/put_price))
    return

def call_algo(ticker):
    stock_price = tt.curr_price(ticker)
    risk_free = .035
    percent_year = 15/260
    volatility = tt.hist_vol(ticker,60)
    weekly_volatility = volatility / math.sqrt(50)
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
    print("buy {} contracts\n".format(10/call_price))
    return

#ouptut price 1 std dev down

#portfolio = ['TSLA', 'DIS', 'SBUX', 'F', 'BABA', 'GE', 'SNAP', 'T', 'DIA', 'VTI', 'LUV', 'XOM', 'CVS', 'AUY', 'GSK']
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

