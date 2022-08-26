import re
import dateutil.parser
import time, datetime
from lxml import etree
from lxml.html import HtmlElement

from ..extract_config import PUBLISH_TIME_META,DATETIME_PATTERN
from htmldate import find_date


class TimeExtractor:
    """
    特殊时间 通过url正则抽取
    # http://www.zhongguotongcuhui.org.cn/hnwtchdt/202203/t20220315_12419414.html
    """

    time_pattern = DATETIME_PATTERN
    PUBLISH_TIME_META =PUBLISH_TIME_META

    @classmethod
    def format_pubtime(cls,timeStamp):
        try:
            timeStamp = int(timeStamp)
        except:
            return None
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime
    @classmethod
    def url_to_timestamp(cls,url=None,**kwargs):
        if not url:
            return None
        try:
            dt = datetime.datetime.now()
            year = dt.year
            month = dt.month
            day = dt.day
            hour = dt.hour
            minute = dt.minute
            second = dt.second
            now1 = int(time.time())
            now = int(time.time())
            isParse = False
            m = None

            if not isParse:
                m = re.search('/(\d{2,4})/(\d{1,2})/(\d{1,2})', url, re.M | re.I)
                if m:
                    isParse = True

                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)
                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    d = dateutil.parser.parse(s, fuzzy=True)
                    now = int(time.mktime(d.timetuple()))

            if not isParse:
                m = re.search('/(\d{4})/(\d{1,2})-(\d{1,2})/', url, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)
                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    d = dateutil.parser.parse(s, fuzzy=True)
                    now = int(time.mktime(d.timetuple()))

            if not isParse:
                m = re.search('/(\d{2,4})-(\d{1,2})/(\d{1,2})/', url, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)
                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    d = dateutil.parser.parse(s, fuzzy=True)
                    now = int(time.mktime(d.timetuple()))

            if not isParse:
                m = re.search('/(\d{6})/(\d{2})/', url, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)[:4]
                        month = m.group(1)[-2:]
                        if m.group(2):
                            day = m.group(2)
                        hour = "00"
                        minute = "00"
                        second = "00"
                        s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))

            if not isParse:
                m = re.search('/(\d{8})/', url, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)[:4]
                        month = m.group(1)[5:6]
                        day = m.group(1)[-2:]
                        hour = "00"
                        minute = "00"
                        second = "00"
                        s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))

            if not isParse:
                m = re.search('(\d{2,4})-(\d{1,2})-(\d{1,2})', url, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)
                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    d = dateutil.parser.parse(s, fuzzy=True)
                    now = int(time.mktime(d.timetuple()))

            if not isParse:
                m = re.search('(\d{6})/(\d{2})', url, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)
                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    d = dateutil.parser.parse(s, fuzzy=True)
                    now = int(time.mktime(d.timetuple()))

            if not isParse:
                m = re.search('(\d{2,4})?-(\d{1,2})-(\d{1,2})', url, re.M | re.I)
                if m:
                    isParse = True

                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)

                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    d = dateutil.parser.parse(s, fuzzy=True)
                    now = int(time.mktime(d.timetuple()))
            if not isParse:
                return None
            else:
                if now1 <= now:
                    return None
                now=cls.format_pubtime(now)
                return now
        except:
            return None

    @classmethod
    def extract_from_meta(cls, element: HtmlElement) -> str:
        """
        一些很规范的新闻网站，会把新闻的发布时间放在 META 中，因此应该优先检查 META 数据
        :param element: 网页源代码对应的Dom 树
        :return: str
        """
        for xpath in cls.PUBLISH_TIME_META:
            publish_time = element.xpath(xpath)
            if publish_time:
                return ''.join(publish_time)
        return None

    @classmethod
    def extract_from_text(cls, element: HtmlElement) -> str:
        text = ''.join(element.xpath('.//text()'))
        for dt in cls.time_pattern:
            dt_obj = re.search(dt, text)
            if dt_obj:
                return dt_obj.group(1)
        else:
            return None

    @classmethod
    def str_to_timestamp(cls,date:str):
        try:
            dt = datetime.datetime.now()
            year = dt.year
            month = dt.month
            day = dt.day
            hour = dt.hour
            minute = dt.minute
            second = dt.second
            now1 = int(time.time())
            now = int(time.time())
            isParse = False
            # if not "前" in date:
            #    isParse=True
            m = None
            if not isParse:
                m = re.search('(\d+)\s*秒之*前', date, re.M | re.I)
                if m:
                    isParse = True
                    now = now - int(m.group(1))
            if not isParse:
                m = re.search('(\d+)\s*分钟之*前', date, re.M | re.I)
                if m:
                    isParse = True
                    now = now - int(m.group(1)) * 60
            if not isParse:
                m = re.search('(\d+)\s*小时之*前', date, re.M | re.I)
                if m:
                    isParse = True
                    now = now - int(m.group(1)) * 60 * 60
            if not isParse:
                m = re.search('(\d+)\s*天之*前', date, re.M | re.I)
                if m:
                    isParse = True
                    now = now - int(m.group(1)) * 60 * 60 * 24
            if not isParse:
                m = re.search('(\d+)\s*个月之*前', date, re.M | re.I)
                if m:
                    isParse = True
                    now = now - int(m.group(1)) * 60 * 60 * 24 * 30

            if not isParse:
                m = re.search('昨天', date, re.M | re.I)
                if m:
                    isParse = True
                    day_time = int(time.mktime(datetime.date.today().timetuple()))
                    now = day_time - 60 * 60 * 24

            if not isParse:
                m = re.search('今天\s*(\d+):(\d+)', date, re.M | re.I)
                if m:
                    isParse = True
                    hour = 0
                    minute = 0
                    second = 0
                    if m.group(1):
                        hour = m.group(1)
                    if m.group(2):
                        minute = m.group(2)
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(
                        second)
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False
            if not isParse:
                m = re.search('(\d{2,4})?年?(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:时]?(\d{1,2})?[:分]?(\d{1,2})?', date,
                              re.M | re.I)
                if m:
                    isParse = True
                    hour = 0
                    minute = 0
                    second = 0
                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)
                    if m.group(4):
                        hour = m.group(4)
                    if m.group(5):
                        minute = m.group(5)
                    if m.group(6):
                        second = m.group(6)
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(
                        second)
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False

            if not isParse:
                m = re.search('(\d{2,4})?年?(\d{1,2})月(\d{1,2})日', date, re.M | re.I)
                if m:
                    isParse = True

                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)

                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False

            if not isParse:
                m = re.search('(\d{4})?\.(\d{1,2})\.(\d{1,2})\s*(\d{2}):(\d{2})', date, re.M | re.I)
                if m:
                    isParse = True

                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)

                    if m.group(4):
                        hour = m.group(4)

                    if m.group(5):
                        minute = m.group(5)

                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False

            if not isParse:
                m = re.search('(\d{4})?\.(\d{2})\.(\d{2})', date, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)

                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False

            if not isParse:
                m = re.search('(\d{1,2})-(\d{1,2})\s*(\d{1,2}):(\d{1,2})', date, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        month = m.group(1)
                    if m.group(2):
                        day = m.group(2)
                    if m.group(3):
                        hour = m.group(3)
                    if m.group(4):
                        minute = m.group(4)

                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(
                        minute) + ":" + second
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False

            if not isParse:
                m = re.search('(\d{2,4})?-(\d{1,2})-(\d{1,2})\s*(\d{1,2}):(\d{1,2})', date, re.M | re.I)
                if m:
                    isParse = True
                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(3)
                    if m.group(4):
                        day = m.group(5)
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False

            if not isParse:
                m = re.search('(\d{2,4})?-(\d{1,2})-(\d{1,2})', date, re.M | re.I)
                if m:
                    isParse = True

                    if m.group(1):
                        year = m.group(1)
                        if len(str(year)) == 2:
                            year = "20" + year
                    if m.group(2):
                        month = m.group(2)
                    if m.group(3):
                        day = m.group(3)

                    hour = "00"
                    minute = "00"
                    second = "00"
                    s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
                    try:
                        d = dateutil.parser.parse(s, fuzzy=True)
                        now = int(time.mktime(d.timetuple()))
                    except:
                        isParse = False

            if not isParse:

                m = re.search(
                    r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2}\w\d{1,2}:\d{1,2}:\d{1,2})',
                    date, re.M | re.I)
                if m:
                    isParse = True
                    date = m.group()
                    try:
                        d = dateutil.parser.parse(date, fuzzy=True)
                        t = int(time.mktime(d.timetuple()))
                        if t < now:
                            now = t
                    except:
                        isParse = False
            if not isParse:
                return None
            else:
                if now1 <= now:
                    return None
                return now
        except:
            return None

    @classmethod
    def extractor(cls, element: HtmlElement) -> str:
        publish_time = (cls.extract_from_meta(element)  # 第二优先级从 Meta 中提取
                        or cls.extract_from_text(element))  # 最坏的情况从正文中提取
        return publish_time

    @classmethod
    def parse_date(cls,**kwargs):
        Is_correct = False
        html = kwargs["html"]
        url = kwargs["url"]
        element = etree.HTML(html)
        pub_t = cls.extract_from_meta(element)
        if pub_t:
            date_t = cls.format_pubtime(cls.str_to_timestamp(pub_t))
            if date_t:
                Is_correct = True
                return date_t
        if not  Is_correct:
            date_t = find_date(html,url=url, outputformat='%Y-%m-%d %H:%M:%S')
            if date_t:
                Is_correct = True
                return date_t
        if not Is_correct:
            date_t = cls.url_to_timestamp(url=url)
            if date_t:
                Is_correct = True
                return date_t
        if not Is_correct:
            str_to_timestamp = cls.str_to_timestamp(html)
            if str_to_timestamp:
                date_t = cls.format_pubtime(str_to_timestamp)
                if date_t:
                    Is_correct = True
                    return date_t
        if not Is_correct:
            return None

    # 调用方法
    @classmethod
    def parse_time(cls,**kwargs):
        detail_time = cls.parse_date(**kwargs)
        if isinstance(detail_time, int):
            detail_time = cls.format_pubtime(detail_time)
        if not detail_time:
            detail_time = cls.format_pubtime(int(time.time()))
        if "00:00:00" in detail_time:
            timeArray = time.localtime(int(time.time()))
            otherStyleTime = time.strftime("%H:%M:%S", timeArray)
            detail_time = detail_time.split(" ")[0]+" "+otherStyleTime
        return detail_time


if __name__ == '__main__':
    pass
