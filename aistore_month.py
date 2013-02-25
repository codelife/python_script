#!/usr/bin/python                                                                                                              
#encoding=utf8
import redis
import sys
from datetime import datetime
redis_host = "192.168.1.250"
year  =  datetime.now().year  
last_month =  datetime.now().month  - 1 
last_month = str(last_month).zfill(2)
print year,last_month
#get all selled item id
item_set=set()
redis_con=redis.Redis(redis_host,6379,0)
for day  in range(1,32):
    key = "CmdtySellStarPntStat_" + str(year) + last_month + str(day).zfill(2)   
    item_set.update(set(redis_con.hkeys(key)))
print item_set
star_point = {}
item_count = {}
man_count = {}
for item_id in item_set :
    star_point[item_id] = 0 
    item_count[item_id] = 0 
    man_count[item_id] = 0
    for day  in range(1,32):
        key_star = "CmdtySellStarPntStat_" + str(year) + last_month + str(day).zfill(2)   
        key_count = "CmdtySellNumStat_" + str(year) + last_month + str(day).zfill(2)      
        key_man = "CmdtySellManTimeStat_" + str(year) + last_month + str(day).zfill(2)      
        star = 0 if redis_con.hget(key_star,item_id) is None else redis_con.hget(key_star,item_id) 
        count = 0 if redis_con.hget(key_count,item_id) is None else redis_con.hget(key_count,item_id) 
        man = 0 if redis_con.hget(key_man,item_id) is None else redis_con.hget(key_man,item_id) 
        star_point[item_id]   += int(star)
        item_count[item_id]   += int(count)
        man_count[item_id]   += int(man)
item_name={
1 : '爆电铁拳',
2 : '毁灭者',
2001 : '凌光',
2002 : '沙漠蝎',
2003 : '玲珑',
4001 : '罗兰鲨',
6001 : '影刃前翼',
12001 : '影刃中翼',
18001 : '影刃尾翼',
24001 : '影刃车轮',
30001 : '凌光头盔',
30002 : '黑炎头盔',
30003 : '水晶流星头盔',
30004 : '爆电铁拳头盔',
30005 : '闪光利爪头盔',
30006 : '致命獠牙头盔',
30007 : '烈焰红唇头盔',
30008 : '雄鹰守护头盔',
30009 : '罗兰鲨头盔',
30010 : '沙漠蝎头盔',
30011 : '玲珑头盔',
30012 : '毁灭者头盔',
36001 : '超级AI-1个月',
36002 : '超级AI-3个月',
36003 : '超级AI-6个月',
36004 : '胜利翻牌器',
36005 : '紧急修理器',
36006 : 'Boss挑战卡',
36007 : 'AI扩散子弹包',
36008 : '强化宝石袋',
36009 : '深渊宝藏',
36010 : '凌光芯片',
36011 : '罗兰鲨芯片',
36012 : '毁灭者芯片',
36013 : '毁灭者礼包',
36014 : '成长礼包',
36015 : '进阶礼包',
36016 : '材料优惠包',
44001 : '强化宝石',
44002 : '幸运宝石',
44003 : '动力结晶',
50001 : '马力拉特-15天',
50002 : '印加拉特-15天',
50003 : '维京拉特-15天',
50004 : 'Boss挑战卡',
50005 : '胜利翻牌器',
50006 : '翻牌器优惠包',
50007 : '紧急修理器',
50008 : '幸运宝石',
50009 : '动力结晶',
50010 : '瞬移',
50011 : '爱心',
51001 : '响尾蛇头盔',
51002 : '轰天暴龙头盔',
51003 : '煞星头盔',
51004 : '火赤炼头盔',
52001 : '响尾蛇前翼',
52002 : '响尾蛇中翼',
52003 : '响尾蛇尾翼',
52004 : '响尾蛇车轮',
52005 : '响尾蛇车体',
52006 : '煞星前翼',
52007 : '煞星中翼',
52008 : '煞星尾翼',
52009 : '煞星车轮',
52010 : '煞星车体',
}
print len(item_set)
print item_name[1]
for item_id in item_set:
    print "%-10s%-45s%-20s%10s%10s"  % (item_id,item_name[int(item_id)],item_count[item_id],star_point[item_id],man_count[item_id])
