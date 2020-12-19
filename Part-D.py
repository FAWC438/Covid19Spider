"""
累计确诊人数占国家总人口比例最高的 10 个国家；
人口数量和累计确诊人数采用12月15日的数据
"""
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

df = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1], thousands=',', usecols=[0, 1, 14])

df['Confirmed rate'] = df['Confirmed'] / df['Population']
print(df)
df.sort_values(by='Confirmed rate', inplace=True, ascending=False)

# 取出累计确诊人数占国家总人口比例最高的 10 个国家
df_res = df[0:10]
df_res = df_res.reset_index(drop=True)  # 重置索引
print(df_res)

plt.bar(list(range(0, 50, 5)), df_res['Confirmed rate'].to_list(), width=2, alpha=0.5, color='r')
plt.xticks(list(range(0, 50, 5)), labels=df_res['Name'].to_list(), rotation=35)
plt.yticks([0.00, 0.02, 0.04, 0.06, 0.08, 0.10], ['0', '2%', '4%', '6%', '8%', '10%'])
plt.tick_params(labelsize=11)
for a, b in zip(list(range(0, 50, 5)), df_res['Confirmed rate'].to_list()):  # 在直方图上显示数字
    plt.text(a, b + 0.000001, '%.2f%%' % (b * 100), ha='center', va='bottom', fontsize=10, color='black')
plt.title('累计确诊人数占国家总人口比例最高的 10 个国家')
plt.xlabel("国家")
plt.ylabel("确诊比例")

plt.tight_layout()
plt.savefig('imgResult/累计确诊人数占国家总人口比例最高的10个国家.png')
plt.show()
df_res.to_csv('csvResult/累计确诊人数占国家总人口比例最高的10个国家.csv', index=False)
