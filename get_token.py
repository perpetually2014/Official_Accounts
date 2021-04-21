# coding=utf8
import os

import time
from lxml import etree
import redis
import requests
import logger
import config

'''
 * @author dingyanan
 * @date 2021/04/12 15:48
'''

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/token%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('news', log_path)


def get_token():
    # 获取cookie
    try:
        cookie_pool = redis.Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password)
        cookies = (cookie_pool.hget('wechatCookiePool', 'perpetaully2019').decode('utf-8'))

    except Exception as e:
        logging.info("redis请求cookie失败,重新请求:{}".format(e))

    t_url = "https://mp.weixin.qq.com/"

    # 使用Cookie，跳过登陆操作
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }
    resp = requests.get(t_url, headers=headers)
    res = resp.content.decode('utf-8')
    html = etree.HTML(res)
    token_url = html.xpath('//a[@class="weui-desktop-btn__head-opr weui-desktop-account__message"]/@href')[0]
    token = token_url.split("token=")[1]

    try:

        cookie_pool.hset(name='wechatCookiePool', key='token', value=token)
        logging.info("token 保存至redis成功：{}".format(token))

    except Exception as error:
        logging.error('普通账号cookie保存至redis报错, %s' % error)


if __name__ == "__main__":
    # get_token()
    pass
