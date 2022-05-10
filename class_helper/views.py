from class_helper import app, render_template, request, log, res, mycol

@app.route('/')
def index():
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
             return res(render_template('config.html'))
    else:
        return res(render_template('login.html'))
