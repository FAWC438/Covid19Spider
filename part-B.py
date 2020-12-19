"""
累计确诊数排名前 20 的国家名称及其数量（利用12月15日数据）
"""

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

df = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1], thousands=',')

# print(df.describe())
# print(df.info())
df.sort_values(by='Confirmed', inplace=True, ascending=False)  # ascending=True为升序，反之为降序
print(df)

df_res = df[0:20]

df_res.drop(df_res.columns[2:15], axis=1, inplace=True)
print(df_res)

plt.bar(list(range(0, 100, 5)), df_res['Confirmed'].to_list(), width=3, alpha=0.5, color='b')
plt.xticks(list(range(0, 100, 5)), labels=df_res['Name'].to_list(), rotation=35)
plt.tick_params(labelsize=6)
for a, b in zip(list(range(0, 100, 5)), df_res['Confirmed'].to_list()):  # 在直方图上显示数字
    plt.text(a, b + 1e5, '%.2e' % b, ha='center', va='bottom', fontsize=4, color='black')
plt.title('累计确诊数排名前20的国家')
plt.xlabel("国家")
plt.ylabel("人数")

plt.tight_layout()
plt.savefig('imgResult/累计确诊数排名前20的国家.png')
plt.show()
df_res.to_csv('csvResult/累计确诊数排名前20的国家.csv', index=False)
