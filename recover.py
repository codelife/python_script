#!/usr/bin/python
#encoding=utf8
import  redis
import struct
redis_host="113.196.60.9"
con_redis=redis.StrictRedis(host=redis_host, port=6379, db=0)
#所有人的星点消费记录清零
for addtional_key in con_redis.keys('Additional_*'):
    con_redis.hset(addtional_key,'StarPntCunsume' ,0)

for Buylist_id in con_redis.keys('NewAiStoreBuyList_*'):
    id=Buylist_id.split('_')[1]
    aistore_log=con_redis.lrange(Buylist_id,0,-1)
    consum_starpoint=0
    for item in aistore_log:
        paid=struct.unpack('<iiiiIii',item)
        if paid[2]==1:
            consum_starpoint+=paid[3]
    con_redis.hset('Additional_'+id,'StarPntCunsume' ,consum_starpoint)
for addtional_key in con_redis.keys('Additional_*'):
   print  con_redis.hget(addtional_key,'StarPntCunsume')
