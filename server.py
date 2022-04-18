import json
import os
import time
from flask import Flask, request
import logging as log
import random
import main

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

# os.chdir(os.path.dirname(__file__))
log.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=log.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
os.makedirs('./email', exist_ok=True)

security_code = {}

def send_email(email, content):
    #qq邮箱smtp服务器
    host_server = ''
    sender_qq = ''
    #pwd为qq邮箱的授权码
    pwd = ''
    #发件人的邮箱
    sender_qq_mail = ''
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

def  generate_verification_code(len=6):
     code_list  =  [] 
     for  i  in  range (10):  # 0-9数字
         code_list.append(str(i))
     for  i  in  range (65, 91):  # 对应从“A”到“Z”的ASCII码
         code_list.append(chr (i))
     for  i  in  range (97, 123):  #对应从“a”到“z”的ASCII码
         code_list.append(chr(i))
     myslice = random.sample(code_list, len)   # 从list中随机获取6个元素，作为一个片断返回
     verification_code = ''.join(myslice)  # list to string
     return  verification_code

app = Flask(__name__)

@app.route('/get_personal_info', methods=['POST'])
def get_personal_info():
    try:
        user_id = request.json['user_id']
        hs = request.json['hs']
        cpli = os.listdir('./user_config/')
        for i in cpli:
            cpfile = i[:-5].split('-')
            if user_id == cpfile[0] and hs == cpfile[1]:
                with open(f'./user_config/{user_id}-{hs}.json', 'r', encoding='utf-8') as f:
                    log.info('信息获取成功')
                    return json.dumps({'file': f.read()}, ensure_ascii=False)
            elif user_id == cpfile[0] and hs != cpfile[1]:
                log.error('密码错误')
                return json.dumps({'error': '密码错误'}, ensure_ascii=False)
        log.error('账号不存在')
        return json.dumps({'error': '账号不存在'}, ensure_ascii=False)
    except:
        log.error('账号信息获取失败')
        return json.dumps({'error': '账号信息获取失败'}, ensure_ascii=False)

@app.route('/push_personal_info', methods=['POST'])
def push_personal_info():
    try:
        user_id = request.json['user_id']
        hs = request.json['hs']
        file = request.json['file']
        with open('./user_config/{}-{}.json'.format(user_id, hs), 'w', encoding='utf8') as f:
            f.write(file)
        log.info('提交成功')
        return json.dumps({'msg': '提交成功'}, ensure_ascii=False)
    except:
        log.info('提交失败')
        return json.dumps({'error': '提交失败'})

@app.route('/is_email_exist', methods=['POST'])
def is_email_exist():
    try:
        user_id = request.json['user_id']
        log.info('user_id:{}'.format(user_id))
        li = os.listdir('./email')
        if li != []:
            for l in li:
                if user_id in l:
                    log.info('账号已存在')
                    return json.dumps({'error': '账号已存在'})
        log.error('账号可注册')
        return json.dumps({'msg': '账号可注册'})
    except:
        log.error('账号检测失败')
        return json.dumps({'msg': '账号检测失败'})

@app.route('/send_security_code', methods=['POST'])
def send_security_code():
    try:
        # 去除超时验证码
        t = time.time()
        if security_code != {}: 
            for i in security_code.keys():
                if int(t) - int(i) >= 180:
                    del security_code[i]
        email = request.json['email']
        content = generate_verification_code()
        send_email(email,content)
        security_code[time.time()] = {email:content}
        log.info('验证码发送成功')
        return json.dumps({'msg': 'succeed'})
    except:
        log.error('验证码发送失败')
        return json.dumps({'error': '验证码发送失败'})

@app.route('/email_check', methods=['POST'])
def email_check():
    try:
        email = request.json['email']
        sc = request.json['sc']
        user_id = request.json['user_id']
        for k, v in security_code.items():
            if v[email] == sc:
                with open('./email/{}.txt'.format(user_id), 'r+', encoding='utf-8') as f:
                    f.seek(0)
                    if email == f.read():
                        return json.dumps({'msg': 'succeed'})
                    else:
                        f.seek(0)
                        f.write(email)
                del security_code[k]
                log.info('验证码检测通过')
                return json.dumps({'msg': 'succeed'})
        log.error('验证码错误')
        return json.dumps({'error': '验证码错误'})
    except:
        log.error('验证码验证失败')
        return json.dumps({'error': '验证码验证失败'})

@app.route('/reset', methods=['POST'])
def userid_email():
    try:
        user_id = request.json['user_id']
        hs = request.json['hs']
        sc = request.json['sc']
        email = request.json['email']
        li = os.listdir('./user_config/')
        for k, v in security_code.items():
            if v[email] == sc:
                for j in li:
                    x = j[:-5].split('-')
                    if x[0] == user_id:
                        os.renames('./user_config/{}'.format(j), './user_config/{}-{}.json'.format(user_id, hs))
                        del security_code[k]
                        log.info('重置成功')
                        return json.dumps({'msg': '重置成功'})
        log.info('重置有误')
        return json.dumps({'msg': '重置有误'})
    except:
        log.error('重置失败')
        return json.dumps({'error': '重置失败'})
    
@app.route('/start_one', methods=['POST'])
def start_one():
    try:
        user_info = request.json['user_info']
        r = main.tasks_2(user_info)
        log.info(r)
        log.info('执行成功')
        return json.dumps({'msg': '执行成功'})
    except:
        log.error('初次推送失败')
        return json.dumps({'error': '初次推送失败'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6703)