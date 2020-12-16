"""
累计确诊数排名前 20 的国家名称及其数量（利用12月15日数据）
"""

import pandas as pd

df = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1], thousands=',')

# print(df.describe())
# print(df.info())
df.sort_values(by='Confirmed', inplace=True, ascending=False)  # ascending=True为升序，反之为降序
print(df)

df_res = df[0:20]

df_res.drop(df_res.columns[2:15], axis=1, inplace=True)
print(df_res)
df_res.to_csv('csvResult/累计确诊数排名前20的国家.csv', index=False)
