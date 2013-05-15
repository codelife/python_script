#!/usr/local/bin/python
#encoding=utf8
import  redis
import  struct
import  sets
redis_host="localhost"
#包含vip包月服务的礼包id或物品ID
vip_gift=set([36001,36002,36003,36014,36015,36017])
con_redis=redis.StrictRedis(host=redis_host, port=6379, db=0)
#
for Buylist_id in con_redis.keys('NewAiStoreBuyList_*'):
    id=Buylist_id.split('_')[1]
    print id
    item_set=sets.Set()                      #初始化用户购买过的物品ID号集合
    vip_type=con_redis.hget("Additional_" + id, 'HaveBuyVip')
    if (vip_type == "3"):                    #只处理被认为是赠送vip的用户购买过的物品
        aistore_log=con_redis.lrange("NewAiStoreBuyList_" + id,0,-1)
        for item_log in aistore_log:
            item_str=struct.unpack('<iiiiIii',item_log)
            item_set.add(item_str[0])
        print vip_gift.intersection(item_set)
        if ((len(vip_gift.intersection(item_set)) > 0)):
            con_redis.hset("Additional_" + id, 'HaveBuyVip',1)
    else:
        pass
