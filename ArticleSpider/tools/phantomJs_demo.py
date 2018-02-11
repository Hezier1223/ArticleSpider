# Created by Max on 2/10/18
from selenium import webdriver

browser = webdriver.PhantomJS(executable_path='/Applications/phantomjs-2.1.1-macosx 2/bin/phantomjs')
browser.get(
    'https://detail.tmall.com/item.htm?spm=a3211.35388-8920366.mobileItemSquare_1514958584244_12.2.37d54b8djJWWbF&id'
    '=562634611177&rn=236700ed3e21f02525b86c5d5dbc3806&abbucket=19')

print(browser.page_source)
browser.quit()
