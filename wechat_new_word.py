import os
import random
import time

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

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/wechat_new_word%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('news', log_path)


# 目标url
def get_mail():
    # 获取cookie
    try:
        cookie_pool = redis.Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password)
        cookies = (cookie_pool.hget('wechatCookiePool', 'perpetaully2019').decode('utf-8'))

    except Exception as e:
        logging.info("redis请求cookie失败,重新请求:{}".format(e))

    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

    # 使用Cookie，跳过登陆操作
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }

    # token
    get_token.get_token()
    token = (cookie_pool.hget('wechatCookiePool', 'token').decode('utf-8'))

    # 获取最近20页
    for page in range(3):
        for fakeid in config.fakenew.keys():
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
            time.sleep(random.uniform(2.1, 5.3))
            try:
                content_json = requests.get(url, headers=headers, params=data).json()
                logging.info(
                    '页码 {},fakeid {},返回json结果'.format(page, config.fakenew[fakeid]))
                # 返回了一个json，里面是每一页的数据
            except Exception as e:
                logging.info("请求失败,重新请求:{}".format(e))

            try:
                app_list = content_json["app_msg_list"]
            except Exception as e:
                logging.info("解析失败,重新请求:{}".format(e))
            if len(app_list) > 0:
                for data in app_list:
                    # 近一年的
                    try:
                        database.GetJdStore().get_insert_1month(config.fakenew[fakeid], data['title'], data['link'],
                                                                time.localtime(data['update_time']),
                                                                data['cover'],
                                                                data['digest'])
                    except Exception as e:
                        logging.info("公众号：{}，数据写入失败,title:{}".format(fakeid, data['title']))
                        logging.info(e)


if __name__ == "__main__":
    # pass
    get_mail()


