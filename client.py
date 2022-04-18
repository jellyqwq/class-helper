import os
import requests
import hashlib

os.chdir(os.path.dirname(__file__))

class App:
    def __init__(self):
        print("检查配置文件中")
        if os.path.isfile('config.py'):
            print('配置文件已存在,读取配置文件')
            try:
                from config import hs, user_id, email_address
                if hs != "":
                    self.hs = hs
                else:
                    self.hs = None
                if user_id != "":
                    self.user_id = user_id
                else:
                    self.user_id = None
                if email_address != "":
                    self.email_address = email_address
                else:
                    self.email_address = None
                print('配置文件加载成功')
            except:
                self.hs = None
                self.user_id = None
                self.email_address = None
        else:
            self.hs = None
            self.user_id = None
            self.email_address = None
            
        
        self.template = """\
{
    "student_id": "学号",
    "class_name": "班级",
    "token": "pushplus的推送token",
    "info": {
        "Wed": {
            "3": [
                {
                    "course-name": "选修课名字",
                    "course-teacher": "老师姓名",
                    "course-week": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                    "course-position": "上课地点" 
                }
            ]
        }
    },
    "class_change": [
        {
            "course-week": [17, 12],
            "course-week-day": [4, 7],
            "course-order": [3, 5]
        },
        {
            "course-week": [7, 11],
            "course-week-day": [2, 4],
            "course-order": [2, 2],
            "course-position": "6102"
        }
    ]
}\
"""
    # 密码加密
    def set_hash(self, user_id, user_password):
        u = user_id + user_password
        m = hashlib.sha256(u.encode('utf8')).hexdigest()
        return m

    # 拉取信息
    def get_info(self, user_id, hs):
        data = {
            'user_id': user_id,
            'hs': hs,
            }
        r = requests.post(url='http://124.156.210.60:6703/get_personal_info', json=data).json()
        if 'error' in r:
            print(r['error'])
        else:
            with open(f'{user_id}.json', 'w', encoding='utf8') as f:
                f.write(r['file'])
            print(f'{user_id}.json保存成功')

    # 创建模板
    def create_template(self, user_id):
        with open(f'{user_id}.json', 'w', encoding='utf-8') as f:
            f.write(self.template)

    # 创建账号
    def create_account(self, user_id, user_password, email_address):
        self.hs = self.set_hash(user_id, user_password)
        self.user_id = user_id
        self.email_address = email_address
        r = requests.post('http://124.156.210.60:6703/is_email_exist', json={'user_id': self.user_id}).json()
        if 'error' in r:
            print(r['error'])
            return None
        requests.post('http://124.156.210.60:6703/send_security_code', json={'email':self.email_address})
        sc = input('请输入验证码:')
        r = requests.post('http://124.156.210.60:6703/email_check', json={'email':self.email_address,'sc': sc, 'user_id': self.user_id}).json()
        if 'error' in r:
            print(r['error'])
            return None
        print(r['msg'])
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write('hs="{}"\nuser_id="{}"\nemail_address="{}"'.format(self.set_hash(user_id, user_password), user_id, email_address))
        self.create_template(self.user_id)

if __name__ == '__main__':
    while True:
        app = App()
        while True:
            print('0.退出系统\n1.创建账号\n2.创建模板\n3.从云端获取配置信息\n4.将配置信息提交到服务器\n5.通过邮箱重置密码\n6.帮助\n7.清屏')
            command = input('')
            if command == '0':
                break
            elif command == '1':
                user_id = user_password = email_address = None
                while True:
                    if not user_id:
                        user_id = input('请输入学号:')
                    if not user_password:
                        user_password = input('请输入密码:')
                    if not email_address:
                        email_address = input('请输入邮箱:')
                    if user_id and user_password and email_address:
                        cm = input(f'学号:{user_id}\n密码:{user_password}\n邮箱:{email_address}\n是否确定(y/n):')
                        if cm == 'n':
                            break
                        elif cm == 'y':
                            app.create_account(user_id, user_password, email_address)
                            break
            elif command == '2':
                if os.path.isfile('{}.json'.format(app.user_id)):
                    while True:
                        cm = input('是否对本地配置模板覆盖(y/n):')
                        if cm == 'y':
                            if app.user_id:
                                app.create_template(app.user_id)
                                break
                            else:
                                print('请先创建账号')
                                break
                        elif cm == 'n':
                            break
            elif command == '3':
                if app.user_id and app.hs:
                    if os.path.isfile('{}.json'.format(app.user_id)):
                        while True:
                            cm = input('是否对本地配置模板覆盖(y/n):')
                            if cm == 'y':
                                app.get_info(app.user_id, app.hs)
                                break
                            elif cm == 'n':
                                break
                    else:
                        app.get_info(app.user_id, app.hs)
                else:
                    print('请先填写配置文件')
            elif command == '4':
                with open('{}.json'.format(app.user_id), 'r', encoding='utf-8') as f:
                    app.file = f.read()
                data = {
                    'user_id': app.user_id,
                    'hs': app.hs,
                    'file': app.file,
                }
                r = requests.post('http://124.156.210.60:6703/push_personal_info', json=data).json()
                if 'error' in r:
                    print(r['error'])
                else:
                    print(r['msg'])
                    r = requests.post('http://124.156.210.60:6703/start_one', json={'user_info': '{}-{}.json'.format(app.user_id, app.hs)}).json()
                    if 'error' in r:
                        print(r['error'])
                    else:
                        print(r['msg'])
            elif command == '5':
                user_id = input('重置密码的账号(学号):')
                email_address = input('账号(学号)绑定的邮箱:')
                r = requests.post('http://124.156.210.60:6703/is_email_exist', json={'user_id':user_id}).json()
                if 'error' in r:
                    requests.post('http://124.156.210.60:6703/send_security_code', json={'email':email_address})
                    sc = input('请输入验证码:')
                    r = requests.post('http://124.156.210.60:6703/email_check', json={'email':email_address, 'sc':sc, 'user_id': user_id}).json()
                    if 'error' in r:
                        print(r['error'])
                    else:
                        print(r['msg'])
                        while True:
                            pwd1 = input('请输入密码:')
                            pwd2 = input('请再次输入密码:')
                            if pwd1 == pwd2:
                                app.hs = app.set_hash(user_id, pwd1)
                                app.user_id = user_id
                                app.email_address = email_address
                                r = requests.post('http://124.156.210.60:6703/reset', json={'hs':app.hs, 'sc':sc, 'user_id': user_id, 'email':email_address}).json()
                                with open('config.py', 'w', encoding='utf-8') as f:
                                    f.write('hs="{}"\nuser_id="{}"\nemail_address="{}"'.format(app.hs, app.user_id, app.email_address))
                                print(r['msg'])
                                break
                            else:
                                print('密码不一致,请重试')
                else:
                    print('账号不存在')
            elif command == '6':
                print('项目地址:https://github.com/jellyqwq/class-helper')
                print('使用说明:https://blog.jellyqwq.com/archives/353')
            elif command == '7':
                os.system('cls') 
        break
    