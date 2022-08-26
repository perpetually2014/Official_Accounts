# -*- coding: utf-8 -*-
import time
import re
import sys
import datetime
import dateutil.parser
from dateutil import parser as date_parser
import gzip

def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def str_to_timestamp(date):
    dt = datetime.datetime.now()
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    now = int(time.time())
    isParse = False
    m = None
    if not isParse:
        m = re.search(u'(\d+)\s*秒前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))
    if not isParse:
        m = re.search(u'(\d+)\s*分钟前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60
    if not isParse:
        m = re.search(u'(\d+)\s*小时前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60
    if not isParse:
        m = re.search(u'(\d+)\s*天前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60*24
    if not isParse:
        m = re.search(u'(\d+)\s*个月前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60*24*30
    if not isParse:
        m = re.search(u'今天\s*(\d+):(\d+)', date, re.M|re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                hour = m.group(1)
            if m.group(2):
                minute = m.group(2)
            s = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
            d =  date_parser.parse(s,fuzzy=True)
            now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search( u'(\d{2,4})?年?(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:时]?(\d{1,2})?[:分]?(\d{1,2})?', date, re.M|re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                tmp_year = m.group(1)
                if len(str(tmp_year))==2:
                    tmp_year = int("20" + tmp_year)
                tmp_year=int(tmp_year)
                if  1970  <tmp_year <= int(year):
                    year = tmp_year
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
            s = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
            # print(s)
            try:
                d =  dateutil.parser.parse(s,fuzzy=True)
                now = int(time.mktime(d.timetuple()))
            except:
                pass
            # now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search( r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})', date, re.M|re.I)
        if m:
            isParse = True
            date = m.group()
            d =  date_parser.parse(date,fuzzy=True)
            t = int(time.mktime(d.timetuple()))
            if t < now:
                now = t

    if not isParse:
        try:
            m = date.split('·')[0]+" " + "00-00-00"
            d = dateutil.parser.parse(m, fuzzy=True)
            now = int(time.mktime(d.timetuple()))

        except:
            pass
    if not isParse:
        m = re.search(r'(\d{4})-(\d{2})-(\d{2})', date, re.M|re.I)
        if m:
            isParse =True
            year = m.group(1)
            month = m.group(2)
            day = m.group(3)
            s = str(year) + "-" + str(month) + "-" + str(day)
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))

    return now
def replace_by_img_tag(txt):
    begin = 0 
    end = 0 
    i = 1 
    while True:
        end = txt.find('{img}', begin)
        if end == -1: 
            break
        new = '\n{IMG:'+str(i)+'}\n'
        txt = txt.replace('{img}', new, 1)
        begin = end + len(new)
        i = i + 1 
    return txt

def replace_by_video_tag(txt):
    begin = 0
    end = 0
    i = 1
    while True:
        end = txt.find('{video}', begin)
        if end == -1:
            break
        new = '\n{VIDEO:'+str(i)+'}\n'
        txt = txt.replace('{video}', new, 1)
        begin = end + len(new)
        i = i + 1
    return txt

#print str_to_timestamp('2018-08-29T05:09:00Z')
def str2int(s):
    #s = 13.4w
    s=s.strip()
    if len(s) == 0:
        return 0
    i = 0 
    pos = s.find('w')
    if pos != -1: 
        i = int( float(s[0:pos])*10000 )
    else:
        i = int(s)
    return i



def get_real_time(pubtime_re,pubtime_gne):
    """
    根据全文正则匹配的时间与gne抽取的时间作对比，取出更合理的时间
    :param pubtime_re:
    :param pubtime_gne:
    :return:
    """
    #print(f"pubtime_re:{pubtime_re}pubtime_gne:{pubtime_gne}")

    rtimearr = time.localtime(pubtime_re)
    r_hour = rtimearr.tm_hour
    r_min = rtimearr.tm_min

    gtimearr = time.localtime(pubtime_gne)
    g_hour = gtimearr.tm_hour
    g_min = gtimearr.tm_min

    if g_hour!=0 or g_min!=0:
        return pubtime_gne
    elif r_hour!=0 or  r_min!=0 :
        return pubtime_re
    else:
        return  int(time.time())

