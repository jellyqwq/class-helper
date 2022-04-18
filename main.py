import schedule
import json
import os
import time
import requests
import logging as log

# os.chdir(os.path.dirname(__file__))
log.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=log.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

week_change = {
    1:"Mon",
    2:"Tue",
    3:"Wed",
    4:"Thu",
    5:"Fri",
    6:"Sat",
    7:"Sun"
}
week_en2cn = {
    "Mon": "星期一",
    "Tue": "星期二",
    "Wed": "星期三",
    "Thu": "星期四",
    "Fri": "星期五",
    "Sat": "星期六",
    "Sun": "星期日"
}
order_reflect = {
    "1": "上午1,2节,8:15~9:55",
    "2": "上午3,4节,10:15~11:55",
    "3": "下午5,6节,14:50~16:30",
    "4": "下午7,8节,16:40~18:20",
    "5": "晚上9,10节,19:10~20:50",
    "6": "晚上11节,21:00~21:45"
}
# 获取今天是星期几,以及周数
def today():
    week = time.strftime("%a")
    start_semester = time.mktime(time.strptime('2022-2-21 00:00:00', '%Y-%m-%d %H:%M:%S'))
    now_semester = time.time()
    week_count = int((now_semester - start_semester) // 604800 + 1)
    return week, week_count

def get_info_data(token, info, week, week_count, student_id, class_name, class_change):
    data = {
        "班级": class_name,
        "学号": student_id,
        "时间": '第{}周-{}'.format(week_count, week_en2cn[week])
    }
    with open(f'./class_info/{class_name}.json', 'r', encoding='utf-8') as f:
        class_info = json.loads(f.read())

    # 先获取该日班级课表的信息
    cinfo = class_info['info'][week]
    for course in cinfo.keys():
        data[course] = ""
        for i in cinfo[course]:
            if week_count in i['course-week']:
                data[course] = {
                    "课程": i['course-name'],
                    "老师": i['course-teacher'],
                    "教室": i['course-position']
                }
    
    # 获取该日课表是否有选修
    if info and week in info:
        info = info[week]
        for course in info.keys():
            for i in info[course]:
                if week_count in i['course-week']:
                    data[course] = {
                        "课程": i['course-name'],
                        "老师": i['course-teacher'],
                        "教室": i['course-position']
                    }

    # 读取调课信息
    if class_change:
        for i in class_change:
            # 初始化变量
            old_course_order = str(i['course-order'][0])
            new_course_order = str(i['course-order'][1])
            old_course_week = i['course-week'][0]
            new_course_week = i['course-week'][1]
            old_course_week_day = i['course-week-day'][0]
            new_course_week_day = i['course-week-day'][1]
            # print(old_course_order, new_course_order)
            # print(old_course_week, new_course_week)
            # print(old_course_week_day, new_course_week_day)

            # 删除课程
            if week_change[old_course_week_day] == week and old_course_week == week_count:
                if old_course_order in data:
                    data[old_course_order] = ""
            
            # 添加课程
            # print(week_change[new_course_week_day], week, new_course_week, week_count)
            if week_change[new_course_week_day] == week and new_course_week == week_count:
                xinfo = class_info['info'][week_change[old_course_week_day]][old_course_order]
                for j in xinfo:
                    if old_course_week in j['course-week']:
                        if "course-position" in i:
                            course_position = i['course-position']
                        else:
                            course_position = j['course-position']
                        data[new_course_order] = {
                            "课程": j['course-name'],
                            "老师": j['course-teacher'],
                            "教室": course_position
                        }
               
    # 剔除无课的节数
    for course in cinfo.keys():
        if data[course] == '':
            del data[course]
        else:
            data[order_reflect[course]] = data.pop(course)

    if len(data) > 3:
        return {
            "token": token,
            "title":"课表小助手提醒",
            "template":"json",
            "content": json.dumps(data, ensure_ascii=False)
        }
    else:
        return None

def sendmsg(data):
    log.info('data2:{}'.format(data))
    if data == None:
        log.info(('无课程不需要推送'))
        return None
    else:
        url = 'http://www.pushplus.plus/send'
        r = requests.post(url, data=data)
        log.info(r)
        return r

# 获取个人信息的函数
def tasks_1():
    user_config = os.listdir('./user_config')
    for user_info in user_config:
        try:
            with open(f'./user_config/{user_info}', 'r', encoding='utf-8') as f:
                uinfo = json.loads(f.read())
            student_id = uinfo['student_id']
            class_name = uinfo['class_name']
            token = uinfo['token']
            week, week_count = today()
            info = uinfo['info']
            class_change = uinfo['class_change']
            data = get_info_data(token, info, week, week_count, student_id, class_name, class_change)
            return sendmsg(data)
        except:
            log.error('执行失败')
            return None

def tasks_2(user_info):
    try:
        with open(f'./user_config/{user_info}', 'r', encoding='utf-8') as f:
            uinfo = json.loads(f.read())
        student_id = uinfo['student_id']
        class_name = uinfo['class_name']
        token = uinfo['token']
        week, week_count = today()
        info = uinfo['info']
        class_change = uinfo['class_change']
        data = get_info_data(token, info, week, week_count, student_id, class_name, class_change)
        return sendmsg(data)
    except:
        log.error('执行失败')
        return None

if __name__ == '__main__':
    # print(tasks_1())
    schedule.every().day.at("06:00").do(tasks_1)
    while True:
        schedule.run_pending()
        time.sleep(1)