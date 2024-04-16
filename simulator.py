### Common
import math
import calendar
import pandas as pd

### TW-Stock info API
import twstock

### Technical Indicators
from talib import abstract

def setup(**kwargs):
    ### The Bank money we got
    fund = float(kwargs['fund'])

    ### Changeable variable
    sid = kwargs['sid']
    
    ### Get the name of stock
    stock_name = twstock.realtime.get(sid)['info']['name']
    print(f'Current Simulating {stock_name} {sid}')

    ### Get Stock From Specific time to 'today'
    stock = twstock.Stock(sid)
    target_time = kwargs['date']
    target = stock.fetch_from(target_time.year, target_time.month-1) if target_time.month > 1 else calendar.monthrange(target_time.year-1, 12)
    number_of_days = calendar.monthrange(target_time.year, target_time.month-1) if target_time.month > 1 else calendar.monthrange(target_time.year-1, 12)
    number_of_days = number_of_days[1]
    target_day = target_time.day

    ### Column Name of Stock Data
    name_attribute = ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction']

    # Change into Pandas
    stock_data = pd.DataFrame(columns = name_attribute, data = target)
    
    ### MACD
    stock_data_macd = abstract.MACD(stock_data, fastperiod=9, slowperiod=3, signalperiod=3)

    ### RSI
    stock_data_RSI1 = abstract.RSI(stock_data, 5)
    stock_data_RSI2 = abstract.RSI(stock_data, 10)
    
    high_macd = -100
    state = 'sell'
    keeping_stock = 0
    last_close = 0

    for date, close, macd, rsi1, rsi2 in zip(stock_data['date'],stock_data['close'],stock_data_macd['macd'], stock_data_RSI1, stock_data_RSI2):
        ### get All Technical Indicators and skip those we don't need
        if math.isnan(macd) or math.isnan(rsi1) or math.isnan(rsi2): continue

        ### Debug part
        print(f'\n現在日期: {date}')
        print(f'收盤價: {close} macd: {macd} rsi5日: {rsi1} rsi10日: {rsi2}\n')
        last_close = close
        if macd > high_macd and macd > 0: high_macd = macd

        if state == 'sell':
            if macd < 0 and abs(macd + 0.5) >= high_macd:
                state = 'buy'
                buy_able = fund//close
                keeping_stock += buy_able
                fund -= buy_able * close
                print(f'正在購入 {buy_able}股，購入後剩餘{round(fund,4)}')
        
        elif state == 'buy':
            if rsi1 <= rsi2:
                state = 'sell'
                print(f'正在賣出 {keeping_stock}股',end='')
                fund += keeping_stock * close
                keeping_stock = 0
                print(f'購入後資金為: {round(fund,4)}')
                high_macd = -100
    fund += keeping_stock * last_close
    print(f'最終資金為: {round(fund,4)}')
    return