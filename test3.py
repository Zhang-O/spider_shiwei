import urllib.request
from bs4 import BeautifulSoup
import re
import urllib.parse
import xlsxwriter
import pandas as pd
import numpy as np

from urllib import request, parse
from urllib.error import URLError
import json
import multiprocessing
import time

# 详情页面的 地址 存放在这里面
urls_of_detail = []
total_pages = 0

# 要爬取的内容 按序存成数组
_1 = []
_2 = []
_3 = []
_4 = []
_5 = []

issue_date_sum = []
project_address_sum = []
project_sector_sum = []
project_content_sum = []
company_name_sum = []
company_staff_sum = []
company_phone_sum = []

# 一级网址
url = 'http://www.stc.gov.cn/ZWGK/TZGG/GGSB/'

# page 表示第几页
def get_urls(url,page):
    # 构造 form 数据
    # postdata = urllib.parse.urlencode({'currDistrict': '', 'pageNo': page,'hpjgName_hidden':'','keyWordName':''})
    # postdata = postdata.encode('utf-8')
    #
    # #发送请求
    # response = urllib.request.urlopen(url, data=postdata)
    # html_cont = response.read()

    if page == 0:
        url = url  + 'index.htm'
    else:
        url = url + 'index_' + str(page) + '.htm'

    req = request.Request(url=url)
    res_data = request.urlopen(req)
    # print(res_data)
    html_cont = res_data.read()

    # 解析文档树
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    #
    # # 用正则表达式 查找 二级网站的网址 所在的 元素 tr
    trs = soup.find_all('a', href=re.compile(r"^./201"))

    # # 把 二级网站的网址存到 urls_of_detail 中
    for i in trs:
        # print(i['href'][2:])
        urls_of_detail.append(i['href'][2:])


def get_info(url,second_url):
    # s = urllib.request.urlopen(urls_of_detail[0])
    # 请求文档
    second_url = url + second_url
    s = urllib.request.urlopen(second_url)
    # 解析文档
    soup = BeautifulSoup(s, 'html.parser', from_encoding='utf-8')

    # 查找的内容  在 td 元素内  ，且没有任何唯一标识 ，找到所有td ，查看每个待爬取得内容在 list 中 的索引
    div = soup.find_all('div', class_=re.compile(r"TRS_Editor"))

    trs = div[0].find_all('tr')
    trs = trs[1:]
    # print(trs[0])
    print('trs num',len(trs))

    for tr in trs:
        tds = tr.find_all('td')
        _1.append(tds[0])
        _2.append(tds[1])
        _3.append(tds[2])
        _4.append(tds[3])
        if len(tds) == 5:
            _5.append(tds[4])
        else:
            _5.append('null')
        print(len(tds))

        # print(tds[0].string)
        # print(tds[1].string)
        # print(tds[2].string)
        # print(tds[3].string)

    # issue_date = tds[4].string
    # issue_date_sum.append(issue_date)
    # # print(issue_date)
    #
    # project_address = tds[9].string
    # project_address_sum.append(project_address)
    # # print(project_address)
    #
    # project_sector = tds[11].string
    # project_sector_sum.append(project_sector)
    # # print(project_sector)
    #
    # project_content = tds[12].string
    # project_content_sum.append(project_content)
    # # print(project_content)
    #
    # company_name = tds[13].string
    # company_name_sum.append(company_name)
    # # print(company_name)
    #
    # company_staff = tds[15].string
    # company_staff_sum.append(company_staff)
    # # print(company_staff)
    #
    # if tds[16].contents[0]:
    #     company_phone = tds[16].contents[0]
    #     company_phone_sum.append(company_phone)
    # else:
    #     company_phone = soup.find_all(text=re.compile("^"
    #                                                   "(\d{3}-\d{8})"
    #                                                   "|(\d{11})"
    #                                                   "|(\d{8}-\d{4})"
    #                                                   "|(\d{3}-\d{8}-\d{4})"
    #                                                   "|(\d{8})"))
    #     company_phone_sum.append(company_phone)
    # print(company_phone)



# print(response.read().decode('utf-8','ignore'))

# 网站显示一共有 1036 页
num0 =0
for page in range(0,7):
    num0 += 1
    # print(num0)
    get_urls(url, page)

# 把所有的二级网站 存成文本
with open('urls_all_liyou','w') as f:
    f.write(str(urls_of_detail))

# print(len(urls_of_detail))
# print(len(set(urls_of_detail)))

print('urls num :' , len(urls_of_detail))
num=0 #  这个主要用于调试 爬的过程中如果出错 看看是在哪个网址出的
for second_url in urls_of_detail:
    num += 1
    print('page num :  ', num)

    if num in [15,42]:
        continue
    if num > 54:
        break

    get_info(url, second_url)

print('end ----------')
print(len(_1))
print(len(_2))
print(len(_3))
print(len(_4))
print(len(_5))
# 用 pandas 导出 成excel
# df2 = pd.DataFrame({ '序号' : pd.Categorical(_1),
#                      '区域' : pd.Categorical(_2),
#                      '类型' : pd.Categorical(_3),
#                      '设置地点（路口或路段）' : pd.Categorical(_4),
#                      '方向' : pd.Categorical(_5),
#
#                      })


# df2.to_excel('jiaotong.xlsx','liyou')

workbook = xlsxwriter.Workbook('./liyou.xlsx')
# 1. -------------------------------------写入学生成绩 ----------------------------------------

# 1.------------------ 创建一个 worksheet 存放具体分数-------------------------------
ws = workbook.add_worksheet('liyou')
#设置宽度
ws.set_column('A:A', 25)
ws.set_column('B:B', 25)
ws.set_column('C:C', 15)
ws.set_column('D:D', 15)
ws.set_column('E:E', 15)
# 写表头
ws.write(0, 0, '序号')
ws.write(0, 1, '区域')
ws.write(0, 2, '类型')
ws.write(0, 3, '设置地点')
ws.write(0, 4, '方向')

number = len(_1)
for i in range(number):
    ws.write(i + 1, 0, str(_1[i]))
    ws.write(i + 1, 1, str(_2[i]))
    ws.write(i + 1, 2, str(_3[i]))
    ws.write(i + 1, 3, str(_4[i]))
    ws.write(i + 1, 4, str(_5[i]))
    print('here')

workbook.close()














