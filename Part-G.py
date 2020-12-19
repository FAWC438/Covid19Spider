"""
展示全球各个国家累计确诊人数的箱型图，要有平均值；
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')
plt.figure(figsize=(5, 6))
scaler = MinMaxScaler()

df = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1], thousands=',', usecols=[0, 1])

# 数据右偏，去除最大的五个异常数据
for i in range(5):
    df = df[df['Confirmed'] != df['Confirmed'].max()]

print(df)
print(df.describe())

# 归一化
# x_reshape = df["Confirmed"].values.reshape(-1, 1)
# Confirmed = scaler.fit_transform(x_reshape)  # 调用MinMaxScaler的fit_transform转换方法
# df['Fitted Confirmed'] = pd.DataFrame(Confirmed)
# print(df)

# 突出展示均值线
f = df.boxplot(column=['Confirmed'], meanline=True, showmeans=True, vert=True, notch=True,
               return_type='dict', grid=True)

for mean in f['means']:
    mean.set(color='r', linewidth=2)

# plt.text(1.1, df['Confirmed'].mean(), '{:.2e}'.format(df['Confirmed'].mean()))
# plt.text(1.1, df['Confirmed'].median(), '{:.2e}'.format(df['Confirmed'].median()))
# plt.text(0.75, df['Confirmed'].quantile(0.25), '{:.2e}'.format(df['Confirmed'].quantile(0.25)))
# plt.text(0.75, df['Confirmed'].quantile(0.75), '{:.2e}'.format(df['Confirmed'].quantile(0.75)))

plt.annotate(text='{:.2e}'.format(df['Confirmed'].mean()), xy=(1, df['Confirmed'].mean()),
             xytext=(1.1, df['Confirmed'].mean() + 5e5),
             arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3', color='purple', alpha=0.4),
             bbox=dict(boxstyle='round,pad=0.5', ec='k', lw=1, alpha=0.4))
plt.annotate(text='{:.2e}'.format(df['Confirmed'].median()), xy=(1, df['Confirmed'].median()),
             xytext=(1.1, df['Confirmed'].median() + 1e5),
             arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3', color='purple', alpha=0.4),
             bbox=dict(boxstyle='round,pad=0.5', ec='k', lw=1, alpha=0.4))
plt.annotate(text='{:.2e}'.format(df['Confirmed'].quantile(0.25)), xy=(1, df['Confirmed'].quantile(0.25)),
             xytext=(0.75, df['Confirmed'].quantile(0.25) + 1e5),
             arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3', color='purple', alpha=0.4),
             bbox=dict(boxstyle='round,pad=0.5', ec='k', lw=1, alpha=0.4))
plt.annotate(text='{:.2e}'.format(df['Confirmed'].quantile(0.75)), xy=(1, df['Confirmed'].quantile(0.75)),
             xytext=(0.75, df['Confirmed'].quantile(0.75) + 5e5),
             arrowprops=dict(arrowstyle='-|>', connectionstyle='arc3', color='purple', alpha=0.4),
             bbox=dict(boxstyle='round,pad=0.5', ec='k', lw=1, alpha=0.4))

plt.title('各个国家累计确诊人数数据的箱型图', y=1.05)
plt.tight_layout()
# plt.savefig('imgResult/全球各个国家累计确诊人数的箱型图.png')
plt.savefig('imgResult/全球各个国家累计确诊人数的箱型图（去除最大5个异常数据后）.png')
plt.show()
