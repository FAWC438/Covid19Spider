"""
针对全球累计确诊数，利用前 10 天采集到的数据做后 5 天的预测，并与实际数据进行 对比。说明你预测的方法，并分析与实际数据的差距和原因。
"""
from math import sqrt

import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.holtwinters import Holt

scaler = MinMaxScaler()

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

df = pd.read_csv('csvFile/Covid19Data2020-12-01.csv', encoding='utf-8', thousands=',', nrows=1, usecols=[0, 1])
# 均方根误差
df_error = pd.DataFrame({'Method': ['Holt', 'ARIMA', 'Roll-2', 'Roll-3', 'Roll-4'], 'Value': [0, 0, 0, 0, 0]})
print(df_error)
# 只读取全球总体数据
for i in range(2, 16):
    if i >= 10:
        str_num = str(i)
    else:
        str_num = '0' + str(i)
    df_temp = pd.read_csv('csvFile/Covid19Data2020-12-' + str_num + '.csv',
                          encoding='utf-8', thousands=',', nrows=1, usecols=[0, 1])
    df.loc[i - 1] = df_temp.loc[0]
# 数据归一化后计算均方误差时将出现精度问题，故不予考虑
# # 将Confirmed列归一化
# x_reshape = df["Confirmed"].values.reshape(-1, 1)
# df["Confirmed"] = scaler.fit_transform(x_reshape)  # 调用MinMaxScaler的fit_transform转换方法
print(df)

fig, ax = plt.subplots()

# 1.原始数据
ax.plot(np.arange(5), df.loc[10:14, 'Confirmed'], marker='o')

# 2.霍尔特(Holt)线性趋势法
df.loc[0:9, 'Holt_linear'] = df.loc[0:9, 'Confirmed']
fit = Holt(np.asarray(df.loc[0:9, 'Confirmed'])).fit(smoothing_level=1, smoothing_trend=0.2)
df.loc[10:14, 'Holt_linear'] = fit.forecast(5)
ax.plot(np.arange(5), df.loc[10:14, 'Holt_linear'], marker='o')
df_error.at[0, 'Value'] = sqrt(mean_squared_error(df.loc[10:14, 'Confirmed'], df.loc[10:14, 'Holt_linear']))

# 3.自回归移动平均模型（ARIMA）
df.loc[0:9, 'ARIMA'] = df.loc[0:9, 'Confirmed']
fit1 = sm.tsa.statespace.SARIMAX(df.loc[0:9, 'Confirmed'], order=(2, 1, 7)).fit()
df.loc[10:14, 'ARIMA'] = fit1.predict(start=10, end=14, dynamic=True)
ax.plot(np.arange(5), df.loc[10:14, 'ARIMA'], marker='o')
df_error.at[1, 'Value'] = sqrt(mean_squared_error(df.loc[10:14, 'Confirmed'], df.loc[10:14, 'ARIMA']))

# 4.生成滑动窗口为2的预测值
df['Roll_2'] = df['Confirmed'].rolling(window=2, center=False).mean()
ax.plot(np.arange(5), df.loc[10:14, 'Roll_2'], marker='o')
df_error.at[2, 'Value'] = sqrt(mean_squared_error(df.loc[10:14, 'Confirmed'], df.loc[10:14, 'Roll_2']))

# 5.生成滑动窗口为3的预测值
df['Roll_3'] = df['Confirmed'].rolling(window=3, center=False).mean()
ax.plot(np.arange(5), df.loc[10:14, 'Roll_3'], marker='o')
df_error.at[3, 'Value'] = sqrt(mean_squared_error(df.loc[10:14, 'Confirmed'], df.loc[10:14, 'Roll_3']))

# 6.生成滑动窗口为4的预测值
df['Roll_4'] = df['Confirmed'].rolling(window=4, center=False).mean()
ax.plot(np.arange(5), df.loc[10:14, 'Roll_4'], marker='o')
df_error.at[4, 'Value'] = sqrt(mean_squared_error(df.loc[10:14, 'Confirmed'], df.loc[10:14, 'Roll_4']))

ax.legend(['Original', 'Holt', 'ARIMA', 'Roll-2', 'Roll-3', 'Roll-4'])
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_xticklabels(['11日', '12日', '13日', '14日', '15日'])
ax.set_xlabel('日期')
ax.set_ylabel('全球确诊人数')
ax.set_title('12月11日至15日全球确诊人数预测')

df.to_csv('csvResult/预测分析.csv', index=False)
df_error.to_csv('csvResult/预测误差.csv', index=False)

plt.savefig('imgResult/12月11日至15日全球确诊人数预测.png')
plt.show()
