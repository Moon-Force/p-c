import re
import time
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


# 设置请求头

headers = {

    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
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


now = datetime.now()

# 获取年份
year = str(now.year)
# 获取月份
month = str(now.month)
formatted_month = format(now.month, '02d')

urls = {'中山': 'https://www.tianqi.com/zhongshan/7/', '深圳': 'https://www.tianqi.com/shenzhen/7/'}
# urls = {'北京':'https://lishi.tianqi.com/beijing/202405.html'}
all_weather_data = []
for city, url in urls.items():
    print("Start : %s" % time.ctime())
    # 发送 GET 请求
    resp = requests.request("GET", url, headers=headers)

    resp.encoding = 'utf-8'

    soup = bs(resp.text, 'html.parser')

    data_all = []

    tian_three = soup.find("div", {"class": "weaone_b"})
    try:
        content = tian_three.find_all("div")
        weather = content[0].get_text()
        # 选取第一个句号前面的字符串
        first_part = weather.split('。')
        # 选取第一个句号前面的字符串 分离出天气 今日天气：中山市，多云,27℃~34℃,南风4级，当前温度31℃。
        weather_items = first_part[0].split(',')
        day = content[1].get_text()
        day_items = day.split()
        data = []
        data.append(city)
        data.append( year + '年' + formatted_month + '月')
        data.append(now.strftime("%Y-%m-%d"))
        data.append(day_items[1])
        # 分离温度
        numbers = re.findall(r'\d+', weather_items[1])
        temperatures = [int(num) for num in numbers]
        data.append(temperatures[1])
        data.append(temperatures[0])
        temp = weather_items[0].split('，')
        data.append(temp[1])
        #  分离风力
        match = re.match(r'(.+?)(\d+)级', weather_items[2])
        if match:
            # 分别获取匹配的文本和数字
            direction = match.group(1)
            level = match.group(2) + '级'
            data.append(direction)
            data.append(level)
        data_all.append(data)
        weather = pd.DataFrame(data_all)

        weather.columns = ["城市","数据日期","日期","星期", "最高气温", "最低气温", "天气", "风向","级数"]

        toexcel(weather, city, now.date())
        # merged_weather_data = pd.concat(all_weather_data, ignore_index=True)
    except Exception as e:
        print(city+ "未找到")

# 保存到本地 Excel 文件
