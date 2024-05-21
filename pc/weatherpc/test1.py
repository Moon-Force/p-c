import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()
headers = {

        'User-Agent': ua.random,

        'Host': 'lishi.tianqi.com',

        'Accept-Encoding': "gzip, deflate",

        'Connection': "keep-alive",

        'cache-control': "no-cache"
}
url = 'https://lishi.tianqi.com/'
resp = requests.request("GET", url, headers=headers)

resp.encoding = 'utf-8'
if resp.status_code == 200:
        # 解析网页内容
    soup = BeautifulSoup(resp.text, 'html.parser')


    cities_table = soup.find("div", {"class": "tablebox"})
    a = cities_table.find_all("ul", {"class": "table_list"})
    city_dict={}
    for i in a:
        b=i.find_all("li")
        for j in b:
            try:
                temp = j.find('a').get('href').replace("/index.html", "")
                city_dict[j.get_text().strip()] = temp
            except Exception as e:
                    pass
        print(city_dict)
    else:
        print('网页请求失败，状态码：', resp.status_code)
print(city_dict)
