# -*-coding:utf-8-*-
import base64
import os
import random
import time
import database
import get_token
import redis
import requests
import logger

import config

'''
 * @author dingyanan
 * @date 2021/04/12 15:48
'''

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/wechat%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('wechat', log_path)

# 查询公众号的base64对应的id

# 目标url
def get_mail():
    # 获取cookie
    try:
        cookie_pool = redis.Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password)
        cookies = (cookie_pool.hget('wechatCookiePool', config.Wechat_account).decode('utf-8'))
    except Exception as e:
        logging.info("redis请求cookie失败,重新请求:{}".format(e))

    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    # 使用Cookie，跳过登陆操作
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }

    # token
    get_token.get_token()
    token = (cookie_pool.hget('wechatCookiePool', 'token').decode('utf-8'))
    tea_list = ['数农晨讯']
    keys = []
    values = []

    for page in range(1):
        for query in tea_list:
            data = {
                'action': 'search_biz',
                'begin': page * 5,
                'count': 5,
                'query': query,
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': 1,
            }
            try:
                content_json = requests.get(url, headers=headers, params=data, timeout=6).json()
                json_list = content_json['list']

                item = {}
                for data in json_list:
                    item['fakeid'] = data['fakeid']
                    item['name'] = data['nickname']
                    keys.append(item['fakeid'])
                    values.append(item['name'])
                    # database.GetJdStore().wechat_source(item)
                    logging.info('item为：{}'.format(item))

                # 返回了一个json，里面是每一页的数据
            except Exception as e:
                logging.info("请求失败,重新请求:{}".format(e))

    list_tea = dict(zip(keys, values))
    logging.info("公众号为:{}".format(list_tea))


if __name__ == "__main__":
    get_mail()
