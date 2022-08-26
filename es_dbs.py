# -*-coding:utf-8-*-
import elasticsearch
import config
import urllib3,os,time
import logger

urllib3.disable_warnings()
log_path = os.path.abspath(os.path.dirname(__file__)) + '/log/tencent%s.log' % time.strftime('%Y%m%d')
logging = logger.log_conf('tencent', log_path)

def parse(item):
    es_url = config.es_hosts
    index = config.es_index
    data = {}
    data['site_id'] = item['site_id']
    data['level'] = item['level']
    data['site_name'] = item['site_name']
    data['type'] = item['type']
    data['url'] = item['url']
    data['title'] = item['title']
    data['source'] = item['source']
    data['content'] = item['content']
    data['publish_time'] = item['publish_time']
    data['images'] = item['images']
    data['data_id'] = item['data_id']
    data['body_html'] = item['body_html']
    data['html'] = item['html']
    data['health_score'] = item['health_score']
    data['health_tag'] = item['health_tag']
    data['province'] = item['province']
    data['content_length'] = item['content_length']
    data['gather_time'] = item['gather_time']
    id = item['data_id']

    # Es数据入库
    try:
        es = elasticsearch.Elasticsearch(es_url, sniff_on_start=True, sniff_on_connection_fail=True, timeout=60)
        es.index(index=index, id=id, doc_type="_doc", body=data)
        print('ES写入成功:{},标题:{}'.format(data['publish_time'],data['title']))
    except Exception as e:
        logging.error('写入ES失败:{}'.format(e))


if __name__ == '__main__':
    pass
