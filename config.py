
import random
# mysql 服务器
host = "127.0.0.1"
port = 3306
user = "root"
passwd = "123"
database = "news"
charset = "utf8"

# redis
redis_host = '127.0.0.1'
redis_port = 6379
redis_password = '123'
wechat_md5 = 'news'



# 公众号fakeid,抓包获取
fakeids = {'MzAwNDA3Nzg5MA==': '杭州统一战线', 'MzAwODQ4OTY3NQ==': '杭州知联', 'MzAxMjA0NDk2NQ==': '滨江统一战线',
           'MzAxMjA5NDE5MA==': '西湖统一战线', 'MzA4NjU1OTE4Mg==': '拱墅统一战线', 'MjM5MzM2MDk3OA==': '杭州市上城区统一战线',
           'MzA3MjA4MjQ5MQ==': '余杭统一战线', 'MzAwNjEwMDI0Mg==': '萧山统一战线', 'MzA5MDQ0NjQxNg==': '富阳统一战线',
           'MzU0Mjc2MTM4NQ==': '建德统一战线', 'MjM5OTYwNzQ3Nw==': '淳安统一战线', 'MjM5NjQwNzgxMQ==': '临安统站统一战线'
           }

# Es配置
es_index = 'news_m2'
es_hosts = ['192.168.20.164:9200', '192.168.20.165:9200', '192.168.20.166:9200']

# kafka配置
TOPIC = 'news_v1'
TOPIC2 = 'news_images'
SERVER = '192.168.20.211:9092, 192.168.20.212:9092, 192.168.20.213:9092'

# 微信账号
Wechat_list = ['内部优惠折扣券', '溯源防伪开放平台', '超级玛2 Pro', '超级码3 Test']
Wechat_account = random.choice(['内部优惠折扣券', '溯源防伪开放平台', '超级玛2 Pro', '超级码3 Test'])

# dingding接受cookie电话
wechat = 'wechat'
token = 'token'
phone_number = '1888888888'
