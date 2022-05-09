from class_helper import app, render_template, request, log

@app.route('/')
def index():
    # 判断cookie是否存在
    cookie = request.cookies.to_dict()
    log.debug(cookie)
    if cookie == {}:
        return render_template('login.html')
    else:
        return render_template('index.html')
