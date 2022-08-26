# coding=utf8
import os
import time
from lxml import etree
import redis
import requests
import logger
import config
import dingding
'''
 * @author dingyanan
 * @date 2021/04/12 15:48
'''

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/wechat%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('wechat', log_path)

def get_token(cookies,Wechat_account):
    t_url = "https://mp.weixin.qq.com/"
    # 使用Cookie，跳过登陆操作
    headers = {
        "Cookie": cookies,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }

    resp = requests.get(t_url, headers=headers)
    res = resp.content.decode('utf-8')
    html = etree.HTML(res)

    try:
        token_url = html.xpath('//a[@class="weui-desktop-btn__head-opr weui-desktop-account__message"]/@href')[0]
        token = token_url.split("token=")[1]
        # logging.info("token请求成功：{},微信号为：{}".format(token, Wechat_account))
        return token
    except Exception as e:
        dingding.sendmessage('三农微信账号：{}，过期了请重新登录'.format(Wechat_account))
        logging.error('账号失效，重新登录:{}'.format(e))
        return None


if __name__ == "__main__":
    get_token()
    # pass
