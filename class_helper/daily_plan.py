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

def urllibpost(url = None, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}, data = None):
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
        11: "21:00",
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

                            # 插入单双周课程判断
                            if kecheng['dsz'] == '0':
                                pass
                            else:
                                dsz = week_count % 2
                                # 单周线 >> dsz=1
                                if dsz:
                                    if kecheng['dsz'] == '1':
                                        pass
                                    else:
                                        continue
                                # 双周线 >> dsz=0
                                else:
                                    if kecheng['dsz'] == '2':
                                        pass
                                    else:
                                        continue

                            data_course['班级'] = kecheng['classname']
                            data_course['明天'] = '第{}周 | 星期{}'.format(week_count, week)
                            
                            # 调休增加的信息
                            if cweek_count != None and cweek != None:
                                data_course['调休'] = '第{}周 | 星期{}'.format(cweek_count, cweek)

                            # 节次换算时间
                            Jc = courseTimeJc.split('-')
                            try:
                                start_time = Jctotime_start[int(Jc[0])]
                            except:
                                start_time = '怎么还有课?'
                            try:
                                end_time = Jctotime_end[int(Jc[1])]
                            except:
                                end_time = Jc[0] + Jc[1]
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

# pushplus推送-default
def sendPushplus(token, text):
    data = {
        "token": token,
        "title":"课表小助手提醒",
        "template":"html",
        "content": text
    }
    try:
        r = urllibpost('http://www.pushplus.plus/send', data=data)
        log.info(r)
        return r
    except:
        log.error("pushplus推送失败")
        return {"error": "pushplus推送失败"}

# telegram推送
def sendTelegram(token, chat_id, text):
    data = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        r = urllibpost(f'https://api.telegram.org/bot{token}/sendMessage', data=data)
        log.info("TG推送成功: %s" % r)
        return r
    except:
        log.error('TG推送失败')
        return {"error": "TG推送失败"}

def addNews(i, hk, text, html=None):
    # 海科新闻
    if i['data_hkxw'] == 'true':
        text += '海科新闻   %s' % hk.data_hkxw[0]['News_time'] + '\n'
        for x in hk.data_hkxw:
            if html:
                text += '  └─ ' + '<a href="%s">%s</a> \n' % (x['News_url'], x['News_titleall'])
            else:
                text += '  └─ ' + x['News_titleall'] + '\n'
                text += '  └─ ' + x['News_url'] + '\n'
    # 通知公告
    if i['data_tzgg'] == 'true':
        text += '通知公告   %s' % hk.data_tzgg[0]['News_time'] + '\n'
        for x in hk.data_tzgg:
            if html:
                text += '  └─ ' + '<a href="%s">%s</a> \n' % (x['News_url'], x['News_titleall'])
            else:
                text += '  └─ ' + x['News_titleall'] + '\n'
                text += '  └─ ' + x['News_url'] + '\n'
    # 媒体报道
    if i['data_mtbd'] == 'true':
        text += '媒体报道   %s' % hk.data_mtbd[0]['News_time'] + '\n'
        for x in hk.data_mtbd:
            if html:
                text += '  └─ ' + '<a href="%s">%s</a> \n' % (x['News_url'], x['News_titleall'])
            else:
                text += '  └─ ' + x['News_titleall'] + '\n'
                text += '  └─ ' + x['News_url'] + '\n'
    # 领导谈话
    if i['data_ldth'] == 'true':
        text += '领导讲话   %s' % hk.data_ldth[0]['News_time'] + '\n'
        for x in hk.data_ldth:
            if html:
                text += '  └─ ' + '<a href="%s">%s</a> \n' % (x['News_url'], x['News_titleall'])
            else:
                text += '  └─ ' + x['News_titleall'] + '\n'
                text += '  └─ ' + x['News_url'] + '\n'
    # 教务通知
    if i['data_jwtz'] == 'true':
        text += '教务通知   %s' % hk.data_jwtz[0]['News_time'] + '\n'
        for x in hk.data_jwtz:
            if html:
                text += '  └─ ' + '<a href="%s">%s</a> \n' % (x['News_url'], x['News_titleall'])
            else:
                text += '  └─ ' + x['News_titleall'] + '\n'
                text += '  └─ ' + x['News_url'] + '\n'
    # 科研通知
    if i['data_kytz'] == 'true':
        text += '科研通知   %s' % hk.data_kytz[0]['News_time'] + '\n'
        for x in hk.data_kytz:
            if html:
                text += '  └─ ' + '<a href="%s">%s</a> \n' % (x['News_url'], x['News_titleall'])
            else:
                text += '  └─ ' + x['News_titleall'] + '\n'
                text += '  └─ ' + x['News_url'] + '\n'
    return text

def sendTomorrowClass():
    from . import config, load_mongodb
    mycol, DBEXIST, COLEXIST = load_mongodb()

    # 判断数据库是否为空
    c = mycol.count_documents({})
    log.debug(c)
    if c != 0:
        # 计算第二天课表
        week, week_count = today()
        if week == 7:
            week = 1
            week_count += 1
        else:
            week += 1

        # 假期调课修正
        twdo = config['TakeWorkingDaysOff']
        cweek_count = cweek = None
        if twdo != []:
            if twdo[0] != [] and twdo[1] != []:
                if week_count == twdo[1][0]:
                    cweek_count = twdo[0][0]
                if week == twdo[1][1]:
                    cweek = twdo[0][1]

        # 海科官网信息的对象获取
        from .hknews import HK
        hk = HK()

        # 遍历数据库信息
        for i in mycol.find():
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
                data = task1(response, i['name'], week, week_count, cweek, cweek_count)
                # pushplus部分
                if i['switch_pushplus'] == 'true' and i['openid'] != '' and i['pushplustoken'] != '':
                    text = '课表推送助手\n'
                    for j in data.keys():
                        if '|' in j:
                            text += j + '\n'
                            for k, v in data[j].items():
                                text += '  └─ ' + k + ': ' + v + '\n'
                        else:
                            text += j + ': ' + data[j] + '\n'
                    text = addNews(i, hk, text, True)
                    sendPushplus(i['pushplustoken'], text)
                
                # telegram推送
                if i['switch_telegram'] == 'true' and i['telegram_bot_token'] != '' and i['telegram_user_id'] != '':
                    text = '课表推送助手\n'
                    for j in data.keys():
                        if '|' in j:
                            text += j + '\n'
                            for k, v in data[j].items():
                                text += '  └─ ' + k + ': ' + v + '\n'
                        else:
                            text += j + ': ' + data[j] + '\n'
                    text = addNews(i, hk, text)
                    log.debug(text)
                    sendTelegram(i['telegram_bot_token'], i['telegram_user_id'], text)

def sendRightNow(sh):
    from . import config, load_mongodb
    mycol, DBEXIST, COLEXIST = load_mongodb()
    # 判断数据库是否为空
    c = mycol.count_documents({})
    log.debug(c)
    
    # 海科官网信息的对象获取
    from .hknews import HK
    hk = HK()

    if c != 0:
        # 今天课表
        week, week_count = today()

        # 假期调课修正
        twdo = config['TakeWorkingDaysOff']
        cweek_count = cweek = None
        if twdo != []:
            if twdo[0] != [] and twdo[1] != []:
                if week_count == twdo[1][0]:
                    cweek_count = twdo[0][0]
                if week == twdo[1][1]:
                    cweek = twdo[0][1]

        i = mycol.find_one({"cookie": sh})
        log.debug('243: %s' % i)
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
            data = task1(response, i['name'], week, week_count, cweek, cweek_count)
            back1 = back2 = None
            # pushplus部分
            if i['switch_pushplus'] == 'true' and i['openid'] != '' and i['pushplustoken'] != '' and i['switch_pushplus_rightnow'] == 'true':
                text = '课表推送助手\n'
                for j in data.keys():
                    if '|' in j:
                        text += j + '\n'
                        for k, v in data[j].items():
                            text += '  └─ ' + k + ': ' + v + '\n'
                    else:
                        text += j.replace('明天', '今天') + ': ' + data[j] + '\n'
                text = addNews(i, hk, text, True)
                back1 = sendPushplus(i['pushplustoken'], text)
            
            # telegram推送
            if i['switch_telegram'] == 'true' and i['telegram_bot_token'] != '' and i['telegram_user_id'] != '' and i['switch_telegram_rightnow'] == 'true':
                text = '课表推送助手\n'
                for j in data.keys():
                    if '|' in j:
                        text += j + '\n'
                        for k, v in data[j].items():
                            text += '  └─ ' + k + ': ' + v + '\n'
                    else:
                        text += j.replace('明天', '今天') + ': ' + data[j] + '\n'
                text = addNews(i, hk, text)
                log.debug(text)
                back2 = sendTelegram(i['telegram_bot_token'], i['telegram_user_id'], text)
            return back1, back2