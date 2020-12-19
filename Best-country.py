"""
列出全世界应对新冠疫情最好的 10 个国家
鉴于各个国家人口、医疗水平、检测人数等客观条件不同，故判断应对新冠疫情是否成功的关键因素及其权值如下：

1. 累计确诊人数占国家总人口比例，权值：0.25
2. 死亡率(死亡人数/确诊人数)，权值：0.3
3. 康复率(康复人数/确诊人数)，权值：0.3
4. 15日内确诊人数日增长率((今日确诊人数-昨日确诊总人数)/昨日确诊总人数)平均值，权值：0.15

权值如此设置是因为在本模型中，新冠肺炎疫情对人的生命健康的影响是首要考虑因素，存活率和康复率是应对疫情是否成功的最关键指标。

累计确诊人数是第二重要的因素，因为这表明了某个国家疫情的规模，体现了该国家疫情的严重程度

日增长速率表明了新冠肺炎疫情在某个国家的肆虐速度，一定程度上能体现疫情在该国家的严重程度。
但是，应当考虑部分国家由于应对措施得当导致潜在感染者被大量发现的情况，因此该指标的权值最小
"""

import numpy as np
import pandas as pd

df = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1], thousands=',')

df['Confirmed rate'] = df['Confirmed'] / df['Population']
df['Deceased rate'] = df['Deceased'] / df['Confirmed']
df['Recovered rate'] = df['Recovered'] / df['Confirmed']
df['Increase rate'] = pd.read_csv('csvResult/所有国家的新增确诊数数据日变化.csv', encoding='utf-8', usecols=[31])
print(df)

# 有空数据的国家不予考虑
df.drop(df[np.isnan(df['Confirmed rate'])].index, inplace=True)
df.drop(df[np.isnan(df['Deceased rate'])].index, inplace=True)
df.drop(df[np.isnan(df['Recovered rate'])].index, inplace=True)
df.drop(df[np.isnan(df['Increase rate'])].index, inplace=True)

# 判决值计算公式:
# (1-确诊率)*0.25+(1-死亡率)*0.3+康复率*0.3+(1-增长率)*0.15
df['Judgement Value'] = (1 - df['Confirmed rate']) * 0.25 + (1 - df['Deceased rate']) * 0.3 + df[
    'Recovered rate'] * 0.3 + (1 - df['Increase rate']) * 0.15

df.drop(labels=df.columns[1:15], axis=1, inplace=True)
df.sort_values(by='Judgement Value', inplace=True, ascending=False)

df.to_csv('csvResult/总体分析.csv', index=False)
