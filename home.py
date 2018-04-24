from flask import Flask

#pip install flask-mysql

app=Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
from views import *
# from views_admin import *
# from views_expert import *
# from views_user import *

	
if __name__=='__main__':
	app.run(port=5000,debug=False,threaded=True,host="0.0.0.0")