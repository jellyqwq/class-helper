from class_helper import app, render_template, request, log, res, mycol, config

@app.route('/')
def index():
    # 判断cookie是否存在
    cookie = request.cookies.to_dict()
    log.debug(cookie)
    if cookie == {}:
        # cookie为空登录页面
        return res(render_template('login.html',
                    host = config['Host'],
                    port = config['Port']
                    ))
    elif 'sh' in cookie.keys():
        # sh在cookie当中则提取sh并从数据库提取相关信息并生成表单
        sh = cookie['sh']
        log.debug('sh: %s', sh)
        count = mycol.count_documents({'cookie':sh})
        if count == 0:
            return res(render_template('login.html',
                        host = config['Host'],
                        port = config['Port']
                        ))
        else:
            info = mycol.find_one({'cookie':sh})
            user_name = info['name']
            openid = info['openid']
            xh = info['xh']
            pushplustoken = info['pushplustoken']
            return res(render_template('config.html',
                        host = config['Host'],
                        port = config['Port'],
                        user_name = user_name,
                        openid = openid,
                        xh = xh,
                        pushplustoken = pushplustoken,
                        ))
    else:
        return res(render_template('login.html',
                    host = config['Host'],
                    port = config['Port']
                    ))
