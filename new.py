#!/usr/bin/python
#encoding=utf8
import  redis
#redis_host="113.196.60.9"
redis_host="localhost"
con_redis=redis.StrictRedis(host=redis_host, port=6379, db=0)
#所有人的星点消费记录清零
for addtional_key in con_redis.keys('Additional_*'):
    id = addtional_key.split('_')[1] 
    count =  con_redis.hget(addtional_key,'PurifyCarCnt120712')
    if count is not None:
        print "id:%s" %id
        print "count:%s" %count
    if count  == "1":
        con_redis.incr('Coins_'+ id , -5000)
        con_redis.hincrby(addtional_key,'StarPoints',80)
    if count  == "2":
        con_redis.incr('Coins_'+ id , -5000)
        con_redis.hincrby(addtional_key,'StarPoints',380)
    if count  == "3":
        con_redis.incr('Coins_'+ id , -5000)
        con_redis.hincrby(addtional_key,'StarPoints',760)
        print "done" 
    if count  == "4":
        con_redis.incr('Coins_'+ id , -5000)
        con_redis.hincrby(addtional_key,'StarPoints',760)
    if count  == "5":
        con_redis.incr('Coins_'+ id , -5000)
        con_redis.hincrby(addtional_key,'StarPoints',760)
    if count  == "6":
        con_redis.incr('Coins_'+ id , -5000)
        con_redis.hincrby(addtional_key,'StarPoints',760)                       
