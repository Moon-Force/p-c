import csv

# CSV文件名
csv_file = 'output.csv'

# 用于存储URL的列表
urls = []

# 打开CSV文件
with open(csv_file, mode='r', encoding='utf-8') as file:
    # 创建csv阅读器
    reader = csv.reader(file)
    # 读取CSV文件的标题行（如果CSV文件有标题行的话）
    headers = next(reader)  # 跳过标题行
    # 遍历CSV文件中的每一行
    for row in reader:
        # 假设URL在第二列，索引为1
        url = row[1]
        # 将URL添加到列表中
        urls.append(url)

# 打印出所有URL
for url in urls:
    print(url)
