import csv

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

def getCity():
    gd=['广州','深圳','珠海','汕头','韶关','佛山','江门','湛江','茂名','肇庆','惠州','梅州','汕尾','河源','阳江','清远','东莞','中山','潮州','揭阳','云浮']

    ua = UserAgent()
    headers = {

        'User-Agent': ua.random,

        'Host': 'lishi.tianqi.com',

        'Accept-Encoding': "gzip, deflate",

        'Connection': "keep-alive",

        'cache-control': "no-cache"
    }
    url = 'https://lishi.tianqi.com/'

    # 发送HTTP请求
    resp = requests.request("GET", url, headers=headers)

    resp.encoding = 'utf-8'

    # 检查请求是否成功
    if resp.status_code == 200:
        # 解析网页内容
        soup = BeautifulSoup(resp.text, 'html.parser')

        # 假设城市列表在一个<table>标签内，并且有特定的class或id
        # 你需要根据实际网页结构调整选择器
        cities_table = soup.find("div", {"class": "tablebox"})
        a = cities_table.find_all("ul", {"class": "table_list"})
        city_dict={}
        for i in a:
            b=i.find_all("li")
            for j in b:
                try:
                    if j.get_text().strip() in gd:
                        temp = j.find('a').get('href').replace("index.html", "")
                        city_dict[j.get_text().strip()] = temp.lstrip('/')
                except Exception as e:
                    pass
        print(city_dict)
    else:
        print('网页请求失败，状态码：', resp.status_code)
    csv_file = 'output.csv'
    # 打开文件，写入内容
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 写入标题行（如果有标题的话）
        writer.writerow(['城市名称', '拼音'])
        # 写入字典内容
        for key, value in city_dict.items():
            writer.writerow([key, value])
    print(f'数据已保存到 {csv_file}')
    return city_dict

