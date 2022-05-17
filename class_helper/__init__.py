import json
# 读取配置文件
with open("./class_helper/example.config.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())

import re
import random
import pymongo
import logging as log
import time
import hashlib

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

# 设置输出日志格式以及等级
log.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=log.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# 初始化数据库,建立数据库对象
def load_mongodb():
    myclient = pymongo.MongoClient("mongodb://{}:{}/".format(config['MongoDBHost'], config['MongoDBPort']))
    mydb = myclient["class_helper"]
    log.info("database is loading...")
    DBEXIST = COLEXIST = True
    dblist = myclient.list_database_names()
    if 'class_helper' not in dblist:
        log.info('database is empty')
        DBEXIST = False
    mycol = mydb['user_config']
    collist = mydb.list_collection_names()
    if collist == []:
        log.info('collection is empty')
        COLEXIST = False
    if DBEXIST and COLEXIST:
        log.info('database loaded successfully')
    return mycol, DBEXIST, COLEXIST

# 验证码缓存
security_code = {}

# 生成验证码
def generate_verification_code():
    code_list = []
    # 取数字
    for i in range(10):
        code_list.append(str(i))
    # 取大写字母
    for i in range(65, 91):
        code_list.append(chr(i))
    # 取小写字母
    for i in range(97, 123):
        code_list.append(chr(i))
    # 根据配置文件获取长度获取随机验证码
    myslice = random.sample(code_list, config['VerificationCodeLenth'])
    verification_code = ''.join(myslice)
    return verification_code

# 发送验证码
def send_email(email, content):
    '向指定邮箱发送文本'
    #qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    #sender_qq为发件人的qq号码
    sender_qq = config['QQAccount']
    #pwd为qq邮箱的授权码
    pwd = config['QQEmailPassword']
    #发件人的邮箱
    sender_qq_mail =  config['QQEmail']
    #收件人邮箱
    receiver = email
    #邮件的正文内容
    mail_content = content
    #邮件标题
    mail_title = '课表推送服务验证码'
    #ssl登录
    smtp = SMTP_SSL(host_server)
    #set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()

from flask import Flask, render_template, request, make_response
# 请求头的设置
def res(params):
    response = make_response(params)
    response.access_control_allow_origin = '/'
    return response

app = Flask(__name__, template_folder='templates')
from . import views
# 注册
@app.route('/users/signup', methods=['POST'])
def signup():
    mycol, DBEXIST, COLEXIST = load_mongodb()
    try:
        email = request.form['email']
        password = request.form['pwd']
        sc = request.form['sc']
    except:
        return res({'error': '参数错误'})
    else:
        # 数据校验
        if email == '':
            return res({'error': '邮箱不能为空'})
        if password == '':
            return res({'error': '密码不能为空'})
        if sc == '':
            return res({'error': '验证码不能为空'})
        if not bool(re.match(r'^[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{1,64}@[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{3,64}$', email, re.I)):
            return res({'error': '邮箱不合法'})
        if not bool(re.match(r'^[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{6,32}$', password, re.I)):
            return res({'error': '密码不合法'})
        if not bool(re.match(r'^[0-9a-z]+$', sc, re.I)) and len(sc) != config['VerificationCodeLenth']:
            return res({'error': '验证码不合法'})
        
        # 将超时验证码删除
        t = time.time()
        if security_code != {}: 
            for i in security_code.keys():
                if int(t) - int(i) >= 180:
                    del security_code[i]

        # 密码哈希加密
        hash_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
        for k, v in security_code.items():
            if v[email] == sc:
                # 生成cookie
                temp_str = email + str(time.time())
                cookie = hashlib.sha256(temp_str.encode('utf-8')).hexdigest()

                # 仅当collection为空时可以直接写入
                if not DBEXIST and not COLEXIST:
                    result = mycol.insert_one({
                        "name": "",
                        "email": email,
                        "password": hash_pwd,
                        "cookie": cookie,
                        "openid": "",
                        "xh": "",
                        "pushplustoken": "",
                        "switch_pushplus": "",
                        "switch_telegram": "",
                        "switch_weather": "",
                        "telegram_bot_token": "",
                        "telegram_user_id": "",
                        "switch_pushplus_rightnow": "",
                        "switch_telegram_rightnow": ""
                    })
                    log.info('sign up info writed successfully: %s' % result)
                    del security_code[k]
                    response = res({'success': '注册成功'})
                    response.set_cookie('sh', cookie, max_age=86400)
                    return response
                # count_documents()可以计算指定元素的出现次数
                elif mycol.count_documents({'email':email}):
                    log.info('email is exist')
                    return res({'error': '邮箱已存在'})
                else:
                    result = mycol.insert_one({
                        "name": "",
                        "email": email,
                        "password": hash_pwd,
                        "cookie": cookie,
                        "openid": "",
                        "xh": "",
                        "pushplustoken": "",
                        "switch_pushplus": "",
                        "switch_telegram": "",
                        "switch_weather": "",
                        "telegram_bot_token": "",
                        "telegram_user_id": "",
                        "switch_pushplus_rightnow": "",
                        "switch_telegram_rightnow": ""
                    })
                    log.info('sign up info writed successfully: %s' % result)
                    log.info('account created successfully\nemail: %s\npassword: %s' % (email, password))
                    del security_code[k]
                    response = res({'success': '注册成功'})
                    response.set_cookie('sh', cookie, max_age=86400)
                    return response
        return res({'error': '验证码超时或未发送'})

def sendvcode(is_resetpwd=False):
    mycol, DBEXIST, COLEXIST = load_mongodb()
    try:
        email = request.form['email']
    except:
        return res({'error': '参数错误'})
    else:
        if email == '':
            return res({'error': '邮箱不能为空'})
        if not bool(re.match(r'^[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]+@[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]+$', email, re.I)):
            return res({'error': '邮箱不合法'})
        
        # 检验是否为重置密码的验证码
        if is_resetpwd == False:
            # count_documents()可以计算指定元素的出现次数
            if mycol.count_documents({'email':email}):
                log.info('email %s was already signed up' % email)
                return res({'error': '邮箱已存在'})
        else:
            if not mycol.count_documents({'email':email}):
                log.info('邮箱 %s 不存在' % email)
                return res({'error': '邮箱不存在'})
        
        t = time.time()
        if security_code != {}: 
            for i in security_code.keys():
                if int(t) - int(i) >= 180:
                    del security_code[i]
            for i in security_code.values():
                log.debug(i)
                if email in i:
                    return res({'error': '请勿重复发送验证码'})
        content = generate_verification_code()
        send_email(email,content)
        security_code[time.time()] = {email:content}
        log.info('verification code sent successfully')
        return res({'result': '验证码发送成功(3分钟有效)'})

# 注册时发送验证码
@app.route('/sendvcode', methods=['POST'])
def sendvcode_by_register():
    return sendvcode()

# 重置密码时发送的验证码
@app.route('/sendvcode/resetpwd', methods=['POST'])
def sendvcode_by_reset():
    return sendvcode(True)


# 登录
@app.route('/users/login', methods=['POST'])
def login():
    mycol, DBEXIST, COLEXIST = load_mongodb()
    try:
        log.debug(request.content_type)
        email = request.form['email']
        log.debug("email: %s" % email)
        pwd = request.form['pwd']
        log.debug("password: %s" % pwd)
    except:
        return res({'error': '参数错误'})
    else:
        if email != '':
            count = mycol.count_documents({'email':email})
            log.debug("count: %d" % count)
            if count == 0:
                log.error('Email %s is unavailable' % email)
                return res({'error': '邮箱不存在'})
            if pwd != '':
                d = mycol.find_one({'email':email})
                log.debug("d: %s" % d)
                hash_pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
                if d['password'] == hash_pwd:
                    old_hash = d['cookie']
                    temp_str = old_hash + str(time.time())
                    new_hash = hashlib.sha256(temp_str.encode('utf-8')).hexdigest()
                    result = mycol.update_one({"_id": d['_id']}, {"$set": { "cookie": new_hash}})
                    log.debug(result)
                    response = res(render_template('config.html'))
                    response.set_cookie('sh', new_hash, max_age=86400)
                    return response
                else:
                    return res({'error': '密码错误'})
            else:
                log.error('Password %s can\'t be empty' % pwd)
                return res({'error': '密码不能为空'})
        else:
            log.error('Email %s can\'t be empty' % email)
            return res({'error': '邮箱不能为空'})

# 退出登录-删除cookie
@app.route('/users/logout', methods=['POST'])
def logout():
    # response = res(render_template('login.html',
    #                 host = config['Host'],
    #                 port = config['Port']))
    response = res({'success': '退出成功'})
    response.delete_cookie('sh')
    return response

@app.route('/submit', methods=['POST'])
def submit():
    mycol, DBEXIST, COLEXIST = load_mongodb()
    # 检查cookie
    try:
        cookie = request.cookies.to_dict()
    except:
        return res({'error': '参数错误'})
    else:
        log.debug('cookie: %s' % cookie)
        if cookie == {}:
            # cookie为空返回数据
            return res({'error': '未登录'})
        elif 'sh' in cookie.keys():
            # sh在cookie当中则提取sh并从数据库提取相关信息并生成表单
            sh = cookie['sh']
            log.debug('sh: %s', sh)
            # 为了防止有人加了cookie来访问导致报错,必须将cookie丢到数据库里查找,确保存在才进行操作
            count = mycol.count_documents({'cookie':sh})
            if count == 0:
                return res({'error': '未登录'})
            else:
                pass
        else:
            return res({'error': '未登录'})
        try:
            name = request.form['name']
            openid = request.form['openid']
            xh = request.form['xh']
            pushplustoken = request.form['pushplustoken']
            telegram_bot_token = request.form['tgtoken']
            telegram_user_id = request.form['tg_user_id']
            switch_pushplus = request.form['switch_pushplus']
            switch_telegram = request.form['switch_telegram']
            switch_weather = request.form['switch_weather']
            switch_pushplus_rightnow = request.form['switch_pushplus_rightnow']
            switch_telegram_rightnow = request.form['switch_telegram_rightnow']
        except:
            return res({'error': '参数错误'})
        else:
            mycol.update_many(
                {'cookie': sh},
                {
                    '$set': {
                        'xh': xh,
                        'name': name,
                        'openid': openid,
                        'pushplustoken': pushplustoken,
                        'switch_weather': switch_weather,
                        'switch_telegram': switch_telegram,
                        'switch_pushplus': switch_pushplus,
                        'telegram_user_id': telegram_user_id,
                        'telegram_bot_token': telegram_bot_token,
                        'switch_pushplus_rightnow': switch_pushplus_rightnow,
                        'switch_telegram_rightnow': switch_telegram_rightnow
                    }
                }
            )
            from . import daily_plan
            back1, back2 = daily_plan.sendRightNow(sh)
            log.info(back1)
            log.info(back2)
            return res({'result': '更新成功'})

@app.route('/user/resetpwd', methods=['POST'])
def reset_password():
    mycol, DBEXIST, COLEXIST = load_mongodb()
    try:
        email = request.form['email']
        password = request.form['pwd']
        sc = request.form['sc']
    except:
        return res({'error': '参数错误'})
    else:
        # 数据校验
        if email == '':
            return res({'error': '邮箱不能为空'})
        if password == '':
            return res({'error': '密码不能为空'})
        if sc == '':
            return res({'error': '验证码不能为空'})
        if not bool(re.match(r'^[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{1,64}@[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{3,64}$', email, re.I)):
            return res({'error': '邮箱不合法'})
        if not bool(re.match(r'^[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{6,32}$', password, re.I)):
            return res({'error': '密码不合法'})
        if not bool(re.match(r'^[0-9a-z]+$', sc, re.I)) and len(sc) != config['VerificationCodeLenth']:
            return res({'error': '验证码不合法'})
        
        # 将超时验证码删除
        t = time.time()
        if security_code != {}: 
            for i in security_code.keys():
                if int(t) - int(i) >= 180:
                    del security_code[i]

        # 密码哈希加密
        hash_pwd = hashlib.sha256(password.encode('utf-8')).hexdigest()
        for k, v in security_code.items():
            if v[email] == sc:

                # count_documents()可以计算指定元素的出现次数
                if not mycol.count_documents({'email':email}):
                    log.info('email is exist')
                    return res({'error': '邮箱不存在'})
                else:
                    mycol.update_many({'email':email},
                    {
                        '$set': {
                            "email": email,
                            "password": hash_pwd
                        }
                    })
                    log.info("email (%s) succeefully reset password" % email)
                    del security_code[k]
                    response = res({'success': '密码重置成功'})
                    return response
        return res({'error': '验证码超时或未发送'})

@app.route('/user/delete', methods=['POST'])
def userdelete():
    mycol, DBEXIST, COLEXIST = load_mongodb()
    try:
        email = request.form['email']
        sc = request.form['sc']
    except:
        return res({'error': '参数错误'})
    else:
        # 数据校验
        if email == '':
            return res({'error': '邮箱不能为空'})
        if sc == '':
            return res({'error': '验证码不能为空'})
        if not bool(re.match(r'^[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{1,64}@[a-z0-9#\!%&\'$\+\-\*/=?^_`.{|}~]{3,64}$', email, re.I)):
            return res({'error': '邮箱不合法'})
        if not bool(re.match(r'^[0-9a-z]+$', sc, re.I)) and len(sc) != config['VerificationCodeLenth']:
            return res({'error': '验证码不合法'})
        
        # 将超时验证码删除
        t = time.time()
        if security_code != {}: 
            for i in security_code.keys():
                if int(t) - int(i) >= 180:
                    del security_code[i]
        
        for k, v in security_code.items():
            if v[email] == sc:

                # count_documents()可以计算指定元素的出现次数
                if not mycol.count_documents({'email':email}):
                    log.info('email is exist')
                    return res({'error': '邮箱不存在'})
                else:
                    mycol.delete_one({'email': email})
                    del security_code[k]
                    log.info('账号(%s)删除成功' % email)
                    response = res({'success': '账号删除成功'})
                    return response
        return res({'error': '验证码超时或未发送'})