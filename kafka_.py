# -*-coding:utf-8-*-
import os
import time
from kafka import KafkaProducer
import logger
import config
import json
log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/news%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('news', log_path)
# producer = KafkaProducer(bootstrap_servers=config.SERVER)
producer = KafkaProducer(bootstrap_servers=config.SERVER, compression_type='gzip')
topic = config.TOPIC
topic2 = config.TOPIC2

def kafka(content):
    try:
        f = producer.send(topic, value=json.dumps(content, ensure_ascii=False).encode('utf-8'))
        f.get(timeout=100)

        print('kafka写入成功：{}'.format(content['title']))
        images = {}
        images['images'] = img = content['images']
        images['url'] = content['url']
        images['gather_time'] = content['gather_time']

        if len(img) > 0:
            f2 = producer.send(topic2, value=json.dumps(images, ensure_ascii=False).encode('utf-8'))
            f2.get(timeout=10)
            # print('图片写入kafka成功：{},'.format(len(img)))
        # else:
        #     print('img为空：{}'.format(img))

    except Exception as e:
        logging.info('写入失败，数据回滚：{}'.format(e))


if __name__ == '__main__':
    kafka()
