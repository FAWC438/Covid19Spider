"""
康复率(康复人数/确诊人数)最高的 10 个国家；
"""
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

df = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1], thousands=',', usecols=[0, 1, 12])

df['Recovered rate'] = df['Recovered'] / df['Confirmed']
print(df)
df.sort_values(by='Recovered rate', inplace=True, ascending=False)

# 取出死亡率最低的 10 个国家
df_res = df[0:10]
df_res = df_res.reset_index(drop=True)  # 重置索引
print(df_res)

plt.bar(list(range(0, 50, 5)), df_res['Recovered rate'].to_list(), width=2, alpha=0.5, color='orange')
plt.xticks(list(range(0, 50, 5)), labels=df_res['Name'].to_list(), rotation=35)
plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], ['0', '0.2%', '0.4%', '0.6%', '0.8%', '1.0%'])
plt.tick_params(labelsize=9)
for a, b in zip(list(range(0, 50, 5)), df_res['Recovered rate'].to_list()):  # 在直方图上显示数字
    plt.text(a, b + 0.008, '%.2f%%' % (b * 100), ha='center', va='bottom', fontsize=9, color='black')
plt.title('康复率最高的 10 个国家')
plt.xlabel("国家")
plt.ylabel("康复率")

plt.tight_layout()
plt.savefig('imgResult/康复率最高的10个国家.png')
plt.show()
df_res.to_csv('csvResult/康复率最高的10个国家.csv', index=False)
