# Created by Max on 2/3/18
import re

__author__ = 'Max'
import hashlib


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


# 从字符串提取数字
def extract_num(text):
    match_re = re.match('.*?(/d+).*', text)
    if match_re:
        return int(match_re.group(1))
    else:
        return 0
