"""
15 天中，每日新增确诊数累计排名前 10 个国家的每日新增确诊数据的曲线图；
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

countries = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1])['Name'].to_list()
df = DataFrame(
    columns=countries)

# 只读取每日确诊数据
for i in range(1, 16):
    if i >= 10:
        str_num = str(i)
    else:
        str_num = '0' + str(i)
    df_temp = pd.read_csv('csvFile/Covid19Data2020-12-' + str_num + '.csv',
                          encoding='utf-8', thousands=',', skiprows=[1], usecols=[0, 1])
    for tup in df_temp.itertuples():
        df.at[i, tup[1]] = tup[2]

df.to_csv('csvResult/所有国家15日确诊人数.csv', index=False)
for i in range(2, 16).__reversed__():
    df.loc[i] -= df.loc[i - 1]
    df.loc[str(i) + ' rate'] = df.loc[i] / df.loc[i - 1]
df = df.T
df['Name'] = np.array(countries)
df['Sum'] = df[df.columns[1:15]].sum(axis=1)
df['Rate Sum'] = df[df.columns[15:29]].mean(axis=1)
df.to_csv('csvResult/所有国家的新增确诊数数据日变化.csv', index=False)
df.sort_values(by='Sum', inplace=True, ascending=False)
df.reset_index(drop=True)

# 作图
# 取出累计确诊最多的10个国家
df_res = df[0:10]
fig, ax = plt.subplots()
day_list = list(range(2, 16))
for i in df_res.index.to_list():
    s = df_res.loc[i]
    ax.plot(day_list, s[[j for j in day_list]])  # 每个国家一条折线
ax.set_xticks(day_list)
ax.set_xlabel('日期')
ax.set_ylabel('新增确诊人数')
ax.set_title('12月1日至15日每日新增确诊数累计排名前 10 的国家', size=13)
plt.legend(df_res['Name'].to_list(), loc='best')  # 图例
plt.tight_layout()
plt.savefig('imgResult/新增确诊数最高的10个国家.png')
plt.show()
