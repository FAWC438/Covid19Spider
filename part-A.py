"""
15 天中，全球新冠疫情的总体变化趋势
"""

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

df = DataFrame()

for i in range(1, 16):
    if i >= 10:
        str_num = str(i)
    else:
        str_num = '0' + str(i)
    df[str(i)] = \
        pd.read_csv('csvFile/Covid19Data2020-12-' + str_num + '.csv',
                    encoding='utf-8', thousands=',', nrows=1).loc[0]  # 只读第一行的全球数据，并且去除千分位的逗号

print(df)
print(df.at['Confirmed', '1'])
print(df.loc['Confirmed'].to_list())
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))  # nrows=2, ncols=2 figsize=(13, 13)

day_list = list(range(1, 16))
# 1.展示全球新冠疫情总确认数量变化
Confirmed_list = df.loc['Confirmed'].to_list()
ax[0, 0].plot(day_list, Confirmed_list, linewidth=2.0, marker='o')
ax[0, 0].text(day_list[0] - 1.5, Confirmed_list[0] + 3e5, '{:.2e}'.format(Confirmed_list[0]), color='r', size=13,
              weight='bold')
ax[0, 0].text(day_list[-1] - 1.5, Confirmed_list[-1] + 3e5, '{:.2e}'.format(Confirmed_list[-1]), color='r', size=13,
              weight='bold')
ax[0, 0].set_xticks(day_list)
ax[0, 0].set_xlabel('日期')
ax[0, 0].set_ylabel('确诊人数')
ax[0, 0].set_title('12月1日至15日全球新冠累计确诊人数变化', y=1.1, size=13)
# 2.展示全球新冠疫情增长速度变化
Confirmed_Percentage_list = df.loc['Confirmed Percentage Day Change'].to_list()
Confirmed_Percentage_list = [float(i[:-1]) for i in Confirmed_Percentage_list]
ax[0, 1].plot(day_list, Confirmed_Percentage_list, linewidth=2.0, marker='o')
ax[0, 1].set_xticks(day_list)
ax[0, 1].set_xlabel('日期')
ax[0, 1].set_yticks([0.10, 0.15, 0.20, 0.25, 0.30, 0.35])
ax[0, 1].set_yticklabels(['0.10%', '0.15%', '0.20%', '0.25%', '0.30%', '0.35%'])
ax[0, 1].set_ylabel('确诊人数日增长率')
ax[0, 1].set_title('12月1日至15日全球新冠总确诊人数增长率', y=1.1, size=13)
# 3.展示现存确诊人数
Active_list = df.loc['Active'].to_list()
ax[0, 2].plot(day_list, Active_list, linewidth=2.0, marker='o')
ax[0, 2].text(day_list[0] - 1.5, Active_list[0] + 8e4, '{:.2e}'.format(Active_list[0]), color='r', size=13,
              weight='bold')
ax[0, 2].text(day_list[-1] - 1.5, Active_list[-1] + 8e4, '{:.2e}'.format(Active_list[-1]), color='r', size=13,
              weight='bold')
ax[0, 2].set_xticks(day_list)
ax[0, 2].set_xlabel('日期')
ax[0, 2].set_ylabel('现存确诊人数')
ax[0, 2].set_title('12月1日至15日全球新冠现存确诊人数净变化', y=1.1, size=13)
# 4.展示全球新冠疫情死亡人数变化
Deceased_list = df.loc['Deceased'].to_list()
ax[1, 0].plot(day_list, Deceased_list, linewidth=2.0, marker='o')
ax[1, 0].text(day_list[0] - 1.5, Deceased_list[0] + 6e3, '{:.2e}'.format(Deceased_list[0]), color='r', size=13,
              weight='bold')
ax[1, 0].text(day_list[-1] - 1.5, Deceased_list[-1] + 6e3, '{:.2e}'.format(Deceased_list[-1]), color='r', size=13,
              weight='bold')
ax[1, 0].set_xticks(day_list)
ax[1, 0].set_xlabel('日期')
ax[1, 0].set_ylabel('死亡人数')
ax[1, 0].set_title('12月1日至15日全球新冠死亡人数变化', y=1.1, size=13)
# 5.展示全球新冠疫情康复人数变化
Recovered_list = df.loc['Recovered'].to_list()
ax[1, 1].plot(day_list, Recovered_list, linewidth=2.0, marker='o')
ax[1, 1].text(day_list[0] - 1.5, Recovered_list[0] + 3e5, '{:.2e}'.format(Recovered_list[0]), color='r', size=13,
              weight='bold')
ax[1, 1].text(day_list[-1] - 1.5, Recovered_list[-1] + 3e5, '{:.2e}'.format(Recovered_list[-1]), color='r', size=13,
              weight='bold')
ax[1, 1].set_xticks(day_list)
ax[1, 1].set_xlabel('日期')
ax[1, 1].set_ylabel('康复人数')
ax[1, 1].set_title('12月1日至15日全球新冠康复人数变化', y=1.1, size=13)
# 5.展示全球新冠疫情检测人数变化
Tests_list = df.loc['Tests'].to_list()
ax[1, 2].plot(day_list, Tests_list, linewidth=2.0, marker='o')
ax[1, 2].text(day_list[0] - 1.5, Tests_list[0] + 3e6, '{:.2e}'.format(Tests_list[0]), color='r', size=13,
              weight='bold')
ax[1, 2].text(day_list[-1] - 1.5, Tests_list[-1] + 3e6, '{:.2e}'.format(Tests_list[-1]), color='r', size=13,
              weight='bold')
ax[1, 2].set_xticks(day_list)
ax[1, 2].set_xlabel('日期')
ax[1, 2].set_ylabel('检测人数')
ax[1, 2].set_title('12月1日至15日全球新冠检测人数变化', y=1.1, size=13)

plt.tight_layout()
plt.subplots_adjust()
plt.savefig('imgResult/总体变化趋势.png')
plt.show()
