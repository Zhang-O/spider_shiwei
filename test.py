import urllib.request
from bs4 import BeautifulSoup
import re
import urllib.parse
import pandas as pd
import numpy as np

# 详情页面的 地址 存放在这里面
urls_of_detail = []
total_pages = 0

# 要爬取的内容 按序存成数组
issue_date_sum = []
project_address_sum = []
project_sector_sum = []
project_content_sum = []
company_name_sum = []
company_staff_sum = []
company_phone_sum = []

# 一级网址
url = 'http://www.sses.sh.cn:80//shhjkxw/eiareport/action/eia_eiaDetailList.do'

# page 表示第几页
def get_urls(url,page):
    # 构造 form 数据
    postdata = urllib.parse.urlencode({'currDistrict': '全市', 'pageNo': page})
    postdata = postdata.encode('utf-8')

    #发送请求
    response = urllib.request.urlopen(url, data=postdata)
    html_cont = response.read()

    # 解析文档树
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

    # 用正则表达式 查找 二级网站的网址 所在的 元素 tr
    trs = soup.find_all('tr', onclick=re.compile(
        r"^window.location='http://www.sses.sh.cn:80/shhjkxw/eiareport/action/eia_eiaReportDetail.do"))

    # 把 二级网站的网址存到 urls_of_detail 中
    for i in trs:
        urls_of_detail.append(i['onclick'][17:-1])


def get_info(second_url):
    # s = urllib.request.urlopen(urls_of_detail[0])
    # 请求文档
    s = urllib.request.urlopen(second_url)
    # 解析文档
    soup = BeautifulSoup(s, 'html.parser', from_encoding='utf-8')

    # 查找的内容  在 td 元素内  ，且没有任何唯一标识 ，找到所有td ，查看每个待爬取得内容在 list 中 的索引
    tds = soup.find_all('td')

    issue_date = tds[4].string
    issue_date_sum.append(issue_date)
    print(issue_date)

    project_address = tds[9].string
    project_address_sum.append(project_address)
    print(project_address)

    project_sector = tds[11].string
    project_sector_sum.append(project_sector)
    print(project_sector)

    project_content = tds[12].string
    project_content_sum.append(project_content)
    print(project_content)

    company_name = tds[13].string
    company_name_sum.append(company_name)
    print(company_name)

    company_staff = tds[15].string
    company_staff_sum.append(company_staff)
    print(company_staff)

    if tds[16].contents[0]:
        company_phone = tds[16].contents[0]
        company_phone_sum.append(company_phone)
    else:
        company_phone = soup.find_all(text=re.compile("^"
                                                      "(\d{3}-\d{8})"
                                                      "|(\d{11})"
                                                      "|(\d{8}-\d{4})"
                                                      "|(\d{3}-\d{8}-\d{4})"
                                                      "|(\d{8})"))
        company_phone_sum.append(company_phone)
    print(company_phone)



# print(response.read().decode('utf-8','ignore'))

# 网站显示一共有 21 页
for page in range(1,22):
    get_urls(url, page)

# 把所有的二级网站 存成文本
with open('urls','w') as f:
    f.write(str(urls_of_detail))

# print(len(urls_of_detail))
# print(len(set(urls_of_detail)))


num=0 #  这个主要用于调试 爬的过程中如果出错 看看是在哪个网址出的
for second_url in urls_of_detail:
    num += 1
    print(num)

    get_info(second_url)


# 用 pandas 导出 成excel
df2 = pd.DataFrame({ '发布日期' : pd.Categorical(issue_date_sum),
                     '项目地址' : pd.Categorical(project_address_sum),
                     '项目所属行业' : pd.Categorical(project_sector_sum),
                     '项目内容' : pd.Categorical(project_content_sum),
                     '建设单位名称' : pd.Categorical(company_name_sum),
                     '建设单位联系人' : pd.Categorical(company_staff_sum) ,
                     '建设单位联系方式':pd.Categorical(company_phone_sum)
                     })


df2.to_excel('shanghai.xlsx')










