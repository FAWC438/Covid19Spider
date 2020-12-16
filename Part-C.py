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

df = DataFrame()
df['Name'] = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1])['Name']
for i in range(1, 16):
    if i >= 10:
        str_num = str(i)
    else:
        str_num = '0' + str(i)
    df[i] = \
        pd.read_csv('csvFile/Covid19Data2020-12-' + str_num + '.csv',
                    encoding='utf-8', thousands=',', skiprows=[1])['Confirmed Changes Today']
df["Sum"] = df[df.columns[1:]].sum(axis=1)
df.sort_values(by='Sum', inplace=True, ascending=False)
# print(df)

df_res = df[0:10]
df_res = df_res.reset_index(drop=True)  # 重置索引

df_res.replace(0, np.nan, inplace=True)
# print(df_res)
# print(df_res.drop(['Name', 'Sum'], axis=1))
df_temp = df_res.drop(['Name', 'Sum'], axis=1).interpolate(axis=1)

# print(df_temp)
index = 0
# 将第一列线性插值无法处理的Nan替换为邻近值
for i in df_temp[1]:  # 遍历某列所有行
    if np.isnan(i):
        df_temp.at[index, 1] = df_temp.at[index, 2]
    index += 1
df_res[df_res.columns[1:-1]] = df_temp
df_res["Sum_interpolated"] = df_res[df_res.columns[1:-1]].sum(axis=1)
print(df_res)

df_res.to_csv('csvResult/每日新增确诊数累计排名前10的国家.csv', index=False)

fig, ax = plt.subplots()
day_list = list(range(1, 16))
for i in range(10):
    ax.plot(day_list, df_temp.loc[i].to_list())
ax.set_xlabel('日期')
ax.set_ylabel('新增确诊人数')
ax.set_title('12月1日至15日每日新增确诊数累计排名前 10 的国家', size=13)
plt.legend(df_res['Name'].to_list(), loc='best')
plt.tight_layout()
plt.show()
