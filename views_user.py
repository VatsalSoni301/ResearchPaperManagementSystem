from home import app
from flask import render_template,request,redirect,url_for,session,flash
#from mysql import MySQL
from flaskext.mysql import MySQL
from datetime import datetime
import os
import requests
import json
import itertools
import re
#from flask_recaptcha import ReCaptcha


mysql = MySQL()
mysql.init_app(app)

app.config.update({'RECAPTCHA_ENABLED': True,
                   
                   'RECAPTCHA_SECRET_KEY':
                       '6LdvCjAUAAAAAE7NvVAWoSxDJB5pR-X41M-_PHeh'})


#recaptcha = ReCaptcha(app=app)


#APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/user')
def user():
		return render_template("signin.html")
		
@app.route('/signout_user')
def signout_user():
		session.pop('id', None)
		session.pop('role', None)
		session.pop('name', None)
		session.pop('img', None)
		return redirect(url_for('.index'))	

@app.route('/signin_user')
def signin_user():
		arr=['a']
		Email = request.args['Email']
		Pass = request.args['Pass']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("SELECT * FROM user_information where email_id=%s and password=%s;", (Email,Pass))
		for raw in cursor.fetchall():
				arr=raw
		if arr[0] =='a':
			return "Unauthorized User"
		else:
			session['id'] = arr[0]
			session['name'] = arr[1] + " " + arr[3]
			session['img'] = arr[11]	
			session['role'] = 'user'
			return redirect(url_for('.your_paper'))	

@app.route('/signin_user_google')
def signin_user_google():
		arr=['a']
		Email = request.args['Email']
		fname = request.args['fname']
		lname = request.args['lname']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("SELECT password FROM user_information where email_id=%s", Email)
		for raw in cursor.fetchall():
			password=raw[0]
		if password=='':
			return render_template("google_inter.html",Email=Email,fname=fname,lname=lname)
		else:
			return redirect(url_for('.signin_user',Email=Email,Pass=password))
			
@app.route('/google_intermediate',methods=['POST'])
def google_intermediate():	
		db = mysql.connect()
		cursor = db.cursor()
		Email=request.args.get('email', default='', type=str)
		#print(email)
		gender=request.form['gn']
		middle=request.form['middle']
		last=request.form['last']
		mobile=request.form['mobile']
		password=request.form['password']
		date=request.form['date']
		designation=request.form['designation']
		cursor.execute("update user_information set gender=%s,middle_name=%s,last_name=%s,mobile_no=%s,password=%s,date_of_birth=%s,designation=%s where email_id=%s",(gender,middle,last,mobile,password,date,designation,Email))
		db.commit()
		return redirect(url_for('.signin_user',Email=Email,Pass=password))
			
@app.route('/user_home')  
def user_home():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			fname=session['name']
			img=session['img']
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_home.html",fname=fname,img=img,c=count,arr=arrx)			
			
	
def notify_user(arr):
		id=session['id']
		c=0
		d=0
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("Select n_id from user_notification where user_id=%s",id)
		for raw in cursor.fetchall():
			if raw[0]==3:
				c=c+1
			if raw[0]==6:
				d=d+1
		if c>0:
			arr.append({'time':c,'type':3,'message':'Reviewer has commented on a Paper.'})
		if d>0:
			arr.append({'time':d,'type':6,'message':'Admin has published your paper'})
		return arr
		
def noticount_user():
		count=0
		id=session['id']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("Select n_id from user_notification where user_id=%s",id)
		for raw in cursor.fetchall():
			count=count+1
		return count
	
@app.route('/validate_email_user_1',methods=['POST'])
def validate_email_user_1():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			email = request.form['email']
			email1=''
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select email_id from user_information where user_id=%s",id)
			for raw in cursor.fetchall():
				email1=raw[0]
			if email1==email:
				return "success"
			else:
				cursor.execute("select * from user_information where email_id=%s",email)
				x=0
				for raw in cursor.fetchall():
					x=x+1
				if x>0:
					return "wrong"
				else:
					return "success"
	
@app.route('/User_Personal_Info')  
def user_pi():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			fname=session['name']
			img = session['img']
			cn=[{'name':'abc'}]
			cn.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select countryName from countries order by countryName ASC")
			for raw in cursor.fetchall():
				cn.append({'name':raw[0]})
			cursor.execute("Select * from user_information where user_id=%s",id)
			arr=['a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a','a']
			arr.clear()
			for raw in cursor.fetchall():
				arr=raw
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("pi_user.html",name="User",k=arr,fname=fname,img=img,c=count,arr=arrx,cn=cn)
			
@app.route('/pi_user1', methods=['POST']) 
def pi_user1():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			img = session['img']
			destination='temp'
		
			for f in request.files.getlist("file"):
				if f.filename == '':
					break
				else:
					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
					filename=f.filename			
					destination = "/".join([target,filename])
					f.save(destination)
					img=f.filename
					session['img']=img
		
			country=request.form['country']
			first = request.form['fname']
			middle = request.form['mname']
			last = request.form['lname']
			session['name'] = first + " " + last
			gender = request.form['gn'] 
			email = request.form['email']
			mobile = request.form['mobile']
			address_1 = request.form['address_1']
			address_2 = request.form['address_2']
			address_3 = request.form['address_3']
			pincode = request.form['pincode']
			biodata = request.form['biodata']
			current = request.form['designation']
			dob = request.form['date'] 
			db = mysql.connect()
			cursor = db.cursor()
		
			cursor.execute('''update user_information set first_name=%s,middle_name=%s,last_name=%s,mobile_no=%s,email_id=%s,date_of_birth=%s,gender=%s,address_1=%s,address_2=%s,address_3=%s,biodata=%s,designation=%s,profile_pic=%s,pincode=%s,country=%s where user_id=%s''', (first,middle,last,mobile,email,dob,gender,address_1,address_2,address_3,biodata,current,img,pincode,country,id))
			db.commit()
			return redirect(url_for('.user_pi'))
		

@app.route('/your_paper')	
def your_paper():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img = session['img']
			arr=[{'topic':'shyam','creation_date':'asd','last':'asd','status':'asasd','pap_id':'1'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from paper_creation where user_id=%s",s_id)
			nn=0
			for raw in cursor.fetchall():
				cursor.execute("Select status_name,creation_date from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
				for raw2 in cursor.fetchall():
					id1=raw2[0]
					id2=raw2[1]
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					nn=1
					arr.append({'topic':raw1[0],'creation_date':id2,'last':raw1[1],'status':id1,'pap_id':raw[0]})
				
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_list_papers.html",name="List Of Papers",k=arr,fname=fname,img=img,c=count,arr=arrx,nos=nn)

	
@app.route('/submit_paper')	
def submit_paper():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img = session['img']
			arr3=[{'id':'1','name':'aaas'}]
			arr10=[{'id':'1','name':'aaas'}]
			arr4=[{'id':'1','name':'aaas'}]
			arr2=[{'id':'1','name':'jkj'}]
			arr2.clear()
			arr10.clear()
			arr3.clear()
			arr4.clear()
			a_name=0
			db = mysql.connect()
			cursor = db.cursor()
			
			cursor.execute("""select author_id,name from author where user_id=%s""",s_id)
			for raw in cursor.fetchall():
				arr10.append({'id':raw[0],'name':raw[1]})
				
			# cursor.execute("""select * from keyword""")
			# for raw in cursor.fetchall():
			# 	arr2.append({'id':raw[0],'name':raw[1]})
			cursor.execute("select * from subject")
			for raw in cursor.fetchall():
				arr3.append({'id':raw[0],'name':raw[1]})
			cursor.execute("select * from track")
			for raw in cursor.fetchall():
				arr4.append({'id':raw[0],'name':raw[1]})
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("Submit_Paper.html",name="Paper Submission",a_name=a_name,arr10=arr10,arr2=arr2,arr3=arr3,arr4=arr4,fname=fname,img=img,arr=arrx,c=count)

@app.route('/author_details',methods=['POST'])	
def author_details():	
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img = session['img']
			
			a_name = request.form['name']
			email = request.form['email']
			designation = request.form['designation']
			# institute = request.form['institute']
			department = request.form['department']
			city = request.form['city']
			country = request.form['country']	
			
			arr12=[{'id':'1','name':'jkj'}]
			arr12.clear()
			id=0
			name=0
			db = mysql.connect()
			cursor = db.cursor()
						
			cursor.execute("""insert into author (name,email,designation,city,country,department) values(%s,%s,%s,%s,%s,%s)""", (a_name,email,designation,city,country,department))	
			cursor.execute("""select * from author""")
			for raw in cursor.fetchall():
				id=raw[0]
				name=raw[1]
				# arr12.append({'id':raw[0],'name':raw[1]})
				arr=str(id)+"~"+name
			db.commit()	
			return arr
	
	# return render_template("author_details.html",arr12=arr12)


@app.route('/delete_author',methods=['POST'])	
def delete_author():
		if 'id' not in session:
			return render_template("signin.html")
		else:	
			s_id = session['id']
			a_id=request.form['a_id']
			
			db = mysql.connect()
			cursor = db.cursor()
			
			cursor.execute("delete from author where author_id=%s",a_id)
			db.commit()
			return "DELETED"
			# return redirect(url_for('.author_details'))	
			
@app.route('/update_author_details',methods=['POST'])	
def update_author_details():
		if 'id' not in session:
			return render_template("signin.html")
		else:	
			s_id = session['id']
			a_id=request.form['a_id']
			
			
			a_name=0
			email=0
			designation=0
			city=0
			country=0
			department=0
			db = mysql.connect()
			cursor = db.cursor()
			
			cursor.execute("""select * from author where author_id=%s """,a_id)
			for raw in cursor.fetchall():
				a_id=raw[0]
				a_name=raw[1]
				email=raw[2]
				designation=raw[3]
				city=raw[4]
				country=raw[5]
				department=raw[6]
			d=str(a_id)+"~"+a_name +"~"+ email+"~"+  designation +"~"+ city +"~"+ country +"~"+ department
			print(d)
			return d		


@app.route('/update_author_details_1',methods=['POST'])	
def update_author_details_1():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img = session['img']
			a_id = request.form['a_id']
			a_name = request.form['name']
			email = request.form['email']
			designation = request.form['designation']
			# institute = request.form['institute']
			department = request.form['department']
			city = request.form['city']
			country = request.form['country']	
			
			db = mysql.connect()
			cursor = db.cursor()
			
			cursor.execute("update author set name=%s,email=%s,designation=%s,city=%s,country=%s,department=%s where author_id=%s",(a_name,email,designation,city,country,department,a_id))
			db.commit()
			d1=str(a_id)+"~"+a_name
			return d1

			
@app.route('/submit_paper_1', methods=['POST'])	
def submit_paper_1():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			destination='temp'
			paper_path=''
			r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data = {'secret' :
                                  '6LdvCjAUAAAAAE7NvVAWoSxDJB5pR-X41M-_PHeh',
                                  'response' :
                                  request.form['g-recaptcha-response']})

        
			google_response = json.loads(r.text)
  
			if google_response['success']:
            
				for f in request.files.getlist("file"):

					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Paper/')
					filename=f.filename
					ext=filename.split(".")
					destination = "/".join([target,filename])
					f.save(destination)
					paper_path=f.filename
					
				primary_author=request.form['pauthor']
				aa=[]
				author1=request.form['author1']
				author2=request.form['author2']
				author3=request.form['author3']
				author4=request.form['author4']
				aa.append(author1)
				aa.append(author2)
				aa.append(author3)
				aa.append(author4)

				
				dd=datetime.utcnow()
				title = request.form['title']
				track = request.form['track']
				sub=request.form['subject']

				kk=[]
				key1=request.form['keyword1']
				key2=request.form['keyword2']
				key3=request.form['keyword3']
				key4=request.form['keyword4']
				key5=request.form['keyword5']
				kk.append(key1)
				kk.append(key2)
				kk.append(key3)
				kk.append(key4)
				kk.append(key5)
				abstract=request.form['abstract']
			
				
				db = mysql.connect()
				cursor = db.cursor()
				
							
				cursor.execute("""insert into paper_creation (user_id,creation_date,path,status_allocation,status_id) values(%s,%s,%s,%s,%s)""", (id,dd,paper_path,'false','1'))
				cursor.execute("select MAX(paper_id) from paper_creation")
				p_id=cursor.fetchone()
				cursor.execute("""insert into submission_of_paper (paper_id,title,track_id,abstract,last_modified_date,path,subject_id) values(%s,%s,%s,%s,%s,%s,%s)""", (p_id,title,track,abstract,dd,paper_path,sub))
				cursor.execute("select MAX(submission_id) from submission_of_paper")
				s_id=cursor.fetchone()
				
				for k in aa:
					if k==primary_author:
						var='yes'
					else:
						var='no'
					cursor.execute("""insert into user_author (author_id,paper_id,user_id,primary_author) values(%s,%s,%s,%s)""",(k,p_id,id,var))
				
				for k in kk:
					cursor.execute("""insert into paper_keyword (submission_id,paper_id,keyword_name) values(%s,%s,%s)""",(s_id,p_id,k))
				cursor.execute("insert into admin_notification (n_id) values(%s)",4)
				
				db.commit()
				return redirect(url_for('.your_paper'))
			
			else:
				return "If you are not robot please go back and try again"
			
			
					
@app.route('/edit_paper_01')	
def edit_paper_01():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			p_id= request.args.get('p_id', default='', type=str)
			s_id = session['id']
			fname=session['name']
			img = session['img']
			arrxy=[{'id':'1','name':'aaas'}]
			arr4=[{'id':'1','name':'aaas'}]
			key=[]
			arr=['a','a','a']
			arr2=[{'id':'1','name':'jkj'}]
			arr.clear()
			arr2.clear()
			arrxy.clear()
			arr4.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
			si=cursor.fetchone()
			cursor.execute("select track_id from submission_of_paper where submission_id=%s",si)
			tt=cursor.fetchone()
			# cursor.execute("""select * from keyword where track_id=%s""",tt)
			# for raw in cursor.fetchall():
			# 	arr2.append({'id':raw[0],'name':raw[1]})
			# cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
			id=si
			cursor.execute("Select * from submission_of_paper where submission_id=%s",id)
			for raw in cursor.fetchall():
				arr=raw
			# cursor.execute("Select keyword_name from keyword,paper_keyword where keyword.keyword_id=paper_keyword.keyword_id and submission_id=%s ",(id))
			# for i in cursor.fetchall():
			# 	key.append({'name':i[0]})
			cursor.execute("select keyword_name from paper_keyword where paper_id=%s and submission_id=%s",(p_id,id))
			for raw in cursor.fetchall():
				key.append(raw[0])
			cursor.execute("select * from subject where track_id=%s",tt)
			for raw in cursor.fetchall():
				arrxy.append({'id':raw[0],'name':raw[1]})
			cursor.execute("select * from track")
			for raw in cursor.fetchall():
				arr4.append({'id':raw[0],'name':raw[1]})
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()	
			return render_template("edit_Submitted_Paper.html",name="Edit Submitted paper",arr2=arr2,arr=arr,keyw=key,arrxy=arrxy,arr4=arr4,fname=fname,p_id=p_id,img=img,arr5=arrx,c=count)

@app.route('/edit_paper_1',methods=['POST'])	
def edit_paper_1():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			p_id= request.args.get('p_id', default='', type=str)
		
			db = mysql.connect()
			cursor = db.cursor()
			destination='temp'
			for f in request.files.getlist("file"):
				if f.filename == '':
					cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
					for raw in cursor.fetchall():
						ss=raw[0]
						cursor.execute("select path from submission_of_paper where submission_id=%s",ss)
						for raw1 in cursor.fetchall():
							paper_path=raw1[0]
					break
				else:
					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Paper/')
					filename=f.filename
					ext=filename.split(".")
					destination = "/".join([target,filename])
					f.save(destination)
					paper_path=f.filename

			key1 = request.form['keyword1']
			key2 = request.form['keyword2']
			key3 = request.form['keyword3']
			key4 = request.form['keyword4']
			key5 = request.form['keyword5']
			kk=[1,2,3,4,5]
			kk.clear()
			kk.append(key1)
			kk.append(key2)
			kk.append(key3)
			kk.append(key4)
			kk.append(key5)
		
			dd=datetime.utcnow()
			title = request.form['title']
			track = request.form['track']
			sub = request.form['subject']
			abstract=request.form['abstract']
			cursor = db.cursor()
			cursor.execute("""insert into submission_of_paper (paper_id,title,track_id,abstract,last_modified_date,path,subject_id) values(%s,%s,%s,%s,%s,%s,%s)""", (p_id,title,track,abstract,dd,paper_path,sub))
			cursor.execute("select MAX(submission_id) from submission_of_paper")
			s_id=cursor.fetchone()
			for k in kk:
				cursor.execute("""insert into paper_keyword (submission_id,paper_id,keyword_name) values(%s,%s,%s)""",(s_id,p_id,k))
			cursor.execute("insert into admin_notification (n_id) values(%s)",(2))
			cursor.execute("select expert_id from expert_comment where paper_id=%s and status_id=%s",(p_id,6))
			for raw in cursor.fetchall():
				cursor.execute("insert into expert_notification (expert_id,n_id) values(%s,%s)",(raw[0],2))
			db.commit()
			return redirect(url_for('.list_paper_comment'))	
		

@app.route('/announcements')	
def announcements():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			fname=session['name']
			img = session['img']
			arr=[{'name':'as','date':'21'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select announcement_details,announcements_date from announcement where related_to like %s order by announcements_date DESC",'%User%')
			for raw in cursor.fetchall():
				arr.append({'name':raw[0],'date':raw[1]})
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_announcement.html",name="Announcement",arr1=arr,fname=fname,img=img,arr=arrx,c=count)


@app.route('/list_paper_comment')	
def list_paper_comment():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img = session['img']
			arr=[{'topic':'shyam','status':'asasd','pap_id':'1','c_date':'122','last':'123'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from paper_creation where user_id=%s and status_id not in(%s,%s,%s,%s)",(s_id,1,7,8,9))
			#cursor.execute("Select paper_id from paper_creation where user_id=%s and status_id=%s",(s_id,7))
			
			for raw in cursor.fetchall():
				
				cursor.execute("Select status_name,creation_date from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
				for raw2 in cursor.fetchall():
					id1=raw2[0]
					id2=raw2[1]
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					arr.append({'topic':raw1[0],'status':id1,'pap_id':raw[0],'c_date':id2,'last':raw1[1]})
				
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("list_paper_comment.html",name="List Of Papers",k=arr,fname=fname,img=img,arr=arrx,c=count)

			
# @app.route('/comment_view')	
# def comment_view():
		# p_id= request.args.get('p_id', default='', type=str)
		# id = session['id']
		# if id=='':
			# return render_template("signin.html")
		# else:
			# fname=session['name']
			# arr=[{'title':'harsh','date':'s','msg':'s'}]
			# arr.clear()
			# cursor = db.cursor()
			# cursor.execute("Select MAX(submission_id) from expert_comment where paper_id=%s",p_id)
			# for raw in cursor.fetchall():
				# cursor.execute("Select title from submission_of_paper where submission_id=%s",raw[0])
				# for raw1 in cursor.fetchall():
					# title=raw1[0]
				
				# cursor.execute("Select date_of_comment,comment_message from expert_comment where paper_id=%s order by date_of_comment DESC",p_id)
				# for raw2 in cursor.fetchall():
					# arr.append({'title':title,'date':raw2[0],'msg':raw2[1]})
				
			# return render_template("comment_view.html",name="List Of Comments",k=arr,j=arr1,fname=fname,p_id=p_id)

@app.route('/paper_view_click')	
def paper_view_click():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			p_id= request.args.get('p_id', default='', type=str)
			sub_id= request.args.get('sub_id', default='', type=str)
			i_id= request.args.get('i_id', default='', type=str)
			search= request.args.get('search', default='', type=str)
			mode= request.args.get('mode', default='', type=str)
			s_id=session['id']
			fname=session['name']
			idd='0'
			img = session['img']
			key=[{'name':'hgh'}]
			key.clear();
			arr=['a']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
			idd=cursor.fetchone()
			cursor.execute("select * from submission_of_paper where submission_id=%s",idd)
			for raw in cursor.fetchall():
				arr=raw
			cursor.execute("Select keyword_name from paper_keyword where paper_id=%s and submission_id=%s",(p_id,idd))
			for i in cursor.fetchall():
				key.append({'name':i[0]})
			cursor.execute("select track_name from track,submission_of_paper where submission_of_paper.track_id=track.track_id and submission_id=%s",idd)
			for r in cursor.fetchall():
				track=r[0]
			cursor.execute("select subject_name from subject,submission_of_paper where submission_of_paper.subject_id=subject.subject_id and submission_id=%s",idd)
			for s in cursor.fetchall():
				sub=s[0]
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("paper_view_click.html",name="View Paper",search=search,mode=mode,sub_id=sub_id,i_id=i_id,img=img,arr=arr,keyw=key,track=track,sub=sub,fname=fname,arr1=arrx,c=count)
			
			
			
@app.route('/user_change_pass')
def user_change_pass():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			fname = session['name']
			img = session['img']
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_change_password.html",name="Change Password",fname=fname,img=img,arr=arrx,c=count)

@app.route('/user_change_pass_1',methods=['POST'])
def user_change_pass_1():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			old=request.form['old']
			new=request.form['new1']
			print(old)
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select password from user_information where user_id=%s",id)
			for raw in cursor.fetchall():
				pas=raw[0]
			if pas == old:
				cursor.execute("update user_information set password=%s where user_id=%s",(new,id))
				db.commit()
				return "Password Successfully updated"
			else:
					return "wrong"		

@app.route('/browse')	
def browse():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			fname = session['name']
			img = session['img']
			arr=[{'id':'1','name':'f'}]
			arr.clear()
			arr1=[{'id':'1','name':'f','volume':'x'}]
			arr1.clear()
			arr2=[{'id':'1','name':'f'}]
			arr2.clear()
			arr3=[{'id':'1','name':'f','track':'x'}]
			arr3.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from volume")
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'name':raw[1]})
				cursor.execute("select * from issue where volume_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					arr1.append({'id':raw1[0],'name':raw1[1],'volume':raw[0]})
				
			cursor.execute("select * from track")
			for raw in cursor.fetchall():
				arr2.append({'id':raw[0],'name':raw[1]})
				cursor.execute("select * from subject where track_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					arr3.append({'id':raw1[0],'name':raw1[1],'track':raw[0]})
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_browse.html",name="Browse",img=img,arr4=arr,arr1=arr1,arr2=arr2,arr3=arr3,fname=fname,arr=arrx,c=count)	

@app.route('/user_issue_paper_list')
def user_issue_paper_list():	

		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			us_id=id
			fname=session['name']
			img = session['img']
			i_id= request.args.get('i_id', default='', type=str)
			arr1=[{'id':1}]
			arr1.clear()
			arr=[{'present':0,'id':'12','p_id':'1','f_name':'harsh','l_name':'shah','topic':'s','last':'asd','path':'x'}]
			arr.clear()
			brief=[{'id':'1'}]
			brief.clear()
			temp=0
			db = mysql.connect()
			cursor = db.cursor()
			# cursor.execute("select paper_id from user_briefcase where user_id=%s",id)
			# for rawx in cursor.fetchall():
				#brief.append({'id':rawx[0]})
			cursor.execute("select paper_id from paper_creation where issue_id=%s ",i_id)
			for raw in cursor.fetchall():
				temp=0
				# for x in brief:
				# 	if x['id']==raw[0]:
				# 		temp=temp+1
				if temp==0:
					cursor.execute("Select user_id from paper_creation where paper_id=%s",raw[0])
					u_id=cursor.fetchone()
					cursor.execute("Select first_name,last_name from user_information where user_id=%s",u_id)
					for raw3 in cursor.fetchall():
						name1=raw3[0]
						name2=raw3[1]
			
					cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
					id=cursor.fetchone()
					cursor.execute("Select title,last_modified_date,path from submission_of_paper where submission_id=%s",id)
					for raw1 in cursor.fetchall():
						arr.append({'present':0,'id':id,'p_id':raw[0],'f_name':name1,'l_name':name2,'topic':raw1[0],'last':raw1[1],'path':raw1[2]})
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			arr1.clear()
			cursor.execute("select paper_id from user_briefcase where user_id=%s",us_id)
			for raw in cursor.fetchall():
				arr1.append({'id':raw[0]})
			for  i in arr:
				for j in arr1:
					if i['p_id']==j['id']:
						i['present']=1
						break

			return render_template("user_issue_list_paper.html",name="List Of Papers",k=arr,img=img,fname=fname,i_id=i_id,c=count,arr=arrx)

@app.route('/user_subject_paper_list')
def user_subject_paper_list():	

		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			us_id=id
			fname=session['name']
			img = session['img']
			sub_id= request.args.get('sub_id', default='', type=str)
			arr=[{'present':0,'id':'12','p_id':'1','f_name':'harsh','l_name':'shah','topic':'y','last':'asd','path':'x'}]
			arr.clear()
			arr1=[{'id':'1'}]
			arr1.clear()
			brief=[{'id':'1'}]
			brief.clear()
			db = mysql.connect()
			cursor = db.cursor()
			# cursor.execute("select paper_id from user_briefcase where user_id=%s",id)
			# for rawx in cursor.fetchall():
			# 	brief.append({'id':rawx[0]})
			cursor.execute("select distinct paper_id from submission_of_paper where subject_id=%s",sub_id)
			for raw8 in cursor.fetchall():
				cursor.execute("select paper_id from paper_creation where paper_id=%s and (status_id=9)",raw8[0])
				for raw9 in cursor.fetchall():
					arr1.append({'id':raw9[0]})
			
			for raw in arr1:
				temp=0
				# for x in brief:
				# 		if x['id'] == raw['id']:
				# 			temp=temp+1
				if temp == 0:
					cursor.execute("Select user_id from paper_creation where paper_id=%s",raw['id'])
					for raw7 in cursor.fetchall():
						cursor.execute("Select first_name,last_name from user_information where user_id=%s",raw7[0])
						for raw3 in cursor.fetchall():
							name1=raw3[0]
							name2=raw3[1]
			
					cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw['id'])
					id=cursor.fetchone()
					cursor.execute("Select title,last_modified_date,path from submission_of_paper where submission_id=%s",id)
					for raw1 in cursor.fetchall():
						arr.append({'present':0,'id':id,'p_id':raw['id'],'f_name':name1,'l_name':name2,'topic':raw1[0],'last':raw1[1],'path':raw1[2]})
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			arr1.clear()
			cursor.execute("select paper_id from user_briefcase where user_id=%s",us_id)
			for raw in cursor.fetchall():
				arr1.append({'id':raw[0]})
	
			for  i in arr:
				for j in arr1:
					if i['p_id']==j['id']:
						i['present']=1
						break
				
			return render_template("user_subject_list_paper.html",name="List Of Papers",k=arr,img=img,fname=fname,sub_id=sub_id,arr=arrx,c=count)			

# @app.route('/add_into_briefcase')		
# def add_into_briefcase():	
		
# 		if 'id' not in session:
# 			return render_template("signin.html")
# 		else:
# 			id = session['id']
# 			p_id= request.args.get('p_id', default='', type=str)
# 			i_id= request.args.get('i_id', default='', type=str)
# 			db = mysql.connect()
# 			cursor = db.cursor()
# 			cursor.execute("""insert into user_briefcase (user_id,paper_id) values(%s,%s)""", (id,p_id))
# 			db.commit()
# 			return redirect(url_for('.user_issue_paper_list',i_id=i_id))
			
@app.route('/add_into_briefcase_1',methods=['POST','GET'])		
def add_into_briefcase_1():	
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			p_id=request.form['id']
			# p_id= request.args.get('p_id', default='', type=str)
			# sub_id= request.args.get('sub_id', default='', type=str)
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""insert into user_briefcase (user_id,paper_id) values(%s,%s)""", (id,p_id))
			db.commit()
			#return redirect(url_for('.user_subject_paper_list',sub_id=sub_id))	
			return "success"		

@app.route('/briefcase')		
def briefcase():	
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img = session['img']
			arr=[{'id':'12','f_name':'harsh','l_name':'shah','topic':'y','last':'asd'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from user_briefcase where user_id=%s",s_id)
			for raw in cursor.fetchall():
				cursor.execute("Select user_id from paper_creation where paper_id=%s",raw[0])
				for raw3 in cursor.fetchall():
					cursor.execute("Select first_name,last_name from user_information where user_id=%s",raw3[0])
					for raw3 in cursor.fetchall():
						name1=raw3[0]
						name2=raw3[1]
			
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					arr.append({'id':raw[0],'f_name':name1,'l_name':name2,'topic':raw1[0],'last':raw1[1]})
			
			
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_briefcase.html",name="Bookmark",k=arr,img=img,fname=fname,arr=arrx,c=count)	

@app.route('/delete_briefcase_1',methods=['POST','GET'])		
def delete_briefcase_1():
	if 'id' not in session:
		return render_template("signin.html")
	else:
		u_id=session['id']
		p_id=request.form['id']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("delete from user_briefcase where user_id=%s and paper_id=%s",(u_id,p_id))
		db.commit()
		return "success"

@app.route("/user_search",methods=['POST','GET'])
def user_search():	
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img=session['img']
			search=request.args.get('search', default='', type=str)
			if search=='':
				search = request.form['search']
			arr=[{'id':'1','title':'as','date':'x','i_id':'x','v_id':'y'}]
			arr.clear()
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
			
			if not arr:
				x='true'
			else:
				x='false'	
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_search.html",name="Search",search=search,k=arr,img=img,fname=fname,x=x,arr=arrx,c=count)

@app.route('/user_summary_paper')
def user_summary_paper():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:	
			id = session['id']
			fname=session['name']
			img=session['img']
			p_id= request.args.get('p_id', default='', type=str)
			max=0
			con=''
			submission=[{'count':'1','id':'1','title':'abc','conclusion':'sasad'}]
			submission.clear()
			comment=[{'id':'1','comment':'dsd'}]
			comment.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select status_id from paper_creation where paper_id=%s",p_id)
			sst=cursor.fetchone()
			cursor.execute("select count(submission_id) from submission_of_paper where paper_id=%s",p_id)
			for raw in cursor.fetchall():
				max=raw[0]
			cursor.execute("select submission_id from submission_of_paper where paper_id=%s order by submission_id DESC",p_id)
			for raw in cursor.fetchall():
				cursor.execute("select title from submission_of_paper where submission_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					cursor.execute("select comment_message from admin_comment where paper_id=%s and submission_id=%s",(p_id,raw[0]))
					for rawz in cursor.fetchall():
						con=rawz[0]
					if con=='':
						con='abc'
					submission.append({'count':max,'id':raw[0],'title':raw1[0],'conclusion':con,'status':sst})
					max=max-1
			for raw in submission:
				cursor.execute("select comment_id,comment_message from expert_comment where submission_id=%s",raw['id'])
				for raw1 in cursor.fetchall():
					cursor.execute("select comment_id from paper_comment where submission_id=%s",raw['id'])
					for raw2 in cursor.fetchall():
						if raw1[0] == raw2[0]:
							comment.append({'id':raw['id'],'comment':raw1[1]})
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("user_summary_paper.html",name="Summary of paper",s=submission,d=comment,img=img,fname=fname,p_id=p_id,c=count,arr=arrx,sst=sst)
@app.route('/user_get_details_by_submission_id')
def user_get_details_by_submission_id():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:	
			id = session['id']
			fname=session['name']
			img=session['img']		
			s_id= request.args.get('s_id', default='', type=str)
			p_id= request.args.get('p_id', default='', type=str)
			key=[{'name':'hgh'}]
			key.clear();
			arr=['a']
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from submission_of_paper where submission_id=%s",s_id)
			for raw in cursor.fetchall():
				arr=raw
			cursor.execute("Select keyword_name from paper_keyword where paper_id=%s and submission_id=%s",(p_id,s_id))
			for i in cursor.fetchall():
				key.append({'name':i[0]})
			cursor.execute("select track_name from track,submission_of_paper where submission_of_paper.track_id=track.track_id and submission_id=%s",s_id)
			for r in cursor.fetchall():
				track=r[0]
			cursor.execute("select subject_name from subject,submission_of_paper where submission_of_paper.subject_id=subject.subject_id and submission_id=%s",s_id)
			for s in cursor.fetchall():
				sub=s[0]
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			return render_template("paper_view_click.html",name="Paper Details",img=img,arr=arr,keyw=key,track=track,sub=sub,fname=fname,p_id=p_id,s_id=s_id,c=count,arr1=arrx)		

@app.route('/user_notification_delete',methods=['POST','GET'])
def user_notification_delete():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:	
			s_id = session['id']
			noty=0
			db = mysql.connect()
			cursor = db.cursor()
			index=request.args.get('index', default='', type=str)
			i=int(index)
			cursor.execute("delete from user_notification where user_id=%s and n_id=%s",s_id,i)
			db.commit()
			if i==6:
				return redirect(url_for('.your_paper'))
			else:
				return redirect(url_for('.list_paper_comment'))	
				
#start
@app.route('/track_subject_keyword',methods=['POST'])		
def track_subject_keyword():

			
			track_id = request.form['track']
			arr=[{'id':'12','name':'harsh','mode':'0'}]
			arr.clear()
			arr1=[{'id':'12','name':'harsh','mode':'0'}]
			arr1.clear()
			
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from subject where track_id=%s """,track_id)
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'name':raw[1]})
			# cursor.execute("""select * from keyword where track_id=%s """,track_id)
			# for raw in cursor.fetchall():
			# 	arr1.append({'id':raw[0],'name':raw[1]})	
			db.commit()
			return render_template("track_subject_keyword.html",arr=arr,arr1=arr1)
			# return jsonify(arr)
			# return json.dumps({'status':'OK','track_id':track_id,'arr':arr});	
			
			
@app.route('/edit_track_subject_keyword',methods=['POST'])	
def edit_track_subject_keyword():

			
			track_id = request.form['track']
			
			arrxy=[{'id':'12','name':'harsh','mode':'0'}]
			arrxy.clear()
			arr2=[{'id':'12','name':'harsh','mode':'0'}]
			arr2.clear()
			
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from subject where track_id=%s """,track_id)
			for raw in cursor.fetchall():
				arrxy.append({'id':raw[0],'name':raw[1]})
			# cursor.execute("""select * from keyword where track_id=%s """,track_id)
			# for raw in cursor.fetchall():
			# 	arr2.append({'id':raw[0],'name':raw[1]})	
			db.commit()
			
			return render_template("edit_track_subject_keyword.html",arrxy=arrxy,arr2=arr2)
			
@app.route('/user_crc')
def user_crc():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			fname = session['name']
			img = session['img']
			arr=[{'pap_id':'1','creation_date':'sas','last':'sas','status':'as','topic':'sas'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			arrx=[{'time':0,'type':0,'message':'sds'}]
			arrx.clear()
			arrx=notify_user(arrx)
			count=noticount_user()
			cursor.execute("select paper_id,creation_date from paper_creation where user_id=%s and (status_id=%s or status_id=%s)",(id,2,4))
			for raw in cursor.fetchall():
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("select status_name from paper_creation,status where status.status_id=paper_creation.status_id and paper_id=%s",raw[0])
				for raww in cursor.fetchall():
					name=raww[0]
				cursor.execute("select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw2 in cursor.fetchall():
					arr.append({'pap_id':raw[0],'creation_date':raw[1],'last':raw2[1],'topic':raw2[0],'status':name})
				
			return render_template("user_crc.html",name="Submit CRC",fname=fname,img=img,arr=arrx,c=count,arry=arr)
			
@app.route('/submit_crc',methods=['POST'])
def submit_crc():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			p_id=request.form['pap']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("update paper_creation set status_id=%s where paper_id=%s",(8,p_id))
			cursor.execute("insert into admin_notification (n_id) values(%s)",5)
			db.commit();
			return "success"
			
@app.route('/temp_crc',methods=['POST'])
def temp_crc():
	return redirect(url_for('.user_crc'))
	
@app.route('/user_add_author')
def user_add_author():
	if 'id' not in session:
			return render_template("signin.html")
	else:
		id = session['id']
		fname = session['name']
		img = session['img']
		arrx=[{'time':0,'type':0,'message':'sds'}]
		arrx.clear()
		arrx=notify_user(arrx)
		count=noticount_user()
		return render_template("user_add_author.html",fname=fname,img=img,arr=arrx,c=count)
		
@app.route('/user_add_author_1',methods=['POST'])
def user_add_author_1():
	if 'id' not in session:
			return render_template("signin.html")
	else:
		id = session['id']
		country=request.form['country']
		name = request.form['name']
		email = request.form['email']
		city = request.form['city']
		area_of_interest = request.form['area_of_interest'] 
		institute = request.form['institute'] 
		university = request.form['university'] 
		designation = request.form['designation']
		department = request.form['department']
		
		db = mysql.connect()
		cursor = db.cursor()		
		cursor.execute("insert into author (name,email,designation,city,country,department,institute,user_id,university,area_of_interset) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,email,designation,city,country,department,institute,id,university,area_of_interest))
		db.commit()
		return redirect(url_for('.user_add_author'))
		
@app.route('/user_list_author')
def user_list_author():
	if 'id' not in session:
			return render_template("signin.html")
	else:
		id = session['id']
		fname = session['name']
		img = session['img']
		arrx=[{'time':0,'type':0,'message':'sds'}]
		arrx.clear()
		arr=[{'id':'x','name':'x','department':'x','institute':'x'}]
		arr.clear()
		
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("""select * from author where user_id=%s """,id)
		for raw in cursor.fetchall():
			arr.append({'id':raw[0],'name':raw[1],'department':raw[6],'institute':raw[7]})
		
		
		arrx=notify_user(arrx)
		count=noticount_user()
		return render_template("user_list_author.html",fname=fname,img=img,arr=arrx,c=count,k=arr)

		
@app.route("/user_delete_author")
def user_delete_author():
	if 'id' not in session:
			return render_template("signin.html")
	else:		
		a_id= request.args.get('id', default='', type=str)
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("update author set user_id=NULL where author_id=%s",(a_id))
		db.commit()
		return redirect(url_for('.user_list_author'))		
		
		
		
@app.route('/user_update_author')	
def user_update_author():
	if 'id' not in session:
		return render_template("signin.html")
	else:
		id = session['id']
		fname = session['name']
		img = session['img']
		
		a_id= request.args.get('a_id', default='', type=str)
		
		arrx=[{'time':0,'type':0,'message':'sds'}]
		arrx.clear()
	
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("""select * from author where author_id=%s """,a_id)
		arr=['a','a','a','a','a','a','a','a','a','a','a']
		for raw in cursor.fetchall():
			arr=raw
		
		arrx=notify_user(arrx)
		count=noticount_user()
		return render_template("user_update_author.html",fname=fname,img=img,arr=arrx,c=count,k=arr)
	
@app.route('/user_update_author_1', methods=['POST']) 
def user_update_author_1():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			fname = session['name']
			img = session['img']
			
			a_id=request.form['a_id']
			name=request.form['name']
			email = request.form['email']
			designation = request.form['designation']
			department = request.form['department']
			area_of_interest = request.form['area_of_interest'] 
			institute = request.form['institute'] 
			city = request.form['city']
			country = request.form['country']
			university = request.form['university'] 
			db = mysql.connect()
			cursor = db.cursor()
		
			cursor.execute('''update author set name=%s,email=%s,designation=%s,city=%s,country=%s,department=%s,institute=%s,university=%s,area_of_interset=%s where author_id=%s''', (name,email,designation,city,country,department,institute,university,area_of_interest,a_id,))
			db.commit()
			return redirect(url_for('.user_list_author'))


		
		
		
		
						