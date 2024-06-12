import csv
import datetime
import sys


def geturl():
    csvurls_dict = csvread()
    now = datetime.datetime.now()
    # 获取当前月份
    current_year = now.year
    current_month = now.month
    base_url = 'https://lishi.tianqi.com/'
    urls = {}
    years = ['2023','2024']
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for key, value in csvurls_dict.items():
        tempurl = base_url + value
        for year in years:
            if int(year) == now.year:
                for month in range(1, current_month + 1):
                    formatted_month = f"{month:02d}"
                    url = f"{tempurl}{year}{month:02d}.html"
                    tempkey = key + str(year) + "年" + str(formatted_month) + "月"
                    urls[tempkey] = url
            else:
                for month in months:
                    url = f"{tempurl}{year}{month}.html"
                    tempkey = key + str(year) + "年" + str(month) + "月"
                    urls[tempkey] = url

    return urls


def csvread():
    csv_file = 'output.csv'

    # 用于存储URL的列表
    url_dict = {}

    # 打开CSV文件
    with open(csv_file, mode='r', encoding='utf-8') as file:
        # 创建csv阅读器
        reader = csv.reader(file)
        # 读取CSV文件的标题行（如果CSV文件有标题行的话）
        headers = next(reader)  # 跳过标题行
        # 遍历CSV文件中的每一行
        for row in reader:
            # 假设URL在第二列，索引为1
            if row[2] == '1':
                url_dict[row[0]] = row[1]
    print(url_dict)
    return url_dict
