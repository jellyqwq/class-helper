from . import app, render_template, request, log, res, load_mongodb

@app.route('/')
def index():
    mycol, DBEXIST, COLEXIST = load_mongodb()
    # 判断cookie是否存在
    cookie = request.cookies.to_dict()
    log.debug(cookie)
    if cookie == {}:
        # cookie为空登录页面
        return res(render_template('login.html'))
    elif 'sh' in cookie.keys():
        # sh在cookie当中则提取sh并从数据库提取相关信息并生成表单
        sh = cookie['sh']
        log.debug('sh: %s', sh)
        count = mycol.count_documents({'cookie':sh})
        if count == 0:
            return res(render_template('login.html'))
        else:
            info = mycol.find_one({'cookie':sh})
            # 功能开关状态
            switch_pushplus = switch_telegram = switch_weather = switch_pushplus_rightnow = switch_telegram_rightnow\
                 = data_hkxw = data_tzgg = data_mtbd = data_ldth = data_jwtz = data_kytz = ''
            if info['switch_pushplus'] == 'true':
                switch_pushplus = 'checked'
            if info['switch_telegram'] == 'true':
                switch_telegram = 'checked'
            if info['switch_weather'] == 'true':
                switch_weather = 'checked'
            if info['switch_pushplus_rightnow'] == 'true':
                switch_pushplus_rightnow = 'checked'
            if info['switch_telegram_rightnow'] == 'true':
                switch_telegram_rightnow = 'checked'
            if info['data_hkxw'] == 'true':
                data_hkxw = 'checked'
            if info['data_tzgg'] == 'true':
                data_tzgg = 'checked'
            if info['data_mtbd'] == 'true':
                data_mtbd = 'checked'
            if info['data_ldth'] == 'true':
                data_ldth = 'checked'
            if info['data_jwtz'] == 'true':
                data_jwtz = 'checked'
            if info['data_kytz'] == 'true':
                data_kytz = 'checked'

            return res(render_template('config.html',
                        user_name = info['name'],
                        openid = info['openid'],
                        xh = info['xh'],
                        tgtoken = info['telegram_bot_token'],
                        tg_user_id = info['telegram_user_id'],
                        pushplustoken = info['pushplustoken'],
                        switch_pushplus = switch_pushplus,
                        switch_telegram = switch_telegram,
                        switch_weather = switch_weather,
                        switch_pushplus_rightnow = switch_pushplus_rightnow,
                        switch_telegram_rightnow = switch_telegram_rightnow,
                        data_hkxw = data_hkxw,
                        data_tzgg = data_tzgg,
                        data_mtbd = data_mtbd,
                        data_ldth = data_ldth,
                        data_jwtz = data_jwtz,
                        data_kytz = data_kytz
                        ))
    else:
        return res(render_template('login.html'))

@app.route('/register')
def register():
    return res(render_template('register.html'))

@app.route('/forget')
def forget():
    return res(render_template('forget.html'))

@app.route('/delete')
def delete():
    return res(render_template('delete.html'))