from calendar import c
import imp
import random
import pymongo
from flask import Flask, render_template, request, make_response
import logging as log
import json
import time
import os
import hashlib

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

os.chdir(os.path.dirname(__file__))

# 读取配置文件
with open("example.config.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())

# 设置输出日志格式以及等级
log.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=log.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# 初始化数据库,建立数据库对象
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
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

# 请求头的设置
def res(params: str | dict | None):
    response = make_response(params)
    response.access_control_allow_origin = 'http://127.0.0.1:4443'
    return response

app = Flask(__name__, template_folder='templates')
import class_helper.views
# 注册
@app.route('/users/signup', methods=['POST'])
def signup():
    name = request.json['name']
    email = request.json['email']
    password = request.json['pwd']
    sc = request.json['sc']
    for k, v in security_code.items():
        if v[email] == sc:
            # 仅当collection为空时可以直接写入
            if not DBEXIST and not COLEXIST:
                result = mycol.insert_one({
                    "name": name,
                    "email": email,
                    "password": password,
                })
                log.info('sign up info writed successfully: %s' % result)
                del security_code[k]
                return json.dumps({'success': 0})
            # count_documents()可以计算指定元素的出现次数
            elif mycol.count_documents({'email':email}):
                log.info('email is exist')
                return json.dumps({'error': 'email is exist'})
            else:
                mycol.insert_one({
                    'name':name, 
                    'email':email, 
                    'password':password,
                })
                log.info('account created successfully\nname: %s\nemail: %s\npassword: %s' % (name, email, password))
                del security_code[k]
                return json.dumps({'success': 0})

# 验证码
@app.route('/sendvcode', methods=['POST'])
def sendvcode():
    # count_documents()可以计算指定元素的出现次数
    if mycol.count_documents({'email':email}):
        log.info('email %s was already signed up' % email)
        return json.dumps({'error': 'email was already signed up'})
    t = time.time()
    if security_code != {}: 
        for i in security_code.keys():
            if int(t) - int(i) >= 180:
                del security_code[i]
    email = request.json['email']
    content = generate_verification_code()
    send_email(email,content)
    security_code[time.time()] = {email:content}
    log.info('verification code sent successfully')
    return json.dumps({'succeed': 0})

# 登录
@app.route('/users/login', methods=['POST'])
def login():
    log.debug(request.content_type)
    email = request.form['email']
    log.debug("email: %s" % email)
    pwd = request.form['pwd']
    log.debug("password: %s" % pwd)
    if email != '':
        count = mycol.count_documents({'email':email})
        log.debug("count: %d" % count)
        if count == 0:
            log.error('Email %s is unavailable' % email)
            return res({'error': '邮箱不存在'})
        if pwd != '':
            d = mycol.find_one({'email':email})
            log.debug("d: %s" % d)
            if d['password'] == pwd:
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
    response = res(render_template('login.html'))
    response.delete_cookie('sh')
    return response

@app.route('/test', methods=['POST'])
def test():
    log.debug(request.content_type)
    email = request.form['email']
    log.debug(email)
    pwd = request.form['pwd']
    log.debug(pwd)
    return res({'succeed': '返回成功'})

if __name__ == '__main__':
    app.run(host='localhost', port=4443, debug=True)
