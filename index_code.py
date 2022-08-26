# -*-coding:utf-8-*-
import base64
import json
import redis,config
import database

try:
    redis_pool = redis.Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password)
except Exception as e:
    print('链接redis出错：{}'.format(e))

# 部门服务
def get_wechat_code():
    a = database.GetJdStore().get_search()
    n = 3
    name_list = []
    for r in [a[i:i + n] for i in range(0, len(a), n)]:
        item = {}
        item['name'] = r[0]
        item['fakeid'] = r[1]
        item['site_id'] = r[2]
        result = json.dumps(item)
        bs64_result = base64.b64encode(result.encode('utf-8'))
        redis_pool.lpush(config.wechat, bs64_result)
        name_list.append(item)
    print('微信账号：{}'.format(len(name_list)))



# 部门服务
def get_wechat_check():
    a = database.GetJdStore().get_check()
    n = 3
    name_list = []
    for r in [a[i:i + n] for i in range(0, len(a), n)]:
        item = {}
        item['name'] = r[0]
        item['fakeid'] = r[1]
        item['site_id'] = r[2]
        result = json.dumps(item)
        bs64_result = base64.b64encode(result.encode('utf-8'))
        redis_pool.lpush(config.checkwechat, bs64_result)
        name_list.append(item)
        # print(item)
    print('微信账号：{}'.format(len(name_list)))

if __name__=='__main__':
    # get_wechat_code()
    get_wechat_check()