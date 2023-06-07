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
fakeids = {'MTI0MDU3NDYwMQ==': '央视新闻', 'MjM5ODEyOTAyMA==': '今日头条'}

# Es配置
es_index = 'data'
es_hosts = ['127.0.0.1:9200', '127.0.0.2:9200', '127.0.0.3:9200']

# kafka配置
TOPIC = 'data1'
SERVER = '127.0.0.1:9092, 127.0.0.2:9092, 127.0.0.3:9092'

# 微信账号
Wechat_list = ['data1', 'data2', 'data3']
Wechat_account = random.choice(['data1', 'data2', 'data3'])

# dingding接受cookie电话
wechat = 'wechat'
token = 'token'
phone_number = '1888888888'
