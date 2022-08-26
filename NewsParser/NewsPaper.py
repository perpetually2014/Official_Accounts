import re
import dateutil.parser
import time, datetime
from lxml import etree
from lxml.html import HtmlElement

from .extract_config import PUBLISH_TIME_META,DATETIME_PATTERN
from htmldate import find_date


def format_pubtime(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


class TimeParser:
    """
    特殊时间 通过url正则抽取
    # http://www.zhongguotongcuhui.org.cn/hnwtchdt/202203/t20220315_12419414.html
    """
    def __init__(self,*args,**kwargs):
        self.time_pattern = DATETIME_PATTERN
        self.PUBLISH_TIME_META =PUBLISH_TIME_META

    def format_pubtime(self,timeStamp):
        try:
            timeStamp = int(timeStamp)
        except:
            return None
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    def url_to_timestamp(self,url=None,**kwargs):
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
                now=self.format_pubtime(now)
                return now
        except:
            return None

    def extract_from_meta(self, element: HtmlElement) -> str:
        """
        一些很规范的新闻网站，会把新闻的发布时间放在 META 中，因此应该优先检查 META 数据
        :param element: 网页源代码对应的Dom 树
        :return: str
        """
        for xpath in self.PUBLISH_TIME_META:
            publish_time = element.xpath(xpath)
            if publish_time:
                return ''.join(publish_time)
        return None

    def extract_from_text(self, element: HtmlElement) -> str:
        text = ''.join(element.xpath('.//text()'))
        for dt in self.time_pattern:
            dt_obj = re.search(dt, text)
            if dt_obj:
                return dt_obj.group(1)
        else:
            return None

    def str_to_timestamp(self,date):
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

    def extractor(self, element: HtmlElement) -> str:
        publish_time = (self.extract_from_meta(element)  # 第二优先级从 Meta 中提取
                        or self.extract_from_text(element))  # 最坏的情况从正文中提取
        return publish_time

    def parse_date(self,**kwargs):
        Is_correct = False
        html = kwargs["html"]
        url = kwargs["url"]
        element = etree.HTML(html)
        pub_t = self.extract_from_meta(element)
        if pub_t:
            date_t = self.format_pubtime(self.str_to_timestamp(pub_t))
            if date_t:
                Is_correct = True
                return date_t
        if not  Is_correct:
            date_t = find_date(html,url=url, outputformat='%Y-%m-%d %H:%M:%S')
            if date_t:
                Is_correct = True
                return date_t
        if not Is_correct:
            date_t = self.url_to_timestamp(url=url)
            if date_t:
                Is_correct = True
                return date_t
        if not Is_correct:
            str_to_timestamp = self.str_to_timestamp(html)
            if str_to_timestamp:
                date_t = self.format_pubtime(str_to_timestamp)
                if date_t:
                    Is_correct = True
                    return date_t
        if not Is_correct:
            return None

    def parse_time(self,**kwargs):
        detail_time = self.parse_date(**kwargs)
        if isinstance(detail_time, int):
            detail_time = format_pubtime(detail_time)
        if not detail_time:
            detail_time = format_pubtime(int(time.time()))
        if "00:00:00" in detail_time:
            timeArray = time.localtime(int(time.time()))
            otherStyleTime = time.strftime("%H:%M:%S", timeArray)
            detail_time = detail_time.split(" ")[0]+" "+otherStyleTime
        return detail_time


class TitleParser:
    pass

if __name__ == '__main__':
    data_time = TimeParser().parse_time(html=
        "4月6日抽查内容主要包括防汛“三个责任人”上岗到位、汛期巡查工作开展、雨水工情信息报送，泄洪设施是否正常、泄洪通道是否通畅等。从抽查情况看，绝大部分水库（水电站）防汛值班及带班人员都坚守岗位，及时接听电话，比较了解近期天气变化、出入库流量、水位等特征值，履职尽责情况良好。但也存在少数巡查责任人基本情况了解不够、业务水平和专业技能有待提高，部分水库尚未开展防汛应急演练等。对电话抽查中发现的问题，要求立即整改落实。",url="http://slt.qinghai.gov.cn/articles/detail?id=1532970083784069120")
    print(data_time)
