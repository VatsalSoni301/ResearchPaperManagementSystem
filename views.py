
from home import app
from flask import render_template,request,redirect,url_for,session,flash,jsonify
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask_mail import Mail,Message
import random
import string
from flask_oauthlib.client import OAuth

from views_admin import *
from views_expert import *
from views_user import *

mysql = MySQL()
mysql.init_app(app)
mail = Mail(app)

GOOGLE_ID='180871412866-i8algb2ticev3q7kfb9k6m07pn3j0vvk.apps.googleusercontent.com'
GOOGLE_SECRET='8ZH4qN1t2-7dsJmGHn3LfDWU'

app.config['GOOGLE_ID'] = "180871412866-i8algb2ticev3q7kfb9k6m07pn3j0vvk.apps.googleusercontent.com"
app.config['GOOGLE_SECRET'] = "8ZH4qN1t2-7dsJmGHn3LfDWU"
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


#APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
	if 'role' in session:
		role=session['role']
		if role=='admin':
			return redirect(url_for('.admin_new'))
		elif role=='reviewer':
			return redirect(url_for('.paper_to_be_reviwed')) 
		elif role=='user':
			return redirect(url_for('.your_paper'))
	else:
		db = mysql.connect()
		cursor = db.cursor()
		user=0
		expert=0
		paper=0
		c=0
		cursor.execute("select count(*) from user_information")
		for raw in cursor.fetchall():
			user=raw[0]
		cursor.execute("select count(*) from expert_information")
		for raw in cursor.fetchall():
			expert=raw[0]
		cursor.execute("select count(*) from paper_creation")
		for raw in cursor.fetchall():
			paper=raw[0]
		arry=[{'day':'as','month':'as','desc':'sd'}]
		arry.clear()
		cursor.execute("select DAYOFMONTH(date_announcement),MONTHNAME(date_announcement),description from site_wide_announcement")
		for raw in cursor.fetchall():
			if c>=4:
				abc=0
			else:
				arry.append({'day':raw[0],'month':raw[1],'desc':raw[2]})
			c=c+1
		return render_template('index.html',u=user,p=paper,e=expert,arry=arry,c=c)

@app.route("/temp_t")
def temp_t():
	db = mysql.connect()
	cursor = db.cursor()
	user=0
	expert=0
	paper=0
	c=0
	cursor.execute("select count(*) from user_information")
	for raw in cursor.fetchall():
		user=raw[0]
	cursor.execute("select count(*) from expert_information")
	for raw in cursor.fetchall():
		expert=raw[0]
	cursor.execute("select count(*) from paper_creation")
	for raw in cursor.fetchall():
		paper=raw[0]
	arry=[{'day':'as','month':'as','title':'asdsa','desc':'sd'}]
	arry.clear()
	cursor.execute("select DAYOFMONTH(date_announcement),MONTHNAME(date_announcement),description from site_wide_announcement")
	for raw in cursor.fetchall():
		if c>=4:
			abc=0
		else:
			arry.append({'day':raw[0],'month':raw[1],'desc':raw[2]})
		c=c+1
	return render_template('index.html',u=user,p=paper,e=expert,arry=arry,c=c)
	
	
@app.route("/signin")
def signin():
	return render_template('signin.html')
	
@app.route("/editorial_guest")
def editorial_guest():
	db = mysql.connect()
	cursor = db.cursor()
	arry=[{'id':'1','fname':'abc','mname':'ds','lname':'sdada','desc':'sdsd','pic':'asa','designation':'ass'}]
	arry.clear()
	cursor.execute("select guest_id,first_name,middle_name,last_name,description,profile,designation from editorial_board")
	for raw in cursor.fetchall():
		arry.append({'id':raw[0],'fname':raw[1],'mname':raw[2],'lname':raw[3],'desc':raw[4],'pic':raw[5],'designation':raw[6]})
	return render_template('editorial_guest.html',arry=arry)	
	
@app.route("/editorial_expert")
def editorial_expert():
	db = mysql.connect()
	cursor = db.cursor()
	arry=[{'id':'1','fname':'abc','lname':'sdada','skill':'sdsd','exp':'asa'}]
	arry.clear()
	cursor.execute("select expert_id,first_name,last_name,skills,experience_in_words from expert_information")
	for raw in cursor.fetchall():
		arry.append({'id':raw[0],'fname':raw[1],'lname':raw[2],'skill':raw[3],'exp':raw[4]})
	return render_template('editorial_expert.html',arry=arry)	
	
@app.route("/CFP_Format")
def CFP_Format():
	db = mysql.connect()
	cursor = db.cursor()
	arry=[{'id':'1','track':'abc'}]
	arry.clear()
	x=1
	cursor.execute("select track_id,track_name from track")
	for raw in cursor.fetchall():
		arry.append({'id':x,'track':raw[1]})
		x=x+1
	return render_template('CFP_Format.html',arry=arry)	
	
@app.route("/contact_us")
def contact_us():
	return render_template('contact_us.html')	
	
@app.route("/contact_us_1",methods=['POST','GET'])
def contact_us_1():
	r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data = {'secret' :
                                  '6LdvCjAUAAAAAE7NvVAWoSxDJB5pR-X41M-_PHeh',
                                  'response' :
                                  request.form['g-recaptcha-response']})

        
	google_response = json.loads(r.text)
  
	if google_response['success']:
		name=request.form['name']
		email=request.form['email_ct']
		mobile=request.form['mobile']
		message=request.form['message']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("insert into contactus (mobile,email,message,name) values(%s,%s,%s,%s)",(mobile,email,message,name))
		db.commit()
		return redirect(url_for('.contact_us'))
	else:
		return "If you are not robot please go back and try again"
	
@app.route("/current_issue")
def current_issue():
	db = mysql.connect()
	cursor = db.cursor()
	id=0
	name=0
	issue=0
	issue_id=0
	a=1
	tt=[{'sr_no':'1','p_id':'1','title':'abc'}]
	tt.clear()
	user=[{'id':'1','auth':'sa'}]
	user.clear()
	cursor.execute("select MAX(volume_id),MAX(volume_name) from volume")
	for raw in cursor.fetchall():
		id=raw[0]
		name=raw[1]
	cursor.execute("select MAX(issue_no) from issue where volume_id=%s",id)
	for raw in cursor.fetchall():
		issue=raw[0]
	cursor.execute("select issue_id from issue where issue_no=%s and volume_id=%s",(issue,id))
	issue_id=cursor.fetchone()
	cursor.execute("select paper_id from paper_creation where issue_id=%s",issue_id)
	for raw in cursor.fetchall():
		cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
		x=cursor.fetchone()
		cursor.execute("select title from submission_of_paper where submission_id=%s",x)
		for raw1 in cursor.fetchall():
			tt.append({'sr_no':a,'p_id':raw[0],'title':raw1[0]})
		a=a+1
		
		cursor.execute("select user_id from paper_creation where paper_id=%s",raw[0])
		for raw1 in cursor.fetchall():
			u_id=raw1[0]
		
		

		cursor.execute("select first_name from user_information where user_id=%s",u_id)
		for raw1 in cursor.fetchall():
			u_name=raw1[0]
			
		
		user.append({'id':raw[0],'u_id':u_id,'auth':u_name})
		
		cursor.execute("select author_id from user_author where paper_id=%s",raw[0])
		for raw2 in cursor.fetchall():
			cursor.execute("select name from author where author_id=%s",raw2[0])
			for raw3 in cursor.fetchall():
				user.append({'id':raw[0],'u_id':raw2[0],'auth':raw3[0]})
			
			
			
	# cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",13)
	# x=cursor.fetchone()
	# cursor.execute("select title from submission_of_paper where submission_id=%s",x)
	# for raw7 in cursor.fetchall():
		# tt1.append({'sr_no':a,'p_id':13,'title':raw7[0]})

			
	return render_template('current_issue.html',user=user,id=id,name=name,issue=issue,tt=tt)

@app.route('/current_issue_id',methods=['POST'])
def current_issue_id():
			title=0
			t1=0
			abstract=0
			id=request.form['pap']			
			# tt12=[{'p_id':'1','title':'abc','abstract':'x'}]
			# tt12.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id)
			x=cursor.fetchone()
			cursor.execute("select title,abstract from submission_of_paper where submission_id=%s",x)
			for raw in cursor.fetchall():
				title=raw[0]
				abstract=raw[1]
				# tt12.append({'p_id':id,'title':raw[0],'abstract':raw[1]})
			t1=title+"~"+abstract
			
			return t1
			# return render_template('current_issue_id.html',title=title,abstract=abstract)	
	
	
@app.route("/previous_issues")
def previous_issues():
			arr=[{'id':'1','name':'f','issue_id':'0'}]
			arr.clear()
			arr1=[{'id':'1','name':'f','volume':'x'}]
			arr1.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from volume")
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'name':raw[1]})
				cursor.execute("select * from issue where volume_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					arr1.append({'id':raw1[0],'name':raw1[1],'issue_id':raw1[3],'volume':raw[0]})
				
			return render_template('previous_issues.html',arr1=arr1,arr=arr)	
			
@app.route("/home_issue_paper_list")
def home_issue_paper_list():
	issue_id= request.args.get('i_id', default='', type=str)
	db = mysql.connect()
	cursor = db.cursor()
	id=0
	name=0
	issue=0
	a=1
	tt=[{'sr_no':'1','p_id':'1','title':'abc'}]
	tt.clear()
		
	user=[{'id':'1','auth':'sa'}]
	user.clear()
	cursor.execute("select volume_id,issue_no from issue where issue_id=%s",issue_id)
	for raw in cursor.fetchall():
		id=raw[0]
		issue=raw[1]
	cursor.execute("select volume_name from volume where volume_id=%s",id)
	for raw9 in cursor.fetchall():
		name=raw9[0]
	# cursor.execute("select MAX(issue_no) from issue where volume_id=%s",id)
	# for raw in cursor.fetchall():
		# issue=raw[0]
	# cursor.execute("select issue_id from issue where issue_no=%s and volume_id=%s",(id,issue))
	# for raw in cursor.fetchall():
		# issue_id=raw[0]
	cursor.execute("select paper_id from paper_creation where issue_id=%s",issue_id)
	for raw in cursor.fetchall():
		cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
		x=cursor.fetchone()
		cursor.execute("select title from submission_of_paper where submission_id=%s",x)
		for raw1 in cursor.fetchall():
			tt.append({'sr_no':a,'p_id':raw[0],'title':raw1[0]})
		a=a+1
		
		
		cursor.execute("select user_id from paper_creation where paper_id=%s",raw[0])
		for raw1 in cursor.fetchall():
			u_id=raw1[0]
		
		

		cursor.execute("select first_name from user_information where user_id=%s",u_id)
		for raw1 in cursor.fetchall():
			u_name=raw1[0]
			
		
		user.append({'id':raw[0],'u_id':u_id,'auth':u_name})
		
		cursor.execute("select author_id from user_author where paper_id=%s",raw[0])
		for raw2 in cursor.fetchall():
			cursor.execute("select name from author where author_id=%s",raw2[0])
			for raw3 in cursor.fetchall():
				user.append({'id':raw[0],'u_id':raw2[0],'auth':raw3[0]})
		
	
			
					
	return render_template('home_issue_paper_list.html',user=user,id=id,name=name,issue=issue,tt1=tt)


@app.route("/user_sign_up")
def user_sign_up():	
		cn=[{'name':'abc'}]
		cn.clear()
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select countryName from countries order by countryName ASC")
		for raw in cursor.fetchall():
			cn.append({'name':raw[0]})
		return render_template('user_sign_up.html',c=cn)
	
# @app.route("/user_signup")
# def user_signup():
		# cn=[{'name':'abc'}]
		# cn.clear()
		# db = mysql.connect()
		# cursor = db.cursor()
		# cursor.execute("select countryName from countries order by countryName ASC")
		# for raw in cursor.fetchall():
			# cn.append({'name':raw[0]})
		# return render_template('user_signup.html',c=cn)

@app.route('/user_signup_1', methods=['POST'])
def user_signup_1():
		destination='temp'
		for f in request.files.getlist("file"):
			if f.filename == '':
				destination="Default.jpg"
			else:
				target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
				filename=f.filename
				ext=filename.split(".")
				destination = "/".join([target,filename])
				f.save(destination)
				destination=filename
		dd=datetime.utcnow()
		first = request.form['fname']
		middle=''
		last = request.form['lname']
		gender = request.form['gn']
		email = request.form['email']
		mobile = request.form['mobile']
		password = request.form['password']
		add_1=request.form['address_1']
		add_2=request.form['address_2']
		add_3=request.form['address_3']
		pincode=request.form['pincode']
		if pincode == '':
			pincode=0
		country=request.form['country']
		dob = request.form['date'] 
		designation = request.form['designation']
		biodata = request.form['biodata']
		salution = request.form['salution']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select * from user_information where email_id=%s",email)
		x=0
		for raw in cursor.fetchall():
			x=x+1
		if x>0:
			return "Email Already Exist"
		else:
			cursor.execute("""insert into user_information (first_name,middle_name,last_name,mobile_no,email_id,password,date_of_birth,gender,biodata,designation,profile_pic,date_registration,address_1,address_2,address_3,pincode,country,salution) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (first,middle,last,mobile,email,password,dob,gender,biodata,designation,destination,dd,add_1,add_2
			,add_3,pincode,country,salution))
			db.commit()
			return redirect(url_for('.index'))	
		
	
@app.route("/signin_1",methods=['POST'])
def signin_1():
	Email = request.form['email']
	Pass = request.form['password']
	role = request.form['role']
	arr=['a']
	db = mysql.connect()
	cursor = db.cursor()
	if role=='admin':
		cursor.execute("SELECT * FROM admin_information where email_id=%s and password=%s;", (Email,Pass))
		for raw in cursor.fetchall():
				arr=raw
		if arr[0] =='a':
			return "wrong"
		else:
			return "success"
	elif role=='expert':
		cursor.execute("SELECT * FROM expert_information where email_id=%s and password=%s;", (Email,Pass))
		for raw in cursor.fetchall():
				arr=raw
		if arr[0] =='a':
			return "wrong"
		else:
			return "success"
	elif role=='user':
		cursor.execute("SELECT * FROM user_information where email_id=%s and password=%s;", (Email,Pass))
		for raw in cursor.fetchall():
				arr=raw
		if arr[0] =='a':
			return "wrong"
		else:
			return "success"
		
otp=0
Email=''
role=''
		
@app.route("/temp",methods=['POST'])
def temp():
	return render_template('forgot1.html')
		
@app.route("/verify",methods=['POST'])
def verify():
		global role
		global Email
		role = request.form['role']
		Email = request.form['email']
		c=0
		db = mysql.connect()
		cursor = db.cursor()
		if role=='admin':
			cursor.execute("select * from admin_information where email_id=%s",Email)
			for raw in cursor.fetchall():
				c=c+1
		elif role=='expert':
			cursor.execute("select * from expert_information where email_id=%s",Email)
			for raw in cursor.fetchall():
				c=c+1
		elif role=='user':
			cursor.execute("select * from user_information where email_id=%s",Email)
			for raw in cursor.fetchall():
				c=c+1
		if c>0:
			msg = Message('Hello', sender = 'harshitus99@gmail.com', recipients = [Email])
			global otp
			otp = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
			msg.body=otp
			mail.send(msg)
			return "success"
		else:
			return "wrong"
	
@app.route("/temp_1",methods=['POST'])
def temp_1():
	role = request.form['role']
	Email = request.form['email']
	Pass = request.form['password']
	
	if role=='expert':
		return redirect(url_for('.signin_expert',Email=Email,Pass=Pass))
	elif role=='user':
		return redirect(url_for('.signin_user',Email=Email,Pass=Pass))
	
@app.route("/temp_111",methods=['POST'])
def temp_111():
	
	Email = request.form['email']
	Pass = request.form['password']
	return redirect(url_for('.signin_admin',Email=Email,Pass=Pass))

	
@app.route("/password")
def password():
		return render_template('forgot.html')
@app.route("/verify1",methods=['POST'])
def verify1():
		msg = request.form['otp']
		if msg==otp:
			return render_template('set_new_password.html')
		else:
			return "OTP is not valid"
			
@app.route("/set_pass",methods=['POST'])
def set_pass():
		password = request.form['password']
		db = mysql.connect()
		cursor = db.cursor()
		if role=='admin':
			cursor.execute("update admin_information set password=%s where email_id=%s",(password,Email))
		elif role=='expert':
			cursor.execute("update expert_information set password=%s where email_id=%s",(password,Email))
		elif role=='user':
			cursor.execute("update user_information set password=%s where email_id=%s",(password,Email))
		db.commit()
		return redirect(url_for('.signin'))
		
@app.route('/validate_email_user',methods=['POST'])
def validate_email_user():
		
		email = request.form['email']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select * from user_information where email_id=%s",email)
		x=0
		for raw in cursor.fetchall():
			x=x+1
		if x>0:
			return "wrong"
		else:
			return "success"
		
@app.route('/google')
def index1():
    if 'google_token' in session:
        me = google.get('userinfo')
        #return jsonify({"data": me.data})
    return redirect(url_for('login1'))
 

@app.route('/login')
def login1():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout1():
    session.pop('google_token', None)
    return redirect(url_for('index1'))


@app.route('/login/authorized')
def authorized():
		resp = google.authorized_response()
		if resp is None:
			return 'Access denied: reason=%s error=%s' % (
				request.args['error_reason'],
				request.args['error_description']
			)
		session['google_token'] = (resp['access_token'], '')
		me = google.get('userinfo')
		email=me.data['email']
		destination=me.data['picture']
		
		fname=me.data['given_name']
		lname=me.data['family_name']
		dd=datetime.utcnow()
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select * from user_information where email_id=%s",email)
		c=0
		for raw in cursor.fetchall():
			c=c+1
		if c>0:
			return redirect(url_for('.signin_user_google',Email=email,fname=fname,lname=lname))
		
		else:
			cursor.execute("""insert into user_information (first_name,middle_name,last_name,mobile_no,email_id,password,date_of_birth,gender,biodata,designation,profile_pic,date_registration,address_1,address_2,address_3,pincode,country) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (fname,"","","",email,"","","","","",destination,dd,"",""
			,"",0,""))
			db.commit()
			return redirect(url_for('.signin_user_google',Email=email,fname=fname,lname=lname))
		
@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')	
		
@app.route("/search")
def search():
	return redirect(url_for('.signin'))
	

@app.route("/read_more")
def read_more():
		arry=[{'day':'as','month':'as','desc':'sd'}]
		arry.clear()
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select DAYOFMONTH(date_announcement),MONTHNAME(date_announcement),description from site_wide_announcement")
		for raw in cursor.fetchall():
			arry.append({'day':raw[0],'month':raw[1],'desc':raw[2]})		
		return render_template('read_more.html',arry=arry)


@app.route("/join_as_expert")
def join_as_expert():
	return render_template('join_as_expert.html')

@app.route('/join_as_expert_1', methods=['POST'])
def join_as_expert_1():
		
		destination='temp'
		cv='temp'
		db = mysql.connect()
		cursor = db.cursor()
		for f in request.files.getlist("file"):
			if f.filename == '':
				destination='Default.jpg'
			else:
				target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
				filename=f.filename 
				destination = "/".join([target,filename])
				f.save(destination)
				destination=filename
		for f1 in request.files.getlist("cv"):
			if f1.filename == '':
				cv=''
			else:
				target1=os.path.join('/home/tp/python_flask/Research_Paper/static','Expert_CV/')
				filename1=f1.filename
				cv = "/".join([target1,filename1])
				f1.save(cv)
				cv=f1.filename
		dd=datetime.utcnow()
		first = request.form['fname']
		middle = request.form['mname']
		last = request.form['lname']
		gender = request.form['gn']
		email = request.form['email']
		mobile = request.form['mobile']
		password = request.form['password']
		skill = request.form['skill']
		dob = request.form['date'] 
		exp = request.form['experience']
		exp_words = request.form['experience_words']
			
		cursor.execute("""insert into expert_information (first_name,middle_name,last_name,mobile_no,email_id,password,date_of_birth,gender,skills,total_experience,experience_in_words,profile_pic,date_registration,expert_cv) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (first,middle,last,mobile,email,password,dob,gender,skill,exp,exp_words,destination,dd,cv))
		db.commit()
		return redirect(url_for('.join_as_expert'))

@app.route("/searchGlobalLink",methods=['POST','GET'])
def searchGlobalLink():
	search=request.form['search']
	global arr
	arr=[]
	global x
	if search!='':
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select paper_id from paper_creation")
		for raw6 in cursor.fetchall():
			id6=raw6[0]
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id6)
			for raw7 in cursor.fetchall():
				id7=raw7[0]
				cursor.execute("select distinct paper_id from submission_of_paper where submission_id=%s and title like %s",(id7,"%" + search + "%",))
				for raw in cursor.fetchall():
					id1=raw[0]
					cursor.execute("select paper_id,issue_id from paper_creation where paper_id=%s and issue_id is not null",id1)
					for raw3 in cursor.fetchall():
						id=raw3[0]
						i_id=raw3[1]
						cursor.execute("select volume_id from issue where issue_id=%s",i_id)
						for raw4 in cursor.fetchall():
							cursor.execute("select volume_name from volume where volume_id=%s",raw4[0])
							for raw5 in cursor.fetchall():
								v_id=raw5[0]
								
						cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id)
						for raw2 in cursor.fetchall():
							cursor.execute("select title,last_modified_date from submission_of_paper where submission_id=%s",raw2[0])
							for raw1 in cursor.fetchall():
								arr.append({'id':id,'title':raw1[0],'date':raw1[1],'i_id':i_id,'v_id':v_id})
								#print(arr)
			
	if not arr:
		x='true'
	else:
		x='false'
	return render_template("home_search.html")

@app.route("/searchGlobalLink1",methods=['POST','GET'])
def searchGlobalLink1():
	global arr
	global x
	print(x)
	return render_template("home_search.html",k=arr,x=x)