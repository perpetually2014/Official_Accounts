# coding=utf8
import os
import time
from lxml import etree
import requests
import logger
import database


'''
 * @author dingyanan
 * @date 2021/04/12 15:48
'''

# 数据导入工具

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/wechat_3word%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('news', log_path)

# 目标url
def get_mail():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }
    data_list = database.GetJdStore().getSearch()
    n = 5
    for data in [data_list[i:i + n] for i in range(0, len(data_list), n)]:
        # 便利整个数据库，每5个元素遍历一次，获取url
        # title ,link,pubdate,thumbnail_url,description
        try:
            res = requests.get(data[1], headers=headers)
            resp = res.content.decode('utf-8')
            html = etree.HTML(resp)

            try:
                name = html.xpath('//strong[@class="profile_nickname"]/text()')[0]
                logging.info("公众号：{}".format(name))
            except Exception as e:
                logging.info("公众号：{}，解析失败,name:{}".format(data,name))
                logging.info(e)

            database.GetJdStore().get_insert_year(name,data[0], data[1], data[2], data[3], data[4])
        except Exception as e:
            logging.info("公众号：{}，数据写入失败,title:{}".format(data[0]))
            logging.info(e)


if __name__ == "__main__":
    # pass
    get_mail()


