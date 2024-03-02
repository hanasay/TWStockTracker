import datetime,time
import twstock
from talib import abstract
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import AutoLocator, MultipleLocator

sid = '2356'
stock_name = twstock.realtime.get(sid)['info']['name']

stock = twstock.Stock(sid)
target = stock.fetch_from(2023,7)

font = FontProperties(fname=r'C:\Windows\Fonts\msjh.ttc', size=14)

name_attribute = ['date', 'capacity', 'turnover', 'open', 'high', 'low', 'close', 'change', 'transaction']

#day = datetime.datetime.now()
#day = day.strftime("%Y-%m-%d")

df = pd.DataFrame(columns = name_attribute, data = target)

rsi_day = 14

df_kd = abstract.STOCH(df, fastk_period=9, slowk_period=3, slowd_period=3)
df_rsi = abstract.RSI(df, rsi_day)
#print(df_rsi)
#df_rsi.plot(figsize=(16,8))
plt.title(f'{sid} {stock_name}', fontproperties=font)
plt.xlabel('日期', fontproperties=font)
plt.ylabel('數值', fontproperties=font)
plt.plot(df['date'], df['close'], label = '收盤價')
plt.plot(df['date'], df_rsi, label = f'RSI {rsi_day}Day')
#plt.plot(df['date'], df_kd['slowk'], label = f'Slow K')
#plt.plot(df['date'], df_kd['slowd'], label = f'Slow D')

plt.legend(loc='upper left', shadow=True, prop=font)
cursor = Cursor(plt.gca(), horizOn=True, vertOn=True, color='red', linewidth=1.0)
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
plt.gca().yaxis.set_major_locator(MultipleLocator(10))
plt.gcf().autofmt_xdate()

plt.show()