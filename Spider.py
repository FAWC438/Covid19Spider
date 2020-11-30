import csv
import time
import requests
from bs4 import BeautifulSoup

url = 'https://ncov2019.live/'

header = {
    'content-type': 'text/html;charset=UTF-8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41',
}

data = {'Name': '', 'Confirmed': '', 'Confirmed Per Million': '', 'Confirmed Changes Today': '',
        'Confirmed Percentage Day Change': '', 'Critical': '', 'Deceased': '', 'Deceased Per Million': '',
        'Deceased Changes Today': '', 'Death Percentage Day Change': '', 'Tests': '', 'Active': '', 'Recovered': '',
        'Recovered Per Million': '', 'Population': ''}

csv_file = open('csvFile/Covid19Data' + time.strftime("%Y-%m-%d") + '.csv', "w", newline='', encoding="utf_8_sig")
csv_writer = csv.DictWriter(csv_file,
                            fieldnames=data.keys())
csv_writer.writeheader()

r = requests.get(url=url, headers=header)
# 保存html文件
with open('htmlFile/page' + time.strftime("%Y-%m-%d-%H-%M") + '.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
soup = BeautifulSoup(r.text, 'html5lib')
items = soup.find('table', id='sortable_table_world').find('tbody').find_all('tr')

for item in items:
    index = 0
    for key in data.keys():
        s = item.select('td')[index].text
        if '★' in s:
            s = ' '.join(s.split()[1:])
        s = s.strip()
        if s == 'Unknown':
            s = 'NA'
        data[key] = s
        index += 1
    csv_writer.writerow(data)
    print(data['Name'])

csv_file.close()
