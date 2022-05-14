from class_helper import app, config
if config['HTTPS'] == True:
    app.run(host=config['RunHost'], port=config['RunPort'], debug=True, ssl_context=("class.jellyqwq.com_bundle.pem", "class.jellyqwq.com.key"))
else:
    app.run(host=config['RunHost'], port=config['RunPort'], debug=True)