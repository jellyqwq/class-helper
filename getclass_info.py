import time
from datetime import datetime
import urllib.request
import urllib.parse
import json
import logging as log

log.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=log.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

def urllibpost(url: str | None, headers: dict | None, data: dict | None) -> dict | list:
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
data = {
    'openid': 'ocoU9uGYdZZDfz9WCNJ7nd2aLF3k',
    'xh': '2021020740025',
    'falg': 'true'
    }

# url = 'http://wecat.hnkjedu.cn/kingojw/xskbjson.aspx'
# response = urllibpost(url,headers,data)
# if 'error' in response:
#     log.error(response['error'])
# elif response[0]['courseTimeXq'] == None:
#     log.error('params openid or xh is invalid')
#     log.debug(response)
# else:
#     # 此处即json的输出
#     print(response)

with open('cd.json', 'r', encoding='utf-8') as f:
    x = json.loads(f.read())

week, week_count = 2, 8
for i in x:
    if i['courseTimeXq'] == 'K%d' % week:
        for j in i['Content_jieci']:
            print(j)