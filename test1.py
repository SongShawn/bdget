# -- coding: utf-8 --

import urllib2
import re
from bs4 import BeautifulSoup

dest_url = 'http://171.221.172.13:8888/lottery/accept/projectList'

head_name = (u'区域', u'项目名称', u'预售证号', u'预售范围',
             u'住房套数', u'开发商咨询电话', u'登记开始时间',
             u'登记结束时间', u'项目报名状态')

# open url
page = urllib2.urlopen(dest_url)

# create bs object
bsObj = BeautifulSoup(page)

info_table = bsObj.find_all("table", class_=re.compile("^nav-table$"))

# 总是把"class="nav-table input-table""的表遍历出来，下边过滤一下
table_flag = 0
for table_elem in info_table :
    class_attr = table_elem['class']
    if (len(class_attr) == 1) and (class_attr[0] == "nav-table") :
        table_flag = 1
        break

if table_flag == 0 :
   print "can find table"
   exit(1)

out_str = ""

# 表头处理
thead_tr_th_list = table_elem.thead.tr.find_all("th")
for th_elem in thead_tr_th_list :
    if len(th_elem.get_text()) != 0 :
        out_str += th_elem.get_text()
        out_str += "  "
print out_str

# print info_table

# str1 = 'nav-table'
# str2 = 'nav-table input-table'
#
# ret = re.match("^nav-table$", str2)
# if ret is not None :
#     print ret.group()
# else :
#     print "not match"


# print page.read()