import csv
import time

import requests
from bs4 import BeautifulSoup

url = 'https://ncov2019.live/'

header = {
    'content-type': 'text/html;charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41',
}

# 数据种类
data = {'Name': '', 'Confirmed': '', 'Confirmed Per Million': '', 'Confirmed Changes Today': '',
        'Confirmed Percentage Day Change': '', 'Critical': '', 'Deceased': '', 'Deceased Per Million': '',
        'Deceased Changes Today': '', 'Death Percentage Day Change': '', 'Tests': '', 'Active': '', 'Recovered': '',
        'Recovered Per Million': '', 'Population': ''}

# 配置输出的csv文件
csv_file = open('csvFile/Covid19Data' + time.strftime("%Y-%m-%d") + '.csv', "w", newline='', encoding="utf_8_sig")
csv_writer = csv.DictWriter(csv_file,
                            fieldnames=data.keys())
csv_writer.writeheader()

# 发送get请求，得到html页面
r = requests.get(url=url, headers=header)
# 保存html文件以防数据丢失或错误
with open('htmlFile/page' + time.strftime("%Y-%m-%d-%H-%M") + '.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
soup = BeautifulSoup(r.text, 'html5lib')
items = soup.find('table', id='sortable_table_world').find('tbody').find_all('tr')

for item in items:
    index = 0
    # 获得各种数据
    for key in data.keys():
        s = item.select('td')[index].text
        # 处理特殊字符
        if '★' in s:
            s = ' '.join(s.split()[1:])
        s = s.strip()
        # 处理空数据
        if s == 'Unknown':
            s = 'NA'
        # 处理人口不足百万的国家
        if s == '0' and (
                key == 'Confirmed Per Million' or key == 'Deceased Per Million' or key == 'Recovered Per Million'):
            s = 'NA'
        data[key] = s
        index += 1
    csv_writer.writerow(data)
    print(data['Name'])

csv_file.close()
