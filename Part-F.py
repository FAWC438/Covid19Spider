"""
用饼图展示各个国家的累计确诊人数的比例（你爬取的所有国家，数据较小的国家 可以合并处理）；
"""
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['savefig.dpi'] = 300  # 图片像素
plt.rcParams['figure.dpi'] = 300  # 分辨率
plt.style.use('Solarize_Light2')

df = pd.read_csv('csvFile/Covid19Data2020-12-15.csv', encoding='utf-8', skiprows=[1], thousands=',', usecols=[0, 1])
df.sort_values(by='Confirmed', inplace=True, ascending=False)
df = df.reset_index(drop=True)  # 重置索引
# print(df)
# print(df.info())
# print(df.head(20))

# 展示确诊人数大于一百万的国家，其它国家归为其它
df_show = df[df['Confirmed'] > 1000000]
df_other = df[df['Confirmed'] < 1000000]
new = pd.DataFrame({'Name': 'Others', 'Confirmed': df_other['Confirmed'].sum()}, index=[1])
df_show = df_show.append(new, ignore_index=True)
print(df_show)

patches, l_text, p_text = plt.pie(df_show['Confirmed'], startangle=300, labels=df_show['Name'],
                                  autopct='%1.2f%%', labeldistance=1.1, textprops={'fontsize': 10, 'color': 'black'})
plt.title('世界219个国家的累计确诊人数比例图', y=1.05)
plt.axis('equal')
# 图例
plt.legend(loc='upper right', fontsize=7)

plt.tight_layout()
plt.savefig('imgResult/世界219个国家的累计确诊人数比例图.png')
plt.show()
df_show.to_csv('csvResult/世界219个国家的累计确诊人数展示数据.csv', index=False)
