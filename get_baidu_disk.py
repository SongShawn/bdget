# -- coding: utf-8 --
import random
import urllib2

import math

import datetime
from bs4 import BeautifulSoup


class StringFactory:
    char_0_9 = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    char_a_z = (
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z')
    char_A_Z = (
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z')
    char_0_9_a_z_A_Z = char_0_9 + char_a_z + char_A_Z

    def __init__(self, prefix="", str_len=0, elem_set=()):
        self.prefix = prefix
        self.str_len = str_len
        self.elem_set = elem_set
        self.elem_set_num = len(elem_set)
        self.num = 0
        self.generated_num = 0
        self.only_prefix = 0
        self.counter = []
        self._calc_private_data()

    def _calc_private_data(self):
        if self.str_len is 0 or self.elem_set_num is 0:
            if len(self.prefix) is 0:
                self.num = 0
            else:
                self.num = 1
                self.only_prefix = 1
        else:
            self.num = math.pow(self.elem_set_num, self.str_len)
            for i in range(0, self.str_len):
                self.counter.append(0)

    def _make_one_string(self):
        if self.num == self.generated_num:
            return None

        ret = self.prefix
        for i in range(0, self.str_len):
            ret += self.elem_set[self.counter[i]]
        self.generated_num += 1

        for i in range(self.str_len - 1, -1, -1):
            if self.counter[i] is self.elem_set_num - 1:
                self.counter[i] = 0
                continue
            else:
                self.counter[i] += 1
                break

        return ret

    def reset(self):
        '''重置后，对象可以从头开始生成字符串。'''
        self.counter = []
        for i in range(0, self.str_len):
            self.counter.append(0)
        self.generated_num = 0

    def get_first_str(self, num=1):
        '''返回tuple，默认返回一个'''
        ret = []
        for i in range(0, num):
            str = self._make_one_string()
            if str is None:
                if len(ret) is 0:
                    return None
                else:
                    return ret
            ret.append(str)
        return ret

    def get_next_str(self, num=1):
        '''同get_first_str'''
        return self.get_first_str(num)

    def get_str_num(self):
        return self.num

    def get_str_remain_num(self):
        return self.num - self.generated_num

    def get_str_generated_num(self):
        return self.generated_num


# 分享被取消
# 啊哦，你来晚了，分享的文件已经被取消了，下次要早点哟。
def bd_res_share_canceled(bs_obj):
    flag = bs_obj.find("div", {"id": "share_nofound_des"})
    if flag is None:
        return False
    return True


# 页面未找到，该资源从来没有分享过
# 啊哦，你所访问的页面不存在了。
def bd_page_not_existed(bs_obj):
    flag = bs_obj.find("div", {"class": "module-error"})
    if flag is None:
        return False
    return False


# @ret True  url有效
#      False url无效
def bd_is_url_valid(bs_obj):
    if bd_res_share_canceled(bs_obj) is True:
        return False
    if bd_page_not_existed(bs_obj) is True:
        return False
    return True


# @ret True  需要密码
def bd_is_shared_page_needs_password(bs_obj):
    flag = bs_obj.find("dl", {"class": "pickpw clearfix"})
    if flag is None:
        return False
    return True


def bd_get_name(bs_obj):
    js_code = bs_obj.find_all("script", {"type": "text/javascript"})
    if js_code is None:
        print "page has no js code"
        return None
    else:
        for code in js_code:
            if len(code.get_text()) is not 0:
                index = code.get_text().find("yunData.FILENAME")
                if index is not -1:
                    file_name = code.get_text()[index:].split("\r\n")[0].split("=")[1]
                    return file_name[2:(len(file_name) - 2)]


BD_URL_BAD_PAGE = 0
BD_URL_SHARE_PAGE = 1
BD_URL_NEED_PASS = 2
BD_URL_INVALID_PAGE = 3
BD_ERR = 4


def bd_parse_page(bs_obj):
    if not bd_is_url_valid(bs_obj):
        return BD_URL_BAD_PAGE, None

    name = bd_get_name(bs_obj)
    if name is not None:
        return BD_URL_SHARE_PAGE, name

    if bd_is_shared_page_needs_password(bs_obj):
        return BD_URL_NEED_PASS, None

    return BD_URL_INVALID_PAGE, None


def bd_url_parse(url):
    page = urllib2.urlopen(url)
    if page is None:
        return BD_URL_INVALID_PAGE, None

    bs_obj = BeautifulSoup(page.read())
    if bs_obj is None:
        return BD_ERR, None

    return bd_parse_page(bs_obj)


bd_url_prefix = 'https://pan.baidu.com/s/1skJ'
url_factory = StringFactory(bd_url_prefix, 4, StringFactory.char_0_9_a_z_A_Z)

url = url_factory.get_first_str()
begin = datetime.datetime.now()
while url is not None:
    ret = bd_url_parse(url[0])
    if ret[0] is BD_URL_SHARE_PAGE:
        print "good res : ", url, "   ", ret[1]
    elif ret[0] is BD_URL_NEED_PASS:
        print "pass res : ", url, "   ", ret[1]
    if url_factory.get_str_generated_num() % 100 is 0:
        print url[0], " ", url_factory.get_str_generated_num(), " ", url_factory.get_str_remain_num()
        end = datetime.datetime.now()
        print end - begin
        begin = datetime.datetime.now()
    url = url_factory.get_next_str()


# 性能问题，urlopen是同步接口，按当前的实现，没处理100个页面需要耗时1分钟
# https://pan.baidu.com/s/1skJ001B   100   14776236.0
# 0:01:05.970435
# https://pan.baidu.com/s/1skJ003d   200   14776136.0
# 0:01:04.472217
# https://pan.baidu.com/s/1skJ004P   300   14776036.0
# 0:01:08.453893
# https://pan.baidu.com/s/1skJ006r   400   14775936.0