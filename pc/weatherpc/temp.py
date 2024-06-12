import os
import random
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from pandas import Series, DataFrame

from getUrls import geturl

# 设置请求头
headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',

    'Host': 'lishi.tianqi.com',

    'Accept-Encoding': "gzip, deflate",

    'Connection': "keep-alive",

    'cache-control': "no-cache"

}


def toexcel(new_data, city, date):
    file_path = city + "的天气.xlsx"
    try:
        # 读取现有的Excel文件
        existing_data = pd.read_excel(file_path)

        # 将新数据追加到现有数据中
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        # 将合并后的数据写回Excel文件
        combined_data.to_excel(file_path, index=False)
        print(f"{date}数据结果已追加到 {file_path}")
    except FileNotFoundError:
        # 如果文件不存在，直接写入新数据
        new_data.to_excel(file_path, index=False)
        print(f"新创建 {file_path}")


# 获得爬取网站的链接
urls = geturl()
# urls = {'北京':'https://lishi.tianqi.com/beijing/202405.html'}
all_weather_data = []
random_number = random.randint(20, 30)
for city, url in urls.items():
    print("Start : %s" % time.ctime())
    # 发送 GET 请求
    time.sleep(random_number)
    resp = requests.request("GET", url, headers=headers)

    resp.encoding = 'utf-8'

    soup = bs(resp.text, 'html.parser')

    data_all = []

    tian_three = soup.find("div", {"class": "tian_three"})
    try:
        lishitable_content = tian_three.find_all("li")
        for i in lishitable_content:

            lishi_div = i.find_all("div")

            data = []
            date_str = city

            # 使用正则表达式匹配非数字的字符序列
            match = re.match(r'(\D+)(\d{4}年\d{1,2}月)', date_str)
            if match is not None:
                data.append(match.group(1))
                data.append(match.group(2))
            else:
                raise Exception("匹配分离失败：82行")

            for j in lishi_div:
                data.append(j.text)

            data_all.append(data)
        weather = pd.DataFrame(data_all)

        weather.columns = ["城市", "数据日期", "当日信息", "最高气温", "最低气温", "天气", "风向信息"]

        weather['当日信息'].apply(str)

        # 把当日信息分为日期和星期
        # ['2022-06-30 星期四 ', '32℃', '26℃', '多云', '东风 2级'] 分为 ['2022-06-30', 星期四 ', '32℃', '26℃', '多云', '东风 2级']
        result = DataFrame(weather['当日信息'].apply(lambda x: Series(str(x).split(' '))))

        result = result.loc[:, 0:1]

        result.columns = ['日期', '星期']

        # 把风向信息分为风向和级数
        # ['2022-06-30 星期四 ', '32℃', '26℃', '多云', '东风 2级'] 分为 ['2022-06-30', 星期四 ', '32℃', '26℃', '多云', '东风',2级']
        weather['风向信息'].apply(str)
        result1 = DataFrame(weather['风向信息'].apply(lambda x: Series(str(x).split(' '))))

        result1 = result1.loc[:, 0:1]

        result1.columns = ['风向', '级数']

        weather = weather.drop(columns='当日信息')

        weather = weather.drop(columns='风向信息')

        weather.insert(loc=2, column='日期', value=result['日期'])

        weather.insert(loc=3, column='星期', value=result['星期'])

        weather.insert(loc=7, column='风向', value=result1['风向'])

        weather.insert(loc=8, column='级数', value=result1['级数'])

        weather[['最高气温', '最低气温']] = weather[['最高气温', '最低气温']].apply(
            lambda x: x.str.replace('℃', ''))  # 去除℃符号

        weather[['最高气温', '最低气温']] = weather[['最高气温', '最低气温']].astype(int)  # 转换为整数类型

        weather[['日期', '星期']] = weather[['日期', '星期']].apply(lambda x: x.str.replace('\n', ''))  # 去除\n符号

        weather[['日期', '星期']] = weather[['日期', '星期']].apply(lambda x: x.str.replace('\t', ''))  # 去除\t符号

        weather[['风向', '级数']] = weather[['风向', '级数']].apply(lambda x: x.str.replace('\n', ''))  # 去除\n符号

        weather[['风向', '级数']] = weather[['风向', '级数']].apply(lambda x: x.str.replace('\t', ''))  # 去除\t符号

        # all_weather_data.append(weather)
        a = pd.DataFrame(weather)
        toexcel(a, city[0:2], city[2:])
        # merged_weather_data = pd.concat(all_weather_data, ignore_index=True)
        print("end : %s" % time.ctime())
    except Exception as e:
        print("发生异常：", repr(e))

# 保存到本地 Excel 文件
