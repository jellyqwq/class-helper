from class_helper import app, config
app.run(host=config['Host'], port=config['Port'], debug=True)