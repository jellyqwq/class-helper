import re
import time
from datetime import datetime
import urllib.request
import urllib.parse
import json
from .__init__ import log

headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-US;q=0.8,zh-CN;q=0.7,zh;q=0.6,ja-CN;q=0.5,ja;q=0.4',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'wecat.hnkjedu.cn',
        'Origin': 'http://wecat.hnkjedu.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat',
        'X-Requested-With': 'XMLHttpRequest'
    }

def urllibpost(url = None, headers = None, data = None) -> dict | list:
    'A post method by urllib'
    data = urllib.parse.urlencode(data).encode('utf-8')
    try:
        req = urllib.request.Request(url=url,
                                data=data,
                                headers=headers,
                                method='POST')
    except:
        raise 'url is invalid'
    else:
        response = urllib.request.urlopen(req)
        if response.status == 200:
            return json.loads(response.read().decode('utf-8'))
        else:
            return {'error': response.status}

# 计算星期几和第几周
def today():
    '''
    week -> int\n
    week_count -> int
    '''
    # 获取星期几 => int
    week = datetime.today().isoweekday() # isoweekday()方法可以获取和星期几对应的整型
    start_semester = time.mktime(time.strptime('2022-2-21 00:00:00', '%Y-%m-%d %H:%M:%S'))
    now_semester = time.time()
    # 计算周数-时间戳算周
    week_count = int((now_semester - start_semester) // 604800 + 1)
    return week, week_count

# 对教室名字格式化,使其成为浅显易懂的
def format_classRoom(s):
    s = re.sub(r'19-', '实训楼',s)
    s = re.sub(r'教学楼60', '6',s)
    s = re.sub(r'10-', '信息学院',s)
    s = re.sub(r'阶梯教室', '公共大楼',s)
    s = re.sub(r'（一楼报告厅）', '',s)
    return s

# 解析课表json
def parse_class(_josn, week, week_count, data_course, cweek, cweek_count):
    Jctotime_start = {
        1: "8:15",
        2: "9:10",
        3: "10:15",
        4: "11:10",
        5: "14:50",
        6: "15:45",
        7: "16:40",
        8: "17:35",
        9: "19:10",
        10: "20:05",
        11: "21:00"
    }
    Jctotime_end = {
        1: "9:00",
        2: "9:55",
        3: "11:00",
        4: "11:55",
        5: "15:35",
        6: "16:30",
        7: "17:25",
        8: "18:20",
        9: "19:55",
        10: "20:50",
        11: "21:45"
    }

    for i in _josn:
        if i['courseTimeXq'] == 'K%d' % week:
            for j in i['Content_jieci']:
                courseTimeJc = j['courseTimeJc']
                for kecheng in j['Content_kecheng']:
                    for wl in kecheng['week'].split(','):
                        # 将周数区间以开始和结束两个时间输出
                        if '-' in wl:
                            w = wl.split('-')
                            start_week = int(w[0])
                            end_week = int(w[1])
                        else:
                            start_week = end_week = int(wl)
                        if start_week <= week_count <= end_week:

                            data_course['班级'] = kecheng['classname']
                            data_course['时间'] = '第{}周 | 星期{}'.format(week_count, week)
                            
                            # 调休增加的信息
                            if cweek_count != week_count and cweek != week:
                                data_course['调休'] = '第{}周 | 星期{}'.format(cweek_count, cweek)

                            # 节次换算时间
                            Jc = courseTimeJc.split('-')
                            start_time = Jctotime_start[int(Jc[0])]
                            end_time = Jctotime_end[int(Jc[1])]
                            result_time = courseTimeJc + ' | ' + start_time + '-' + end_time

                            data_course[result_time] = {
                                    "课程": kecheng['courseName'],
                                    "教室": format_classRoom(kecheng['classRoom']),
                                    "老师": kecheng['teacherName']
                                }
    return data_course

# 解析
def task1(_vjson, name, week, week_count, cweek, cweek_count):
    data_course = {}
    data_course['用户'] = name
    return parse_class(_vjson, week, week_count, data_course, cweek, cweek_count)


# pushplus推送-json
def sendPushplus(token, data):
    data = {
        "token": token,
        "title":"课表小助手提醒",
        "template":"json",
        "content": json.dumps(data, ensure_ascii=False)
    }
    url = 'http://www.pushplus.plus/send'
    r = urllibpost(url, data=data)
    log.info(r)
    
def run_daily():
    from . import config, load_mongodb
    mycol, DBEXIST, COLEXIST = load_mongodb()

    # 判断数据库是否为空
    c = mycol.count_documents({})
    log.debug(c)
    if c != 0:
        # 假期调课修正
        week, week_count = today()
        twdo = config['TakeWorkingDaysOff']
        cweek_count = cweek = None
        if twdo != []:
            if twdo[0] != [] and twdo[1] != []:
                if week_count == twdo[1][0]:
                    cweek_count = twdo[0][0]
                if week == twdo[1][1]:
                    cweek = twdo[0][1]

        # 遍历数据库信息
        for i in mycol.find():
            
            if i['switch_pushplus'] != '' and i['openid'] != '' and i['pushplustoken'] != '':

                data = {
                    'openid': i['openid'],
                    'xh': i['xh'],
                    'falg': 'true'
                }
                
                url = 'http://wecat.hnkjedu.cn/kingojw/xskbjson.aspx'
                response = urllibpost(url, headers,data)
                if 'error' in response:
                    log.error(response['error'])
                elif response[0]['courseTimeXq'] == None:
                    log.error('params openid or xh is invalid')
                    log.debug(response)
                else:
                    # 此处即json的输出
                    name = i['name']
                    data = task1(response, name, week, week_count, cweek, cweek_count)
                    sendPushplus(i['pushplustoken'], data)