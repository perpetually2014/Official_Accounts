
import json
import os

import redis
from flask import Flask, request

import logger

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/cookies.log'
logger_ = logger.log_conf('cookies', log_path)


import config

app = Flask(__name__)

@app.route('/PinDuoDuoCookieInterface', methods=['POST', 'GET'])
def cookie_pool():
    if request.method == 'GET':
        return 'give me cookie'

    if request.method == 'POST':
        # 获取插件上传的数据
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        pdd_account = json_data.get('pddAccount')
        pdd_cookie_str = json_data.get('pddCookie')
        pdd_account_type = json_data.get('pddAccountType')
        logger_.info('类型: {}, 账号: {}, Cookie: {}'.format(pdd_account_type, pdd_account, pdd_cookie_str))

        # 保存普通用户cookie到redis
        if pdd_account_type == 'ordinary':
            try:
                cookie_pool_conn = redis.Redis(host=config.redis_host, port=config.redis_port,password=config.redis_password)
                cookie_pool_conn.hset(name='wechatCookiePool', key=pdd_account, value=pdd_cookie_str)
                return 'true'
            except Exception as error:
                logger_.error('普通账号cookie保存至redis报错, %s' % error)
                return 'false'


if __name__ == '__main__':
    # app.debug = True
    app.debug = False
    app.run('0.0.0.0', 18083)
