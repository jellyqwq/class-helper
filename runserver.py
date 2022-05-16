from class_helper import app, config
app.run(host=config['RunHost'], port=config['RunPort'], debug=True)