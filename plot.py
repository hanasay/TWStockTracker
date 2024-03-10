### Common
import datetime,time
import pandas as pd
import numpy as np

### For Image Drawing
from matplotlib import pyplot as plt
from matplotlib.widgets import MultiCursor
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoLocator, MultipleLocator

### TW-Stock info API
import twstock

### Technical Indicators
from talib import abstract

def Plot_stock(**kwargs):
    ### Changeable variable
    sid = kwargs['sid']
    mode = kwargs['mode']
    
    ### Get the name of stock
    stock_name = twstock.realtime.get(sid)['info']['name']

    ### Get Stock From Specific time to 'today'
    stock = twstock.Stock(sid)
    target = stock.fetch_from(2023,7)

    ### Setting Font To Chinese-Tradition
    font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=14)

    ### Column Name of Stock Data
    name_attribute = ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction']

    # Change into Pandas
    stock_data = pd.DataFrame(columns = name_attribute, data = target)

    ### Matplotlib Initialize
    fig = plt.figure(figsize=(15, 6))
    ax1 = plt.subplot(2, 1, 1)
    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    fig.suptitle(f'{sid} {stock_name}', fontproperties=font)
    plt.xlabel('日期', fontproperties=font)
    plt.ylabel('數值', fontproperties=font)

    ### Stock Close Price plot
    ax1.plot(stock_data['date'], stock_data['close'], label = '收盤價', color='r')

    match mode:
        case "MA":
            ### Stock MA plot
            stock_data_ma = abstract.MA(stock_data, kwargs['MA'])
            ax2.plot(stock_data['date'], stock_data_ma, label = f'RSI {kwargs[mode]}')
        case "MACD":
            ### Stock MACD plot
            stock_data_macd = abstract.MACD(stock_data, fastperiod=kwargs['MACD_fast'], slowperiod=kwargs['MACD_slow'], signalperiod=kwargs['MACD_signal'])
            ax2.plot(stock_data['date'], stock_data_macd['macd'], label = f'MACD')
            ax2.plot(stock_data['date'], stock_data_macd['macdsignal'], label = f'Signal')
            ax2.plot(stock_data['date'], stock_data_macd['macdhist'], label = f'HIST')
        case "KD":
            ### Stock KD plot
            stock_data_kd = abstract.STOCH(stock_data, fastk_period=kwargs['KD_fastk'], slowk_period=kwargs['KD_slowk'], slowd_period=kwargs['KD_slowd'])
            ax2.plot(stock_data['date'], stock_data_kd['slowk'], label = f'Slow K')
            ax2.plot(stock_data['date'], stock_data_kd['slowd'], label = f'Slow D')
        case "RSI":
            ### Stock RSI plot
            stock_data_RSI = abstract.RSI(stock_data, kwargs['RSI'])
            ax2.plot(stock_data['date'], stock_data_RSI, label = f'RSI {kwargs[mode]}')

    ax1.legend(loc='upper left', shadow=True, prop=font, bbox_to_anchor=(1, 0.5))
    ax2.legend(loc='upper left', shadow=True, prop=font, bbox_to_anchor=(1, 0.5))

    ### Crosshair on image
    cursor = MultiCursor(fig.canvas, (ax1, ax2), color='r',lw=0.5, horizOn=True, vertOn=True)

    ### Set axis data type
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().yaxis.set_major_locator(MultipleLocator(10))
    plt.gcf().autofmt_xdate()

    plt.show()