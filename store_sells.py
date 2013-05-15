#!/usr/bin/python
#coding:gb2312
import redis
import time
import lxml.etree
redis_conn = redis.StrictRedis(host="192.168.1.47", port=6379, db=0)


def time_list(time_start=None, time_stop=None, format="%Y%m%d"):
    """
        return a date list like 20130410 from time_start to time_stop(
    default is now)
    """
    from datetime import date
    time_list = []
    if time_start is None:
        time_start = time.mktime(time.localtime())
    else:
        time_start = time.mktime(date(*time_start).timetuple())
    if time_stop is None:
        time_stop = time.mktime(time.localtime())
    else:
        time_stop = time.mktime(date(*time_stop).timetuple())
    time_delta = int((time_stop - time_start) / 86400)
    if time_delta < 0:
        raise Exception("Time range is out expect from" + str(time.ctime(
            time_start)) + " to " + str(time.ctime(time_stop)))
    for i in range(1, time_delta + 1):
        time_list.append(time.strftime(format, time.gmtime(
            time_start + 86400 * i)))
    return time_list

time_range = time_list((2013, 04, 10))
sells_summery = {}
item_array = {}
xml_doc = lxml.etree.parse('/usr/local/kor/config/staticData/aiStore.xml')
for node in xml_doc.xpath("//aiStore/Kind/Type/Commodity"):
    item_array[node.get('ID')] = [node.get('Name'),  node.get("StarPoint")]

for sells_date in time_range:
    sells_record = redis_conn.hgetall("CmdtySellNumStat_" + sells_date)
    for record_key in sells_record.keys():
        if record_key in sells_summery:
            sells_summery[record_key] += int(sells_record[record_key])
        else:
            sells_summery[record_key] = int(sells_record[record_key])

import codecs
fd = codecs.open("log.csv", 'a', 'gb2312')
for id in sells_summery.keys():
    fd.write(id + ',' + item_array[id][0] + ',' + str(sells_summery[id]) + ','
             + str(sells_summery[id] * int(item_array[id][1])) + '\n')
