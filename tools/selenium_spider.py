# Created by Max on 2/4/18
import time
from selenium import webdriver

# 利用浏览器进行知乎登录
browser = webdriver.Chrome(executable_path='/Users/Arthur/Documents/chromedriver')
browser.get('https://www.zhihu.com/signin')
browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input').send_keys(
    '13611969835')

browser.find_element_by_css_selector('.SignFlow-password .SignFlowInput .Input-wrapper input').send_keys(
    'zzh921223')

browser.find_element_by_css_selector('.Button.SignFlow-submitButton').click()

time.sleep(10)
Cookies = browser.get_cookies()
