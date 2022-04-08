import base64
import hashlib
import os
import random
import time

from lxml import etree
from lxml.html import tostring

import get_token
import redis
import requests
import logger
import database
import config

'''
 * @author dingyanan
 * @date 2021/04/12 15:48
'''

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/wechat%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('wechat', log_path)


# 目标url
def get_mail():
    # 获取cookie
    try:
        cookie_pool = redis.Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password)
        cookies = (cookie_pool.hget('wechatCookiePool', config.Wechat_account).decode('utf-8'))

    except Exception as e:
        logging.info("redis请求cookie失败,重新请求:{}".format(e))

    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    # 使用Cookie，跳过登陆操作
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }

    # 获取token
    get_token.get_token()
    token = (cookie_pool.hget('wechatCookiePool', 'token').decode('utf-8'))

    # 获取最近2页
    for page in range(1):
        for fakeid in config.fakeids.keys():
            data = {
                "token": token,
                "lang": "zh_CN",
                "f": "json",
                "ajax": "1",
                "action": "list_ex",
                "begin": 5 * page,
                "count": "5",
                "query": "",
                "fakeid": fakeid,
                "type": "9",
            }

            # 使用get方法进行提交
            # time.sleep(random.uniform(3.1, 5.3))
            try:
                content_json = requests.get(url, headers=headers, params=data).json()
                if len(content_json) == 1:
                    logging.info('cookie失效：{}'.format(content_json))
                    break
            except Exception as e:
                logging.info("请求失败,重新请求:{}".format(e))

            app_list = content_json["app_msg_list"]
            item = {}
            item['site_id'] = (base64.b64decode(fakeid).decode('utf-8'))
            item['site_name'] = config.fakeids[fakeid]
            for data in app_list:
                time_local = time.localtime(data['update_time'])
                # # 转换成新的时间格式(2021-05-05 20:28:54)
                item['publish_time'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time_local))
                item['title'] = data['title'].replace('\u200b', '')
                item['url'] = host = data['link']
                item['data_id'] = hashlib.md5(host.encode('utf-8')).hexdigest()
                item['source'] = config.fakeids[fakeid]
                try:
                    res_detail = requests.get(url=data['link'], headers=headers)
                    resp_detail = (res_detail.content.decode('utf-8'))
                    html = resp_detail
                    tree = etree.HTML(html)
                    body = tree.xpath('//div[@id="js_content"]')[0]
                    item['content'] = ''.join(tree.xpath('//div[@id="js_content"]//text()')).replace('\xa0', '')
                    item['images'] = tree.xpath('//div[@id="js_content"]//img/@data-src')
                    item['body_html'] = tostring(body, encoding='utf-8').decode()
                    database.GetJdStore().wechat_news(item)
                    logging.info('公众号为：{},时间：{},标题：{},图片：{},正文：{}'.format(item['url'],
                       item['publish_time'], item['title'], item['images'], item['content']))

                except Exception as e:
                    logging.info("公众号：{}，数据写入失败,title:{}".format(item['site_name'], e))


if __name__ == "__main__":
    # pass
    get_mail()
