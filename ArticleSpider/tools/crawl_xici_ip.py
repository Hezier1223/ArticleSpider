# Created by Max on 2/9/18
import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', user='root', password='root', db='article_spider', charset='utf8')
cursor = conn.cursor()


def crawl_ips():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/64.0.3282.140 Safari/537.36 '
    }
    ip_list = []

    for i in range(2121):
        response = requests.get('https://www.kuaidaili.com/free/inha/{0}'.format(i), headers=headers)
        selector = Selector(text=response.text)
        all_trs = selector.css('#list tr')

        for tr in all_trs[1:]:
            all_tds = tr.css('td::text').extract()
            ip = all_tds[0]
            port = all_tds[1]
            proxy_type = all_tds[3]
            speed = all_tds[5]
            print(speed, type(speed))
            if speed:
                if type(speed) == 'str':
                    speed = 0
                else:
                    speed = speed.split('秒')[0]
            else:
                speed = 0

            ip_list.append((ip, port, proxy_type, speed))

        for ip_info in ip_list:
            cursor.execute(
                "INSERT proxy_ip(ip, port, speed, type) VALUES('{0}', '{1}', {2}, '{3}')".format(ip_info[0], ip_info[1],
                                                                                                 ip_info[3], ip_info[2]
                                                                                                 )
            )
            conn.commit()


class GetIP(object):
    def judge_ip(self, ip_id, ip, port):
        http_url = 'http://www.baidu.com'
        proxy_url = 'https://{0}:{1}'.format(ip, port)
        proxy_dict = {
            'http': proxy_url
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print('Invalid ip and port', e)
            self.delete_proxy(ip_id)
            return True
        else:
            code = response.status_code
            if 200 <= code <= 300:
                return True
            else:
                print('Invalid ip and port')
                self.delete_proxy(ip_id)
                return False

    # 从数据库中删除无效的IP
    def delete_proxy(self, ip_id):
        delete_sql = 'DELETE FROM article_spider.proxy_ip WHERE id={0}'.format(ip_id)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def get_random_ip(self):
        random_sql = "SELECT id, ip, port FROM article_spider.proxy_ip ORDER BY rand() LIMIT 1"
        result = cursor.execute(random_sql)
        if result == 1:
            for ip_info in cursor.fetchall():
                ip_id = ip_info[0]
                ip = ip_info[1]
                port = ip_info[2]

                judge_result = self.judge_ip(ip_id, ip, port)
                if judge_result:
                    return 'http://{0}:{1}'.format(ip, port)
                else:
                    return self.get_random_ip()
