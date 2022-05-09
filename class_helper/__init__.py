import random
import pymongo
from flask import Flask, jsonify, request
import logging as log
import json
import time

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

# 读取配置文件
with open("example.config.json", "r", encoding="utf-8") as f:
    config = json.loads(f.read())

# 设置输出日志格式以及等级
log.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=log.INFO,
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

app = Flask(__name__, template_folder='templates')
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

@app.route('/')

@app.route('/test', methods=['POST'])
def test():
    log.info(request.content_type)
    email = request.json['email']
    log.info(email)
    return json.dumps({'succeed': 0})

if __name__ == '__main__':
    app.run(host='localhost', port=4443, debug=True)
