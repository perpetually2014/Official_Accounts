# -*-coding:utf-8-*-
import base64
import datetime
import os
import random
import threading
import time
from lxml.html.clean import Cleaner
import es_dbs
import index_code
from Images_parser import body_html_images
from NewsParser import GeneralNewsExtractor
from lxml import etree
from lxml.html import tostring
import get_token
import redis
import requests
import kafka_
import logger
import database
import config
import hashlib
import clean_body_html

'''
 * @author dingyanan
 * @date 2021/04/12 15:48
'''
log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/wechat%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('wechat', log_path)

try:
    # 获取cookie
    cookie_pool = redis.Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password)
    # 初始化微信账号，和公众号
    cookie_pool.delete(config.wechat)
    cookie_pool.delete(config.token)
    index_code.get_wechat_code()
except Exception as e:
    logging.info("redis请求cookie失败,重新请求:{}".format(e))

def get_index(Wechat_account, cookies, token):
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }
    try:
        bs64list = cookie_pool.rpop(config.wechat)
        names = eval(base64.b64decode(bs64list).decode('utf-8'))
    except Exception as e:
        cookie_pool.rpush(config.wechat, bs64list)
        logging.error('链接redis出错：{}'.format(e))

    pages = 2
    for page in range(pages):
        item = {}
        item['source'] = names['name']
        item['site_name'] = '微信公众号'
        item['site_id'] = names['site_id']
        item['level'] = 3
        item['type'] = 2
        fakeid = names['fakeid']
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
        try:
            url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
            time.sleep(2.1)
            content_json = requests.get(url, headers=headers, params=data).json()
        except Exception as e:
            logging.info("请求失败,重新请求:{},{}".format(e, content_json))

        status_code = content_json.get('base_resp').get('ret')
        # { "base_resp": { "err_msg": "invalid args", "ret": 200002    } }
        if status_code == 200002:
            print('参数错误：{}'.format(item['source']))
            item['is_update'] = -1
            item['publish_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
            # 记录数据量
            database.GetJdStore().update(item)
        # {'base_resp': {'err_msg': 'freq control', 'ret': 200013}}
        elif status_code == 200013:
            cookie_pool.rpush(config.wechat, bs64list)
            cookie_pool.sadd(config.token, Wechat_account)
            logging.warning('账号:{},被系统限制:{}，稍后重试:{}'.format(Wechat_account, item['source'], status_code))
            break
        # "ret": 0
        elif status_code == 0:
            data_list = content_json.get("app_msg_list")
            app_msg_cnt = content_json.get('app_msg_cnt')
            item['count'] = app_msg_cnt
            item['data_list'] = data_list
            run = {}
            run['fakeid'] = fakeid
            run['count'] = app_msg_cnt
            run['spider_time'] = time.strftime("%Y-%m-%d %H:%M:%S")

            # 记录数据量
            database.GetJdStore().spider_time(run)
            logging.info('账号：{}，数量：{}'.format(item['source'], item['count']))
            get_wechat(cookies, item)
        else:
            # 200003
            cookie_pool.sadd(config.token, Wechat_account)
            logging.warning('账号无效:{},状态码：{}'.format(Wechat_account,status_code))
            break

def get_wechat(cookies, wechat_item):
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }
    data_list = wechat_item['data_list']
    item = {}
    item['source'] = wechat_item['source']
    item['site_name'] = wechat_item['site_name']
    item['site_id'] = wechat_item['site_id']
    item['level'] = wechat_item['level']
    item['type'] = wechat_item['type']

    for data in data_list[:]:
        publishtime2 = datetime.datetime.fromtimestamp(data['update_time'])
        item['publish_time'] = str(publishtime2)
        item['title'] = data['title']
        item['url'] = host = data['link']
        item['data_id'] = hashlib.md5(host.encode('utf-8')).hexdigest()
        md5_news = item['data_id'].encode('utf-8')
        ret = cookie_pool.sadd(config.wechat_md5, md5_news)
        if ret == 0:
            print('数据重复,被过滤:{},名称：{}'.format(item['publish_time'],item['source']))
        else:
            res_detail = requests.get(url=data['link'], headers=headers)
            resp_detail = (res_detail.content.decode('utf-8'))
            html = resp_detail
            result = get_detail(html, host)
            tree = etree.HTML(html)
            body = tree.xpath('//div[@id="js_content"]')[0]
            body_html = tostring(body, encoding='utf-8').decode()
            body_html = clean_body_html.body_html(body_html)
            item['images'] = (tree.xpath('//div[@id="js_content"]//img/@data-src'))
            item['gather_time'] = str(time.strftime("%Y-%m-%d %H:%M:%S"))
            item['content'] = result['content']
            # 去掉样式
            cleaner = Cleaner(style=True, scripts=True, comments=True, javascript=True, page_structure=False,
                              safe_attrs_only=False)
            # 清理微信样式
            item['body_html'] = cleaner.clean_html(body_html)
            item = body_html_images.images_parser(result=item, host=host)
            print('公众号:{},时间：{}'.format(item['source'],item['publish_time']))
            # kafka_.kafka(item)
            # es_dbs.parse(item)

# 提取详情页
def get_detail(html, host):
    try:
        extractor = GeneralNewsExtractor()
        result = extractor.extract(html, title_xpath='', host=host, author_xpath='',
                                   publish_time_xpath='', body_xpath='//div[@id="js_content"]')
        return result
    except Exception:
        return


if __name__ == "__main__":
    Thread_list = []
    while True:
        # 所有账号都无效，程序暂停
        if cookie_pool.scard(config.token) == len(config.Wechat_list):
            logging.info('所有账号被系统限制，稍后重试')
            break
        for Wechat_account in (config.Wechat_list):
            cookies = (cookie_pool.hget('wechatCookiePool', Wechat_account).decode('utf-8'))
            token = get_token.get_token(cookies, Wechat_account)
            try:
                t = threading.Thread(target=get_index, args=(Wechat_account, cookies, token))
                Thread_list.append(t)
                t.start()
            except Exception as e:
                raise e
        for t in Thread_list:
            t.join(timeout=10)
