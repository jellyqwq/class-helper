from . import app, render_template, request, log, res, load_mongodb, origin

@app.route('/')
def index():
    log.debug(origin)
    mycol, DBEXIST, COLEXIST = load_mongodb()
    # 判断cookie是否存在
    cookie = request.cookies.to_dict()
    log.debug(cookie)
    if cookie == {}:
        # cookie为空登录页面
        return res(render_template('login.html', origin=origin))
    elif 'sh' in cookie.keys():
        # sh在cookie当中则提取sh并从数据库提取相关信息并生成表单
        sh = cookie['sh']
        log.debug('sh: %s', sh)
        count = mycol.count_documents({'cookie':sh})
        if count == 0:
            return res(render_template('login.html', origin=origin))
        else:
            info = mycol.find_one({'cookie':sh})
            # 功能开关状态
            switch_pushplus = switch_telegram = switch_weather = ''
            if info['switch_pushplus'] == 'true':
                switch_pushplus = 'checked'
            if info['switch_telegram'] == 'true':
                switch_telegram = 'checked'
            if info['switch_weather'] == 'true':
                switch_weather = 'checked'

            return res(render_template('config.html',
                        origin = origin,
                        user_name = info['name'],
                        openid = info['openid'],
                        xh = info['xh'],
                        tgtoken = info['telegram_bot_token'],
                        tg_user_id = info['telegram_user_id'],
                        pushplustoken = info['pushplustoken'],
                        switch_pushplus = switch_pushplus,
                        switch_telegram = switch_telegram,
                        switch_weather = switch_weather,
                        ))
    else:
        return res(render_template('login.html', origin = origin))

@app.route('/register')
def register():
    return res(render_template('register.html', origin = origin))
