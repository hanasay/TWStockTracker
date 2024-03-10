### Common
import datetime,time
import pandas as pd
import numpy as np

### For Image Drawing
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoLocator, MultipleLocator

### TW-Stock info API
import twstock

### Technical Indicators
from talib import abstract

def Plot_stock(stock_id: str, RSI_day):
    ### Changeable variable
    sid = stock_id
    rsi_day = RSI_day
    
    ### Get the name of stock
    stock_name = twstock.realtime.get(sid)['info']['name']

    ### Get Stock From Specific time to 'today'
    stock = twstock.Stock(sid)
    target = stock.fetch_from(2023,7)

    ### Setting Chinese-Tradition font
    font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=14)

    ### Column name of Stock data
    name_attribute = ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction']

    df = pd.DataFrame(columns = name_attribute, data = target)

    df_kd = abstract.STOCH(df, fastk_period=9, slowk_period=3, slowd_period=3)
    df_rsi = abstract.RSI(df, rsi_day)

    plt.title(f'{sid} {stock_name}', fontproperties=font)
    plt.xlabel('日期', fontproperties=font)
    plt.ylabel('數值', fontproperties=font)

    ### Stock Close Price plot
    plt.plot(df['date'], df['close'], label = '收盤價')

    ### Stock RSI plot
    plt.plot(df['date'], df_rsi, label = f'RSI {rsi_day}Day')

    ### Stock KD plot
    #plt.plot(df['date'], df_kd['slowk'], label = f'Slow K')
    #plt.plot(df['date'], df_kd['slowd'], label = f'Slow D')

    plt.legend(loc='upper left', shadow=True, prop=font)

    ### Crosshair on image
    cursor = Cursor(plt.gca(), horizOn=True, vertOn=True, color='red', linewidth=1.0)

    ### Set axis data type
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().yaxis.set_major_locator(MultipleLocator(10))
    plt.gcf().autofmt_xdate()

    plt.show()