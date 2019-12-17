# -*- encoding:utf-8 -*-
from flask import Flask, request, g
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
#import config.config as config
import dist.acd_74_p.config.config as config
#from app.knowledgeBase import app as knowledgeBase
from dist.acd_74_p.app.knowledgeBase import app as knowledgeBase
from dist.acd_74_p.app.situationAnalysis import app as situationAnalysis
from dist.acd_74_p.app.fileUpload import app as fileUpload
# from dist.acd_74_p.app.situationAnalysis import histogramChartData

from multiprocessing import Process
import threading
import time
from threading import Thread
import  datetime
import traceback
import json
import calendar
import redis
import re
import logging

app = Flask(__name__)
app.register_blueprint(situationAnalysis)
app.register_blueprint(knowledgeBase)
app.register_blueprint(fileUpload)

conn = connect(**config.DatabaseConfig.siem)
cursor = conn.cursor(cursor_factory=RealDictCursor)
cursor.execute("select * from ip2latlon")
allLocaltionInfo = cursor.fetchall()
locationMapping = {}
for locationInfo in allLocaltionInfo:
    locationMapping[locationInfo["country_name"]] = locationInfo["pngs"]
    locationMapping[locationInfo["country_name_cn"]] = locationInfo["pngs"]
cursor.close()

@app.before_request
def setupdb():
    g.conn_data = connect(**config.DatabaseConfig.siem)
    g.cursor_data = g.conn_data.cursor(cursor_factory=RealDictCursor)


@app.teardown_request
def unsetdb(exception):
    if g.cursor_data:
        g.cursor_data.close()
        g.cursor_data = None
    if g.conn_data:
        g.conn_data.close()
        g.conn_data = None


@app.errorhandler(404)
def err_notfound(ex):
    if request.is_xhr:
        return ('{"error":true, "msg":"请求的资源不存在"}', 404)
    else:
        return ("""<!DOCTYPE html>
                <html><head>
                    <meta charset="utf-8">
                    <title> 404  </title>
                </head><body>
                    <div style="text-align:center;
                                font-size:12em; color:#AAA;">404</div>
                    <hr style="width:80%;" />
                    <div style="text-align:center;
                                font-size:2em; color:#AAA;">
                                     Sorry!请求的资源不存在。</div>
                </body></html>""", 404)


@app.errorhandler(500)
def err_exception(ex):
    if request.is_xhr:
        return ('{"error":true, "msg":"服务器内部出现异常"}', 500)
    else:
        return ("""<!DOCTYPE html>
                <html><head>
                    <meta charset="utf-8">
                    <title> 500  </title>
                </head>
                <body>
                    <div style="text-align:center;
                                font-size:12em; color:#AAA;">500</div>
                    <hr style="width:80%;" />
                    <div style="text-align:center;
                                font-size:2em; color:#AAA;">
                                     Sorry!服务器内部出现异常</div>
                </body></html>""", 500)
def locationTransition(location):
    try:
        if(location == "" or location == None):
            return location
        location = re.sub(u'(\"+)', u'', location)
        return location.strip().upper()
    except Exception as e:
        return location.strip().upper()

def histogramChartData(timeSlot="day"):
    rule = ""
    beginTime = datetime.datetime.now()
    endTime = None
    histogramData = []
    histogramXData = []
    beginTimeSql = ""
    endTimeSql = ""
    whereSql = ""
    if (timeSlot == "realTime"):
        rule = "mi"
        beginTime = datetime.datetime.now()
        endTime = beginTime - datetime.timedelta(minutes=int(14))
        beginTimeSql = (datetime.datetime.now()+datetime.timedelta(minutes=int(1))).strftime('%Y-%m-%d %H:%M:00')
        endTimeSql = endTime.strftime('%Y-%m-%d %H:%M:00')
        minute = int(endTime.minute)
        for i in range(15):
            histogramXData.append(minute % 60)
            minute += 1
            histogramData.append(0)
            i = i  #  无用，阻止警告
        whereSql = "r_time >= '%s' and  r_time < '%s'" %(endTimeSql,beginTimeSql)
    if(timeSlot == "day"):
        rule = "HH24"
        beginTime = beginTime + datetime.timedelta(hours=int(1))
        endTime = beginTime - datetime.timedelta(1)
        beginTimeSql = beginTime.strftime('%Y-%m-%d %H'+':00:00') 
        endTimeSql = endTime.strftime('%Y-%m-%d %H'+':00:00')
        whereSql = "r_time >= '%s' and  r_time < '%s'" %(endTimeSql,beginTimeSql)
        nowHour = beginTime.strftime('%H')
        computerNowHour = abs(int(nowHour))
        for i in range(24):
            histogramXData.append(computerNowHour % 24 )
            computerNowHour += 1
            histogramData.append(0)
            i = i  #  无用，阻止警告
    elif(timeSlot == "week"):
        rule = "dd"
        beginTime = datetime.datetime.now() + datetime.timedelta(1)
        endTime = beginTime - datetime.timedelta(7)
        monthRange = calendar.mdays[int(endTime.strftime('%m'))]
        beginTimeSql = beginTime.strftime('%Y-%m-%d 00:00:00')
        endTimeSql = endTime.strftime('%Y-%m-%d 00:00:00')
        whereSql = "r_time >= '%s' and  r_time < '%s'" %(endTimeSql,beginTimeSql)
        yesterday = int(endTime.strftime('%d'))
        for i in range(7):
            histogramXData.append(yesterday % monthRange if yesterday % monthRange != 0 else monthRange )
            yesterday += 1
            histogramData.append(0)
    elif(timeSlot == "month"):
        rule = "dd"
        beginTime = datetime.datetime.now() + datetime.timedelta(1)
        monthRange = calendar.mdays[int(beginTime.strftime('%m'))-1]
        endTime = beginTime - datetime.timedelta(1) - datetime.timedelta(monthRange-1)
        beginTimeSql = beginTime.strftime('%Y-%m-%d 00:00:00')
        endTimeSql = endTime.strftime('%Y-%m-%d 00:00:00')
        whereSql = "r_time >= '%s' and  r_time < '%s'" %(endTimeSql,beginTimeSql)
        yesterday = int(endTime.strftime('%d'))
        for i in range(monthRange):
            histogramXData.append(yesterday % monthRange if yesterday % monthRange != 0 else monthRange )
            yesterday += 1
            histogramData.append(0)
    else:
        rule = "MM"
        nowYear = (beginTime.year + 1) if (beginTime.month + 1) / 13 >= 1 else beginTime.year
        nowMouth = 1 if (beginTime.month + 1) / 13 >= 1 else beginTime.month
        beginTimeSql = beginTime.strftime(str(nowYear) + '-'+ str(nowMouth + 1) +'-01 00:00:00')
        endTimeSql = beginTime.strftime(str(nowYear - 1) + '-'+ str(nowMouth + 1) +'-01 00:00:00')
        yesteryear = (nowMouth + 1) % 13
        whereSql = "r_time >= '%s' and  r_time < '%s'" %(endTimeSql,beginTimeSql)
        for i in range(12):
            histogramXData.append(yesteryear % 12 if yesteryear % 12 != 0 else 12 )
            yesteryear += 1
            histogramData.append(0)
    hData = {}
    g.cursor.execute("select to_char(r_time,'" + rule +" ') cycletime,count(log_id) as logcount,count(distinct(s_ip)) as sipcount,count(distinct(d_ip)) as dipcount from h_threat_info where "+ whereSql +" group by cycletime order by cycletime desc ")
    rows = g.cursor.fetchall()
    logcount = histogramData.copy()
    sipcount = histogramData.copy()
    dipcount = histogramData.copy()
    for row in rows:
        if(histogramXData.index(int(row['cycletime']))!=-1):
            logcount[histogramXData.index(int(row['cycletime']))] = row['logcount']
            sipcount[histogramXData.index(int(row['cycletime']))] = row['sipcount']
            dipcount[histogramXData.index(int(row['cycletime']))] = row['dipcount']
    hData['logcount']=logcount
    hData['sipcount']=sipcount
    hData['dipcount']=dipcount  
    result = {}
    result["histogramData"] = hData
    result["histogramXData"] = histogramXData
    return result

def dataAnalysisStatistics():
    try:
        g.cursor.execute(
        """
        select 
        count(*) as allcount,
        sum(case when r_time <= %s and r_time >= %s then 1 else 0 end) as thisweek, 
        sum(case when r_time <= %s and r_time >= %s then 1 else 0 end) as lastweek,
        sum(case when r_time <= %s and r_time >= %s then 1 else 0 end) as thismonth,
        sum(case when r_time <= %s and r_time >= %s then 1 else 0 end) as lastmonth,
        count(distinct s_ip) as sipcount,
        count(distinct d_ip) as dipcount
        from h_threat_info
        """, (datetime.datetime.now(), datetime.datetime.now()-datetime.timedelta(7), datetime.datetime.now()-datetime.timedelta(7), datetime.datetime.now()-datetime.timedelta(14),
            datetime.datetime.now(), datetime.datetime.now()-datetime.timedelta(30), datetime.datetime.now() - datetime.timedelta(30), datetime.datetime.now() - datetime.timedelta(60)))
        rows = g.cursor.fetchall()
        yestDay = (datetime.datetime.now()-datetime.timedelta(1) + datetime.timedelta(hours=int(1))). strftime('%Y-%m-%d %H'+':00:00')
        g.cursor.execute(
        """
        select
        count(distinct s_ip)
        from (select * from h_threat_info where r_time >= %s) a
        where not EXISTS (select 1 from h_threat_info b where r_time < %s and a.s_ip = b.s_ip)

        """, (yestDay,yestDay))
        rows1 = g.cursor.fetchall()
        g.cursor.execute(
        """
        select
        count(distinct d_ip)
        from (select * from h_threat_info where r_time >= %s) a
        where not EXISTS (select 1 from h_threat_info b where r_time < %s and a.d_ip = b.d_ip)

        """, (yestDay,yestDay))
        rows2 = g.cursor.fetchall()
        aggregateStatistics = {}
        aggregateStatistics['threatDataCount'] = rows[0]["allcount"]
        thisweek = rows[0]["thisweek"] if rows[0]["thisweek"] != None else 0
        thismonth = rows[0]["thismonth"] if rows[0]["thismonth"] != None else 0
        lastweek = rows[0]["lastweek"] if rows[0]["lastweek"] != None else 0
        lastmonth = rows[0]["lastmonth"] if rows[0]["lastmonth"] != None else 0
        aggregateStatistics['weekRingThan'] = (thisweek - lastweek) / (lastweek if lastweek != None and lastweek != 0 else 1) # 周环比
        aggregateStatistics['monthRingThan'] = (thismonth - lastmonth) / (lastmonth if lastmonth != None and lastmonth != 0 else 1)
        aggregateStatistics['attackSourceCount'] = rows[0]["sipcount"]
        aggregateStatistics['asAddYesterday'] = rows1[0]["count"]
        aggregateStatistics['avictimHostCount'] = rows[0]["dipcount"]
        aggregateStatistics['ahAddYesterday'] = rows2[0]["count"]
        
        ###########################     饼图数据    ##########################
        g.cursor.execute("""
            SELECT 
            'APT事件'  as ttn0,sum(case when string_to_array(threat_type,',') @> array['APT事件'] then 1  else 0 end) as ttv0,
		    '僵尸网络' as ttn1,sum(case when string_to_array(threat_type,',') @> array['僵尸网络'] then 1  else 0 end) as ttv1, 
			'勒索软件' as ttn2,sum(case when string_to_array(threat_type,',') @> array['勒索软件'] then 1  else 0 end) as ttv2,
			'流氓推广' as ttn3,sum(case when string_to_array(threat_type,',') @> array['流氓推广'] then 1  else 0 end) as ttv3,
			'窃密木马' as ttn4,sum(case when string_to_array(threat_type,',') @> array['窃密木马'] then 1  else 0 end) as ttv4,
			'远控木马' as ttn5,sum(case when string_to_array(threat_type,',') @> array['远控木马'] then 1  else 0 end) as ttv5,
			'网络蠕虫' as ttn6,sum(case when string_to_array(threat_type,',') @> array['网络蠕虫'] then 1  else 0 end) as ttv6,
			'黑市工具' as ttn7,sum(case when string_to_array(threat_type,',') @> array['黑市工具'] then 1  else 0 end) as ttv7,
			'挖矿木马' as ttn8,sum(case when string_to_array(threat_type,',') @> array['挖矿木马'] then 1  else 0 end) as ttv8
            FROM public.h_threat_info
        """)
        rows2 = g.cursor.fetchall()
        piechartsData = []
        for i in range(9):
            piechartsData.append({'name':rows2[0]["ttn"+str(i)],'value':rows2[0]["ttv"+str(i)] if rows2[0]["ttv"+str(i)] != None else 0})
        piechartsData = sorted(piechartsData, key=lambda RealDictRow: RealDictRow["value"],reverse=True)
        ###########################     攻击源排名    ##########################
        g.cursor.execute("select s_ip,string_agg(s_ip_location,',') as alocation,count(*) as attackCount from h_threat_info group by s_ip order by attackCount desc limit 10 offset 0")
        rows3 = g.cursor.fetchall()
        attackSource = []     # 攻击源前10集合
        for rows in rows3:
            victimHost = rows["s_ip"]
            attackNumber = rows["attackcount"]
            location = rows["alocation"].split(",")[0] if rows["alocation"] != None and rows["alocation"] != "" else ""
            nationalFlag = locationMapping.get(locationTransition(location)) if locationMapping.get(locationTransition(location)) != None else ""
            attackSource.append({"victimHost":victimHost,"attackNumber":attackNumber,"location":location,"nationalFlag":nationalFlag})
        

        ###########################     被攻击主机排名    ##########################
        g.cursor.execute("select d_ip,string_agg(d_ip_location,',')  as alocation,count(*) as attackCount from h_threat_info group by d_ip order by attackCount desc limit 10 offset 0")
        rows3 = g.cursor.fetchall()
        avictimHost = []     # 被攻击主机排名前10集合
        for rows in rows3:
            victimHost = rows["d_ip"]
            attackNumber = rows["attackcount"]
            location = rows["alocation"].split(",")[0] if rows["alocation"] != None and rows["alocation"] != "" else ""
            nationalFlag = locationMapping.get(locationTransition(location)) if locationMapping.get(locationTransition(location)) != None else ""
            avictimHost.append({"victimHost":victimHost,"attackNumber":attackNumber,"location":location,"nationalFlag":nationalFlag})
        result = {}
        result["aggregateStatistics"] = aggregateStatistics
        result["piechartsData"] = piechartsData
        result["attackSource"] = attackSource
        result["avictimHost"] = avictimHost 
        result["hisData"] = ""

        # g.cursor.execute("insert into t_result(beacon_type,threat_type,beacon,credibility,tags,state,r_time,invalid_time) values (%s,%s,%s,%s,%s,%s,%s,%s) ")        
        return result
    except Exception as e:
        print(traceback.format_exc())
        return {}
  
def positionRank(face = "attack"):
    """ 攻击地点排名  """
    try:
        if(face == "attack"):
            sql = """select s_ip_location as location,count(distinct(s_ip)) as ipcount,count(log_id) as logidcount 
                     from h_threat_info  where s_ip_location != '' and s_ip_location is not null group by location order by ipcount desc,logidcount desc"""
        else:
            sql = """select d_ip_location as location,count(distinct(d_ip)) as ipcount,count(log_id) as logidcount 
                     from h_threat_info  where d_ip_location != '' and d_ip_location is not null  group by location order by ipcount desc,logidcount desc"""
        g.cursor.execute(sql)
        rows = g.cursor.fetchall()
        result = []
        for row in rows:
            gather = {}
            gather["location"] = row["location"]
            gather["nationalFlag"] = locationMapping.get(locationTransition(row["location"])) if locationMapping.get(locationTransition(row["location"])) != None else ""
            gather["ipcount"] = row["ipcount"]
            gather["logidcount"] = row["logidcount"]
            result.append(gather)
        return result
    except Exception as e:
        print(traceback.format_exc())
        return []

def circuitInfo():
    """ 获取线路信息 """
    try:
        result = {}  # 返回数据集合
        g.cursor.execute("""select line_info as lineinfo,count(log_id) as logidcount 
                     from  h_threat_info  group by lineinfo """)
        rows = g.cursor.fetchall()
        lines = []
        for row in rows:
            gather = {}
            gather["lineName"] = row["lineinfo"]
            gather["lineCount"] = row["logidcount"]
            lines.append(gather)
        result["lines"] = lines
        count = 0
        for line in lines:
            count += int(line["lineCount"])
        result["count"] = count
        return result
    except Exception as e:
        print(traceback.format_exc())
        return {}

def getAptorgs():
    try:
        g.cursor.execute("select distinct unnest(string_to_array(string_agg(apt_org,','),',')) as aptorg from h_threat_info where apt_org != ''")
        rows = g.cursor.fetchall()
        querySql = "select "
        i = 0
        for row in rows:
            querySql += "'"+row["aptorg"]+"' as ttn" + str(i) + ",sum(case when string_to_array(apt_org,',') @> array['"+ row["aptorg"] +"'] then 1  else 0 end) as ttv"+str(i)+","
            i += 1
        querySql = querySql[0:-1] + " FROM public.h_threat_info"
        g.cursor.execute(querySql)
        rows2 = g.cursor.fetchall()
        aptOrgData = []
        for i in range(len(rows)):
            aptOrgData.append({'name':rows2[0]["ttn"+str(i)],'value':rows2[0]["ttv"+str(i)] if rows2[0]["ttv"+str(i)] != None else 0})
        aptOrgData = sorted(aptOrgData, key=lambda RealDictRow: RealDictRow["value"],reverse=True)
        return aptOrgData
    except Exception as e:
        logging.error(traceback.format_exc())
        return []   


def attackTechnique():
    """ 获取攻击手法和攻击工具 """
    try:
        g.cursor.execute(
        """
            SELECT 
            '漏洞利用' as ttn0,sum(case when string_to_array(attack_technique,',') @> array['漏洞利用'] then 1  else 0 end) as ttv0,
		    'SQL注入' as ttn1,sum(case when string_to_array(attack_technique,',') @> array['SQL注入'] then 1  else 0 end) as ttv1, 
			'分布式拒绝服务攻击' as ttn2,sum(case when string_to_array(attack_technique,',') @> array['分布式拒绝服务攻击'] then 1  else 0 end) as ttv2,
			'避免阻隔' as ttn3,sum(case when string_to_array(attack_technique,',') @> array['避免阻隔'] then 1  else 0 end) as ttv3,
			'劫持' as ttn4,sum(case when string_to_array(attack_technique,',') @> array['劫持'] then 1  else 0 end) as ttv4,
			'扫描' as ttn5,sum(case when string_to_array(attack_technique,',') @> array['扫描'] then 1  else 0 end) as ttv5,
			'爆破' as ttn6,sum(case when string_to_array(attack_technique,',') @> array['爆破'] then 1  else 0 end) as ttv6
            FROM public.h_threat_info
        """)
        rows = g.cursor.fetchall()
        piechartsData = []
        for i in range(7):
            piechartsData.append({'name':rows[0]["ttn"+str(i)],'value':rows[0]["ttv"+str(i)] if rows[0]["ttv"+str(i)] != None else 0})
        piechartsData = sorted(piechartsData, key=lambda RealDictRow: RealDictRow["value"],reverse=True)
        g.cursor.execute(
        """
            SELECT 
            '黑客工具' as ttn0,sum(case when string_to_array(attack_tool,',') @> array['黑客工具'] then 1  else 0 end) as ttv0,
		    '远控' as ttn1,sum(case when string_to_array(attack_tool,',') @> array['远控'] then 1  else 0 end) as ttv1, 
			'木马' as ttn2,sum(case when string_to_array(attack_tool,',') @> array['木马'] then 1  else 0 end) as ttv2
            FROM public.h_threat_info
            """)
        rows2 = g.cursor.fetchall()
        pieData = []
        for i in range(3):
            pieData.append({'name':rows2[0]["ttn"+str(i)],'value':rows2[0]["ttv"+str(i)] if rows[0]["ttv"+str(i)] != None else 0})
        pieData = sorted(pieData, key=lambda RealDictRow: RealDictRow["value"],reverse=True)
        result = {}
        result["attacktechnique"] = piechartsData
        result["attacktools"] = pieData
        return result
    except Exception as e:
        print(traceback.format_exc())
        return {}

def run():
    try:
        while(True):
            with app.app_context():
                g.conn = connect(**config.DatabaseConfig.siem)
                g.cursor = g.conn.cursor(cursor_factory=RealDictCursor)
                dataAnalysis = dataAnalysisStatistics()
                positionRankAttack = positionRank()
                positionRankBeAttacked = positionRank("beAttacked")
                circuit = circuitInfo()
                attacktech = attackTechnique()
                aptOrgsData = getAptorgs()
                pool = redis.ConnectionPool(host=config.REDIS.redis_host, port=config.REDIS.redis_port, decode_responses=True)
                r1 = redis.Redis(connection_pool=pool)
                r1.set("dataAnalysis",str(dataAnalysis))
                r1.set("positionRankAttack",str(positionRankAttack))
                r1.set("positionRankBeAttacked",str(positionRankBeAttacked))
                r1.set("circuit",str(circuit))
                r1.set("attacktech",str(attacktech))
                r1.set("aptOrgsData",str(aptOrgsData))
                if g.cursor:
                    g.cursor.close()
                    g.cursor = None
                if g.conn:
                    g.conn.close()
                    g.conn = None
            time.sleep(int(config.ToCacheTime.cacheTime))
    except Exception as e:
        if g.cursor:
            g.cursor.close()
            g.cursor = None
        if g.conn:
            g.conn.close()
            g.conn = None


if __name__ == '__main__':
    thread = Process(target=run)
    thread.start()   
    app.run(host='0.0.0.0', port=9002, debug=False)
