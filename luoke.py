#!/usr/bin/python
# encoding=utf-8
import socket
import re
import struct
import subprocess
import MySQLdb as mdb
import time
import sys
# dir 最大编号
global max_dir
max_dir = 2617


def query(start, stop):
    remote_host = '192.168.1.1'
    remote_port = 443
    len = 2502361088  # 95270000
    null1 = 0
    unknow_id = 458755  # 00070003
    account = 445450639  # 1a8d098f
    null2 = 4
    query_str = struct.pack(
        '>Liiiihh',
        len,
        unknow_id,
        account,
        null1,
        null2,
        start,
        stop)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((remote_host, remote_port))
    sock.send(query_str)
    sock.settimeout(2)
    try:
        response_data = sock.recv(8192)
    except:
        pass
    if start != max_dir:
        x = struct.unpack('>8i3h3i2h3i2h3i2h3i2h3i2h3i2h3i2h2i', response_data)
        i = 10
        sum = 0
        while i <= 45:
            sum += x[i]
            i += 5
        return sum
    else:
        x = struct.unpack('>8i3h3i2h3i2h3i2h2i', response_data)
        i = 10
        sum = 0
        while i <= 25:
            sum += x[i]
            i += 5
        return sum


def insert_online(database, table, count):
    try:
        conn = mdb.connect(host='192.168.100.3', user='root', db=database)
        cur = conn.cursor()
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        ret = cur.execute(
            "insert into %s (online_num,create_time) values (%d,'%s')" %
            (table, count, create_time))
        print "insert into %s (online_num,create_time) values (%d,'%s')" % (table, count, create_time)
        return ret
        conn.close()
    except:
        print "exception output............."
        return 1

if __name__ == '__main__':
    start = 1
    stop = 8
    online_sum = 0
    print "start querying ...."
    while start <= max_dir:
        try:
            # print start,stop,online_sum
            online_sum += query(start, stop)
            start += 8
        except Exception as e:
            print time.ctime()
            print e
            continue
    insert_online("stat", "luoke", online_sum)
