import os
import time
from itertools import chain
import pymysql
import logger
import config

log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/news%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('news', log_path)

class GetJdStore:
    def __init__(self):
        # 打开数据库连接
        self.db = pymysql.connect(
            host=config.host,
            port=config.port,
            user=config.user,
            passwd=config.passwd,
            database=config.database,
            charset=config.charset
        )

    def wechat_news(self, item):
        site_id = item['site_id']
        level = item['level']
        site_name = item['site_name']
        type = item['type']
        url = item['url']
        title = item['title']
        source = item['source']
        content = item['content']
        publish_time = item['publish_time']
        images = str(item['images'])
        data_id = item['data_id']
        body_html = item['body_html']

        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # for db in ['anji_news','wechat_news']:
        sql = "INSERT INTO {}(site_id, level, site_name, type, url,title,source,content,publish_time,images,data_id,body_html) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY " \
              "UPDATE body_html = VALUES(body_html), update_time = CURRENT_TIMESTAMP ".format('wechat_news')
        try:
            # 执行sql语句
            cursor.execute(sql, [site_id, level, site_name, type, url, title, source, content, publish_time, images,
                                 data_id, body_html])

            # 提交到数据库执行
            self.db.commit()
            # logging.info("时间:{},写入成功,标题为:{}".format(publish_time, title))
        except Exception as e:
            # 如果发生错误则回滚
            logging.info("写入失败，数据回滚{},{}".format(e, url))
            self.db.rollback()
        finally:
            # 关闭数据库连接
            self.db.close()

    # 微信账号
    def wechat_source(self, item):
        fakeid = item['fakeid']
        name = item['name']
        type = item['type']
        site_id = item['site_id']
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句

        sql = "INSERT INTO wechat_source(fakeid,name,type,site_id) VALUES (%s,%s,%s,%s)ON DUPLICATE KEY " \
              "UPDATE name = VALUES(name), update_time = CURRENT_TIMESTAMP "
        try:
            # 执行sql语句
            cursor.execute(sql, [fakeid, name, type, site_id])
            # 提交到数据库执行
            self.db.commit()
            logging.info("微信账号写入成功,标题为:{}".format(name))

        except Exception as e:
            # 如果发生错误则回滚
            logging.info("写入失败，数据回滚{}".format(e))
            self.db.rollback()
        finally:
            # 关闭数据库连接
            self.db.close()

    # 搜索
    def get_search(self):
        cur = self.db.cursor()
        # 1.查询操作(按时间查找，今天的)
        sql = "select name,fakeid,site_id from wechat_source  where is_update =1 ORDER BY spider_time  ASC"
        # sql = "select name,fakeid,site_id from wechat_source  where is_update =1"
        try:
            cur.execute(sql)  # 执行sql语句
            results = cur.fetchall()  # 获取查询的所有记录
            resultlist = list(chain.from_iterable(results))
            return resultlist
        except Exception as e:
            logging.info("查询错误{}".format(e))
            raise e
        finally:
            self.db.close()  # 关闭连接

    # 更新数量
    def spider_time(self, item):
        # 使用cursor()方法获取操作游标
        fakeid = item['fakeid']
        count = item['count']
        spider_time = item['spider_time']
        cursor = self.db.cursor()
        sql = "INSERT INTO wechat_source(fakeid,count,spider_time) VALUES (%s,%s,%s)ON DUPLICATE KEY " \
              "UPDATE count = VALUES(count), spider_time = VALUES(spider_time), update_time = CURRENT_TIMESTAMP "
        try:
            # 执行sql语句
            cursor.execute(sql, [fakeid, count, spider_time])
            # 提交到数据库执行
            self.db.commit()
            logging.info("开启采集,账号为:{}".format(fakeid))

        except Exception as e:
            # 如果发生错误则回滚
            logging.info("写入失败，数据回滚{}".format(e))
            self.db.rollback()
        finally:
            # 关闭数据库连接
            self.db.close()


if __name__ == '__main__':
    pass
