from home import app
from flask import render_template,request,redirect,url_for,session,flash,jsonify
#from mysql import MySQL
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask_mail import Mail,Message


mysql = MySQL()
mysql.init_app(app)
db = mysql.connect()
mail = Mail(app)

#APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/admin')
def admin():
		return render_template("signin_admin.html")
		
@app.route('/signout_admin')
def signout_admin():
		session.pop('id', None)
		session.pop('role', None)
		session.pop('name', None)
		session.pop('img', None)
		return redirect(url_for('.index'))
		
@app.route('/signin_admin')
def signin_admin():
		arr=['a']
		Email = request.args['Email']
		Pass = request.args['Pass']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("SELECT * FROM admin_information where email_id=%s and password=%s;", (Email,Pass))
		for raw in cursor.fetchall():
				arr=raw
		if arr[0] =='a':
			return "Unauthorized User"
		else:
			session['id'] = arr[0]
			session['name'] = arr[1] + " " + arr[3]
			session['img'] = arr[9]
			session['role'] = 'admin'
			return redirect(url_for('.admin_new'))
			
			
@app.route('/admin_home')  
def admin_home():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			fname=session['name']
			img=session['img']
			
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_home.html",fname=fname,img=img,arr=arrx,c=count)	

def notify(arr):
		c=0
		d=0
		e=0
		f=0
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("Select n_id from admin_notification")
		for raw in cursor.fetchall():
			if raw[0]==2:
				c=c+1
			if raw[0]==3:
				d=d+1
			if raw[0]==4:
				e=e+1
			if raw[0]==5:
				f=f+1
		if c>0:
			arr.append({'time':c,'type':2,'message':'User has resubmitted Paper.'})
		if d>0:
			arr.append({'time':d,'type':3,'message':'Reviewer has commented on a Paper.'})
		if e>0:
			arr.append({'time':e,'type':4,'message':'User has uploaded new paper.'})
		if f>0:
			arr.append({'time':f,'type':5,'message':'User has Submitted CRC Copy.'})
			# if raw[0]!=None:
				# p_id=int(raw[0])
				# cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
				# id=cursor.fetchone()
				# cursor.execute("select title from submission_of_paper where submission_id=%s",id)
				# title=cursor.fetchone()
				# tt=str(title)
				# msg=str(raw[1])
				# msg=msg+' '+tt+'  paper.'
				# arr.append({'index':raw[2],'paper_id':raw[0],'message':msg})
			# else:
				# arr.append({'index':raw[2],'paper_id':raw[0],'message':raw[1]})
		return arr
def noticount():
		count=0
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("Select n_id from admin_notification")
		for raw in cursor.fetchall():
			count=count+1
		return count
		
			
@app.route('/Admin_Personal_Info')
def admin_pi():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img = session['img']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select * from admin_information where admin_id=%s",id)
			arr=['a','a','a','a','a','a','a','a','a','a']
			for raw in cursor.fetchall():
				arr=raw
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("pi_admin.html",name="Admin",k=arr,c=count,arr=arrx,fname=fname,img=img)
		
@app.route('/pi_admin1', methods=['POST'])
def pi_admin1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			img = session['img']
			destination='temp'
			for f in request.files.getlist("file"):
				if f.filename == '':
					break
				else:
					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
					filename=f.filenam
					destination = "/".join([target,filename])
					f.save(destination)
					img=f.filename
					session['img']=img
				
		
			first = request.form['fname']
			middle = request.form['mname']
			last = request.form['lname']
			session['name'] = first + " " + last
			gender = request.form['gn']
			email = request.form['email']
			mobile = request.form['mobile']
			skill = request.form['skill']
			dob = request.form['date'] 
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute('''update admin_information set first_name=%s,middle_name=%s,last_name=%s,mobile_no=%s,email_id=%s,gender=%s,skills=%s,date_of_birth=%s,profile_pic=%s where admin_id=%s''', (first,middle,last,mobile,email,gender,skill,dob,img,id))
			db.commit()
			return redirect(url_for('.admin_pi'))
		
@app.route('/status')
def status():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			arr2=[{'id':'1','name':'jkj'}]
			arr2.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from status""")
			for raw in cursor.fetchall():
				arr2.append({'id':raw[0],'name':raw[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("Edit_Status.html",name="Status",arr2=arr2,c=count,arr=arrx,fname=fname,img=img)
		
@app.route('/status_1', methods=['POST'])
def status_1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			name = request.form['Sname']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""insert into status (status_name) values(%s)""", name)
			db.commit()
			return redirect(url_for('.status'))
		
@app.route('/status_2', methods=['POST'])
def status_2():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			key = request.form.getlist('key')
			keys=','.join(key)
			keyx=keys.split(",")
			db = mysql.connect()
			cursor = db.cursor()
			for i in keyx:
				if i!='':
					cursor.execute("""delete from status where status_id=%s""", i)
			db.commit()
			return "Successfully deleted"
		
@app.route('/keyword')
def keyword():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			arr2=[{'id':'1','name':'jkj'}]
			arr2.clear()
			arr3=[{'id':'1','name':'jkj'}]
			arr3.clear()
			arr4=[{'id':'1','name':'jkj'}]
			arr4.clear()
			page_count=''
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from subject")
			for raw in cursor.fetchall():
				arr3.append({'id':raw[0],'name':raw[1]})
			cursor.execute("select * from track")
			for raw in cursor.fetchall():
				arr4.append({'id':raw[0],'name':raw[1]})
			cursor.execute("""select * from keyword""")
			for raw in cursor.fetchall():
				arr2.append({'id':raw[0],'name':raw[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			#page_count=0
			
			return render_template("Edit_Keyword.html",name="Keyword",page_count=page_count,img=img,c=count,arr=arrx,arr2=arr2,arr3=arr3,arr4=arr4,fname=fname)
	
@app.route('/keyword_1', methods=['POST'])
def keyword_1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			t_id = request.form['track']
			name = request.form['keyword']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""insert into keyword (keyword_name,track_id) values(%s,%s)""", (name,t_id))
			db.commit()
			return "success"
		#return render_template("successful_message.html",page_count=page_count)
	
	
@app.route('/keyword_2', methods=['POST'])
def keyword_2():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			db = mysql.connect()
			cursor = db.cursor()
			key = request.form.getlist('key')
			keys=','.join(key)
			keyx=keys.split(",")
			for i in keyx:
				if i!='':
					cursor.execute("""delete from keyword where keyword_id=%s""", i)
			db.commit()
			return redirect(url_for('.keyword'))
		
@app.route('/track')
def track():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			arr2=[{'id':'1','name':'jkj'}]
			arr2.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from track""")
			for raw in cursor.fetchall():
				arr2.append({'id':raw[0],'name':raw[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("Edit_Track.html",name="Track",c=count,arr=arrx,img=img,arr2=arr2,fname=fname)
		
@app.route('/track_1', methods=['POST'])
def track_1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			name = request.form['Tname']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""insert into track (track_name) values(%s)""", name)
			db.commit()
			return "success"
		
@app.route('/track_2', methods=['POST'])
def track_2():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			db = mysql.connect()
			cursor = db.cursor()
			key = request.form.getlist('key')
			keys=','.join(key)
			keyx=keys.split(",")
			cursor = db.cursor()
			for i in keyx:
				if i!='':
					cursor.execute("""delete from track where track_id=%s""", i)
			db.commit()
			return "success"

@app.route('/subject')
def subject():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			
			arr2=[{'id':'1','name':'jkj'}]
			arr2.clear()
			arr4=[{'id':'1','name':'jkj'}]
			arr4.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from track")
			for raw in cursor.fetchall():
				arr4.append({'id':raw[0],'name':raw[1]})
			cursor.execute("""select * from subject """,)
			for raw in cursor.fetchall():
				arr2.append({'id':raw[0],'name':raw[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("edit_Subject.html",name="Subject",img=img,c=count,arr=arrx,arr2=arr2,arr4=arr4,fname=fname)		
		
@app.route('/subject_1', methods=['POST'])
def subject_1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			t_id = request.form['track']
			name = request.form['Sname']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""insert into subject (subject_name,track_id) values(%s,%s)""", (name,t_id))
			db.commit()
			return redirect(url_for('.subject'))
	
@app.route('/subject_2', methods=['POST'])
def subject_2():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			key = request.form.getlist('key')
			keys=','.join(key)
			keyx=keys.split(",")
			db = mysql.connect()
			cursor = db.cursor()
			for i in keyx:
				if i!='':
					cursor.execute("""delete from subject where subject_id=%s""", i)
			db.commit()
			return "Deleted Successfully"
		
@app.route('/admin_announcements')
def admin_announcements():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			db = mysql.connect()
			cursor = db.cursor()
			arry=[{'id':'1','details':'asa','relate':'as','date':'21'}]
			arr1=[{'id':'1','email':'asa','fname':'sasas','lname':'sasas'}]
			arr2=[{'id':'1','email':'asa','fname':'sasas','lname':'sasas'}]
			arr1.clear()
			arr2.clear()
			arry.clear()
			cursor.execute("select user_id,email_id,first_name,last_name from user_information")
			for raw in cursor.fetchall():
				arr1.append({'id':raw[0],'email':raw[1],'fname':raw[2],'lname':raw[3]})
			cursor.execute("select expert_id,email_id,first_name,last_name from expert_information")
			for raw in cursor.fetchall():
				arr2.append({'id':raw[0],'email':raw[1],'fname':raw[2],'lname':raw[3]})
			cursor.execute("select announcement_id,announcement_details,related_to,announcements_date from announcement")
			for raw in cursor.fetchall():
				arry.append({'id':raw[0],'details':raw[1],'relate':raw[2],'date':raw[3]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_announcement.html",name="Announcement",img=img,c=count,k=arr1,l=arr2,arr=arrx,fname=fname,arry=arry)
		
@app.route('/admin_announcements_1', methods=['POST'])
def admin_announcements_1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			name = request.form['Aname']
			relate=request.form['relate']
			dd=datetime.utcnow()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""insert into announcement (admin_id,announcement_details,related_to,announcements_date) values(%s,%s,%s,%s)""", (id,name,relate,dd))
			db.commit()
			return redirect(url_for('.admin_announcements'))

@app.route("/delete_announcement")
def delete_announcement():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:		
		a_id= request.args.get('id', default='', type=str)
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("delete from announcement where announcement_id=%s",a_id)
		db.commit()
		return redirect(url_for('.admin_announcements'))
			
@app.route('/site_wide_announcements')
def site_wide_announcements():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			arr1=[{'a_id':'1','date':'1','dec':'asa'}]
			arr1.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select an_id,date_announcement,description from site_wide_announcement")
			for raw in cursor.fetchall():
				arr1.append({'a_id':raw[0],'date':raw[1],'dec':raw[2]})
			
			
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("site_wide_announcements.html",name="Site Wide Announcement",arr1=arr1,img=img,c=count,arr=arrx,fname=fname)
		
			
@app.route('/admin_announcements_2', methods=['POST'])
def admin_announcements_2():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			name = request.form['Aname_site']
			dd=datetime.utcnow()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""insert into site_wide_announcement (date_announcement,description) values(%s,%s)""", (dd,name))
			db.commit()
			return redirect(url_for('.site_wide_announcements'))

@app.route("/delete_site_announcement")
def delete_site_announcement():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:		
		a_id= request.args.get('id', default='', type=str)
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("delete from site_wide_announcement where an_id=%s",a_id)
		db.commit()
		return redirect(url_for('.site_wide_announcements'))
			
@app.route('/add_expert')
def add_expert():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("expert_signup.html",name="Add Reviewer",img=img,c=count,arr=arrx,fname=fname)
		
@app.route('/add_expert_1', methods=['POST'])
def add_expert_1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
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
			return redirect(url_for('.add_expert'))
		
@app.route('/list_experts')
def list_experts():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select expert_id,first_name from expert_information")
			arr=[{'id':'12','first_name':'shyam','Reviewed':'5','Remaining':'5','Total':'10'}]
			arr.clear()
			for raw in cursor.fetchall():
				cursor.execute("Select count(paper_id) from paper_of_expert where expert_id=%s and (status_id=7 or status_id=6)",raw[0])
				for raw1 in cursor.fetchall():
					id=raw1[0]
				cursor.execute("Select count(paper_id) from paper_of_expert where expert_id=%s and (status_id=2 or status_id=3 or status_id=4 or status_id=5)",raw[0])
				for raw2 in cursor.fetchall():
					id1=raw2[0]
				id2=id1+id
				arr.append({'id':raw[0],'first_name':raw[1],'Remaining':id,'Reviewed':id1,'Total':id2})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			
		return render_template("admin_list_experts.html",name="List Of Reviewers",k=arr,arr=arrx,c=count,img=img,fname=fname)

@app.route('/expert_details')
def expert_details():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			mode= request.args.get('mode', default='', type=str)
			e_id= request.args.get('e_id', default='', type=str)
			arr=[{'paper_id':'12','title':'asdsa','creation_date':'12','last_modified_date':'12','status':'dsds'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id,status_name from paper_of_expert,status where paper_of_expert.status_id=status.status_id and expert_id=%s ",e_id)
			for raw in cursor.fetchall():
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					cursor.execute("select title,last_modified_date from submission_of_paper where submission_id=%s",raw1[0])
					for raw2 in cursor.fetchall():
						title=raw2[0]
						last=raw2[1]
				cursor.execute("select creation_date from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
				for raw3 in cursor.fetchall():
					arr.append({'paper_id':raw[0],'title':title,'creation_date':raw3[0],'last_modified_date':last,'status':raw[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_expert_details.html",name="Papers of Reviewer",mode=mode,eid=e_id,arr=arrx,c=count,img=img,k=arr,fname=fname)
			
# @app.route('/list_papers')
# def list_papers():
		# id = session['id']
		# if id=='':
			# return render_template("signin.html")
		# else:
			# fname=session['name']
			# cursor.execute("Select paper_id from paper_creation")
			# arr=[{'id':'12','f_name':'harsh','l_name':'shah','topic':'shyam','creation_date':'asd','last':'asd','status':'asasd'}]
			# arr.clear()
			# for raw in cursor.fetchall():
				# cursor.execute("Select status_name,creation_date from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
				# for raw2 in cursor.fetchall():
					# id1=raw2[0]
					# id2=raw2[1]
				
				# cursor.execute("Select user_id from paper_creation where paper_id=%s",raw[0])
				# u_id=cursor.fetchone()
				# cursor.execute("Select first_name,last_name from user_information where user_id=%s",u_id)
				# for raw3 in cursor.fetchall():
					# name1=raw3[0]
					# name2=raw3[1]
			
				# cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				# id=cursor.fetchone()
				# cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				# for raw1 in cursor.fetchall():
					# arr.append({'id':id,'f_name':name1,'l_name':name2,'topic':raw1[0],'creation_date':id2,'last':raw1[1],'status':id1})
			
			# return render_template("admin_list_papers.html",name="List Of Papers",k=arr,fname=fname)
			
@app.route('/admin_paper_details')
def admin_paper_details():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			i_id= request.args.get('i_id', default='', type=str)
			p_id= request.args.get('p_id', default='', type=str)
			search= request.args.get('search', default='', type=str)
			mode= request.args.get('mode', default='', type=str)
			if mode=='expert_':
				e_id= request.args.get('e_id', default='', type=str)
				u_id=0
			elif mode=='author_paper':
				a_id= request.args.get('a_id', default='', type=str)
				u_id=0
				e_id=0
			else:
				u_id= request.args.get('u_id', default='', type=str)
				e_id=0
			idd='0'
			key=[{'name':'hgh'}]
			key.clear();
			arr=['a']
			arr.clear()
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
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_paper_details.html",name="Paper Details",search=search,a_id=a_id,i_id=i_id,mode=mode,img=img,eid=e_id,uid=u_id,arr=arr,keyw=key,track=track,sub=sub,fname=fname,pp_id=p_id,arr1=arrx,c=count)
		

@app.route('/list_users')
def list_users():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select user_id,first_name from user_information")
			arr=[{'user_id':'21','first_name':'shyam','Total':'5'}]
			arr.clear()
			for raw in cursor.fetchall():
				cursor.execute("Select count(paper_id) from paper_creation where user_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					id=raw1[0]
				arr.append({'user_id':raw[0],'first_name':raw[1],'Total':id})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_list_users.html",name="List Of Users",img=img,k=arr,fname=fname,arr=arrx,c=count)
			
@app.route('/admin_user_details')
def admin_user_details():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			u_id= request.args.get('u_id', default='', type=str)
			arr=[{'paper_id':'12','title':'asdsa','creation_date':'12','last_modified_date':'12','status':'dsds'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id from paper_creation where user_id=%s",u_id)
			for raw in cursor.fetchall():
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					cursor.execute("select title,last_modified_date from submission_of_paper where submission_id=%s",raw1[0])
					for raw2 in cursor.fetchall():
						title=raw2[0]
				cursor.execute("select creation_date,status_name from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
				for raw3 in cursor.fetchall():
					arr.append({'paper_id':raw[0],'title':raw2[0],'creation_date':raw3[0],'last_modified_date':raw2[1],'status':raw3[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_expert_details.html",name="Papers of User",k=arr,uid=u_id,img=img,fname=fname,arr=arrx,c=count)
		
		
@app.route('/allocation')
def allocation():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img=session['img']
			arr=[{'id':'1','title':'as'}]
			arr.clear()
			arr1=[{'id':'1','fname':'as','lname':'as'}]
			arr1.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id from paper_creation where status_allocation=%s",'false')
			for raw in cursor.fetchall():
				id=raw[0]
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id)
				for raw2 in cursor.fetchall():
					cursor.execute("select title from submission_of_paper where submission_id=%s",raw2[0])
					for raw1 in cursor.fetchall():
						arr.append({'id':id,'title':raw1[0]})
			cursor.execute("select expert_id,first_name,last_name from expert_information")
			for raw in cursor.fetchall():
				arr1.append({'id':raw[0],'fname':raw[1],'lname':raw[2]})
			if not arr:
				x='true'
			else:
				x='false'
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("allocation.html",name="Allocation Of Paper",img=img,k=arr,l=arr1,x=x,fname=fname,arr=arrx,c=count)
		
@app.route('/allocation_1', methods=['POST'])
def allocation_1():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			exp_ids = request.form['temp_12']
			pap_id = request.form.getlist('papers_title') 
			exp_id=exp_ids.split(",")
		
			db = mysql.connect()
			cursor = db.cursor()
			for i in pap_id:
				for j in exp_id:
					if int(j)!=0:
						cursor.execute("""insert into paper_of_expert (expert_id,paper_id,status_id) values(%s,%s,%s)""",(int(j),i,7))
						cursor.execute("insert into expert_notification (expert_id,n_id) values(%s,%s)",(j,1))
				cursor.execute('''update paper_creation set status_allocation="true" where paper_id=%s''', i)
				cursor.execute('''update paper_creation set status_id=7 where paper_id=%s''',i)
				
			db.commit()
			return redirect(url_for('.allocation'))
		

			
@app.route('/add_admin')
def add_admin():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname = session['name']
			img=session['img']
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_signup.html",name="Add Admin",fname=fname,img=img,c=count,arr=arrx)
			
@app.route('/add_admin_1',methods=['POST'])
def add_admin_1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			db = mysql.connect()
			cursor = db.cursor()
			destination='temp'
			for f in request.files.getlist("file"):
				if f.filename=='':
					destination='Default.jpg'
				else:
					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
					filename=f.filename
					ext=filename.split(".")
					destination = "/".join([target,filename])
					f.save(destination)
					destination=filename
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
			cursor.execute("""insert into admin_information (first_name,middle_name,last_name,mobile_no,email_id,password,gender,skills,profile_pic,date_of_birth,date_registration) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (first,middle,last,mobile,email,password,gender,skill,destination,dob,dd))
			db.commit()
			return redirect(url_for('.add_admin'))
				
@app.route('/validate_email_admin',methods=['POST'])
def validate_email_admin():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			email = request.form['email']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from admin_information where email_id=%s",email)
			x=0
			for raw in cursor.fetchall():
				x=x+1
			if x>0:
				return "wrong"
			else:
				return "success"
@app.route('/validate_email_expert',methods=['POST'])
def validate_email_expert():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			email = request.form['email']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from expert_information where email_id=%s",email)
			x=0
			for raw in cursor.fetchall():
				x=x+1
			if x>0:
				return "wrong"
			else:
				return "success"
@app.route('/validate_email_admin_1',methods=['POST'])
def validate_email_admin_1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			email = request.form['email']
			email1=''
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select email_id from admin_information where admin_id=%s",id)
			for raw in cursor.fetchall():
				email1=raw[0]
			if email1==email:
				return "success"
			else:
				cursor.execute("select * from admin_information where email_id=%s",email)
				x=0
				for raw in cursor.fetchall():
					x=x+1
				if x>0:
					return "wrong"
				else:
					return "success"
			
@app.route('/admin_comments',methods=['POST'])
def admin_comments():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			fname = session['name']
			img=session['img']
			arr=[{'title':'harsh','date':'s','msg':'s','e_name':'x'}]
			arr.clear()
			p_id= request.args.get('pp_id', default='', type=str)
			db = mysql.connect()
			cursor = db.cursor()
			# cursor.execute("Select paper_id from submission_of_paper where submission_id=%s",s_id)
			# for raw4 in cursor.fetchall():
				# p_id=raw4[0]		
			cursor.execute("Select date_of_comment,comment_message,expert_id from expert_comment where paper_id=%s and (status_id=4 or status_id=5 or status_id=6)",p_id)
			for raw in cursor.fetchall():
				cursor.execute("select first_name from expert_information where expert_id=%s",raw[2])
				for raw3 in cursor.fetchall():
					e_name=raw3[0]
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
				for raw1 in cursor.fetchall():
					cursor.execute("select title from submission_of_paper where submission_id=%s",raw1[0])
					for raw2 in cursor.fetchall():
						arr.append({'title':raw2[0],'date':raw[0],'msg':raw[1],'e_name':e_name})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_comments.html",name="List Of Comments",k=arr,img=img,fname=fname,c=count,arr=arrx)
			
@app.route('/admin_change_pass')
def admin_change_pass():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname = session['name']
			img = session['img']
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_change_password.html",name="Change Password",fname=fname,img=img,c=count,arr=arrx)

@app.route('/admin_change_pass_1',methods=['POST'])
def admin_change_pass_1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			old=request.form['old']
			new=request.form['new1']
			#cnew=request.form['cnew']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select password from admin_information where admin_id=%s",id)
			for raw in cursor.fetchall():
				pas=raw[0]
			if pas == old:
				cursor.execute("update admin_information set password=%s where admin_id=%s",(new,id))
				db.commit()
				return "success"
			else:
					return "wrong"	


@app.route('/admin_archived')
def admin_archived():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			fname = session['name']		
			img=session['img']
			arr=[{'id':'1','name':'f'}]
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
					arr1.append({'id':raw1[0],'name':raw1[1],'volume':raw[0]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_archived_paper.html",name="Archived Paper",arr2=arr,arr1=arr1,img=img,fname=fname,c=count,arr=arrx)	



		# s_id = session['id']
		# if s_id=='':
			# return render_template("signin.html")
		# else:
			# fname = session['name']
			# arr=[{'id':'1','name':'as'}]
			# arr.clear()
			# cursor.execute("select * from volume")
			# for raw in cursor.fetchall():
				# arr.append({'id':raw[0],'name':raw[1]})
			
			# return render_template("admin_archived_paper.html",name="Archived Paper",k=arr,fname=fname)
			
@app.route('/admin_pending')
def admin_pending():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			fname = session['name']
			img=session['img']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from paper_creation where (status_id=%s or status_id=%s or status_id=%s or status_id=%s or status_id=%s or status_id=%s) and issue_id is null",(2,3,4,5,6,7))
			arr=[{'id':'12','f_name':'harsh','l_name':'shah','topic':'shyam','creation_date':'asd','last':'asd','status':'asasd'}]
			arr.clear()
			for raw in cursor.fetchall():
				cursor.execute("Select status_name,creation_date from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
				for raw2 in cursor.fetchall():
					id1=raw2[0]
					id2=raw2[1]
				
				cursor.execute("Select user_id from paper_creation where paper_id=%s",raw[0])
				u_id=cursor.fetchone()
				cursor.execute("Select first_name from user_information where user_id=%s",u_id)
				for raw3 in cursor.fetchall():
					name1=raw3[0]
			
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					arr.append({'id':raw[0],'f_name':name1,'topic':raw1[0],'creation_date':id2,'last':raw1[1],'status':id1})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_pending_paper.html",name="Pending Paper",k=arr,img=img,fname=fname,arr=arrx,c=count)
			
@app.route('/admin_new')
def admin_new():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			fname = session['name']
			img=session['img']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from paper_creation where status_id=%s",1)
			arr=[{'id':'12','f_name':'harsh','l_name':'shah','topic':'shyam','creation_date':'asd','last':'asd','status':'asasd'}]
			arr.clear()
			for raw in cursor.fetchall():
				cursor.execute("Select status_name,creation_date from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
				for raw2 in cursor.fetchall():
					id1=raw2[0]
					id2=raw2[1]
				
				cursor.execute("Select user_id from paper_creation where paper_id=%s",raw[0])
				u_id=cursor.fetchone()
				cursor.execute("Select first_name from user_information where user_id=%s",u_id)
				for raw3 in cursor.fetchall():
					name1=raw3[0]
			
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					arr.append({'id':raw[0],'f_name':name1,'topic':raw1[0],'creation_date':id2,'last':raw1[1],'status':id1})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_list_papers.html",name="New Paper",k=arr,img=img,fname=fname,c=count,arr=arrx)




@app.route('/volume')
def volume():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname = session['name']
			img=session['img']			
			arr=[{'id':'1','name':'f'}]
			arr.clear()
			arr1=[{'id':'1','name':'f','volume':'x','i_no':'1'}]
			arr1.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from volume")
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'name':raw[1]})
				cursor.execute("select * from issue where volume_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					arr1.append({'id':raw1[0],'name':raw1[1],'volume':raw[0],'i_no':raw1[3]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_add_volume.html",name="Volume",arr2=arr,arr1=arr1,img=img,fname=fname,arr=arrx,c=count)	
			
@app.route('/volume_1',methods=['POST'])
def volume_1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			temp=0
			name = request.form['Vname']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select volume_name from volume")
			for raw in cursor.fetchall():
				if raw[0]==name:
					temp=temp+1
					break
					
			if temp==0:	
				cursor.execute("""insert into volume (volume_name) values(%s)""", name)
				db.commit()
				return redirect(url_for('.volume'))
			else:
				
				return "Already Created volume"
		
				

@app.route('/issue')
def issue():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			arr=[{'id':'1','name':'f'}]
			arr.clear()
			arr1=[{'id':'1','name':'f','volume':'x','i_no':'1'}]
			arr1.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select * from volume")
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'name':raw[1]})
				cursor.execute("select * from issue where volume_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					arr1.append({'id':raw1[0],'name':raw1[1],'volume':raw[0],'i_no':raw1[3]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			# cursor.execute("select * from volume")
			# for raw in cursor.fetchall():
				# arr.append({'id':raw[0],'name':raw[1]})
				
			# cursor.execute("select * from issue")
			# for raw in cursor.fetchall():
				# arr1.append({'id':raw[0],'name':raw[1]})
				
			return render_template("admin_add_issue.html",name="Issue",arr2=arr,img=img,arr1=arr1,fname=fname,arr=arrx,c=count)	
			
@app.route('/issue_check',methods=['POST'])
def issue_check():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			temp=0
			x=0
			issue_no = request.form['issue']
			v_id = request.form['volume']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select issue_no from issue where volume_id=%s",v_id)
			for raw in cursor.fetchall():
				x=int(issue_no)
				if raw[0] == x:
					temp=temp+1
					
			if temp==0:
				return "success"
			else:
				return "wrong"
					
			
@app.route('/issue_1',methods=['POST'])
def issue_1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			v_id = request.form['volume']
			issue_no = request.form['issue_no']
			name1 = request.form['start_month']
			name2 = request.form['end_month']
			name=name1+' to '+name2
			db = mysql.connect()
			cursor = db.cursor()
			
			cursor.execute("""insert into issue (issue_name,volume_id,issue_no) values(%s,%s,%s)""", (name,v_id,issue_no))
			db.commit()
			return redirect(url_for('.issue'))
				
			
			
			# cursor.execute("""insert into issue (issue_name,volume_id,issue_no) values(%s,%s,%s)""", (name,v_id,issue_no))
			# db.commit()
			# return redirect(url_for('.issue'))
			
			
@app.route('/issue_paper_list')
def issue_paper_list():	
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			i_id= request.args.get('i_id', default='', type=str)
			arr=[{'id':'12','f_name':'harsh','l_name':'shah','topic':'shyam','last':'asd'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id from paper_creation where issue_id=%s",i_id)
			for raw in cursor.fetchall():
				
				
				cursor.execute("Select user_id from paper_creation where paper_id=%s",raw[0])
				u_id=cursor.fetchone()
				cursor.execute("Select first_name,last_name from user_information where user_id=%s",u_id)
				for raw3 in cursor.fetchall():
					name1=raw3[0]
					name2=raw3[1]
			
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					arr.append({'id':id,'f_name':name1,'l_name':name2,'topic':raw1[0],'last':raw1[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_issue_list_paper.html",name="List Of Papers",i_id=i_id,img=img,k=arr,fname=fname,arr=arrx,c=count)
			
			
@app.route('/paper_add_volume')
def paper_add_volume():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img=session['img']
			arr=[{'id':'1','title':'as'}]
			arr.clear()
			arr1=[{'id':'1','year':'as'}]
			arr1.clear()
			arr2=[{'id':'1','month':'as','no':1}]
			arr2.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id from paper_creation where status_id=%s",(8))
			for raw in cursor.fetchall():
				id=raw[0]
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id)
				for raw2 in cursor.fetchall():
					cursor.execute("select title from submission_of_paper where submission_id=%s",raw2[0])
					for raw1 in cursor.fetchall():
						arr.append({'id':raw2[0],'title':raw1[0]})
						
			cursor.execute("select * from volume")
			for raw in cursor.fetchall():
				arr1.append({'id':raw[0],'year':raw[1]})
				
			cursor.execute("select * from issue")
			for raw in cursor.fetchall():
				arr2.append({'id':raw[0],'month':raw[1],'no':raw[3]})
			
			if not arr:
				x='true'
			else:
				x='false'
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_paper_in_volume.html",name="Add Paper In Volume",k=arr,l=arr1,m=arr2,x=x,img=img,fname=fname,arr=arrx,c=count)
		
		
		
@app.route('/paper_add_volume_1',methods=['POST'])
def paper_add_volume_1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			y_name = request.form['year']
			m_name = request.form['month']
			subm_id = request.form['paper']
			paper_path=''
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id from submission_of_paper where submission_id=%s",subm_id)
			for raw in cursor.fetchall():
				p_id=raw[0]
			cursor.execute('''update paper_creation set issue_id=%s,status_id=%s where paper_id=%s''',(m_name,9,p_id))
			cursor.execute("select user_id from paper_creation where paper_id=%s",p_id)
			u_id=cursor.fetchone()
			cursor.execute("insert into user_notification (user_id,n_id) values(%s,%s)",(u_id,6))
		
			for f in request.files.getlist("file"):

					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Paper/')
					filename=f.filename
					ext=filename.split(".")
					destination = "/".join([target,filename])
					f.save(destination)
					paper_path=f.filename
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
			id=cursor.fetchone()
								
			cursor.execute("select * from submission_of_paper where submission_id=%s",id)
			for raw in cursor.fetchall():
				cursor.execute("insert into submission_of_paper (title,abstract,last_modified_date,path,track_id,paper_id,subject_id) values(%s,%s,%s,%s,%s,%s,%s)",(raw[1],raw[2],raw[3],paper_path,raw[5],raw[6],raw[7]))
			
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
			new_id=cursor.fetchone()
			
			cursor.execute("select keyword_name from paper_keyword where paper_id=%s and submission_id=%s",(p_id,id))
			for raw in cursor.fetchall():
				cursor.execute("insert into paper_keyword (keyword_name,submission_id,paper_id) values(%s,%s,%s)",(raw[0],new_id,p_id))
						
			db.commit()
			return redirect(url_for('.paper_add_volume'))		

@app.route("/admin_search",methods=['POST','GET'])
def admin_search():	
		
		if 'id' not in session:
			return render_template("signin_admin.html")
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
					cursor.execute("select distinct paper_id from submission_of_paper where submission_id=%s and title like %s",(id7,"%" + search + "%"))
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
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_search.html",name="Search",search=search,k=arr,img=img,fname=fname,x=x,arr=arrx,c=count)	

@app.route('/admin_summary_paper')
def admin_summary_paper():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			id = session['id']
			fname=session['name']
			img=session['img']
			p_id= request.args.get('p_id', default='', type=str)
			max=0
			submission=[{'count':'1','id':'1','title':'abc'}]
			submission.clear()
			admin_comment=[{'id':'1','comment':'asdsa'}]
			admin_comment.clear()
			comment=[{'id':'1','status':'asa','comment':'dsd','name':'abc'}]
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
					submission.append({'count':max,'id':raw[0],'title':raw1[0]})
					max=max-1
			for raw in submission:
				cursor.execute("select comment_message,status_name,first_name from expert_comment,status,expert_information where status.status_id=expert_comment.status_id and expert_comment.expert_id=expert_information.expert_id and submission_id=%s",raw['id'])
				for raw1 in cursor.fetchall():
					comment.append({'id':raw['id'],'status':raw1[1],'comment':raw1[0],'name':raw1[2]})
				cursor.execute("select comment_message from admin_comment where paper_id=%s and submission_id=%s",(p_id,raw['id']))
				for raw2 in cursor.fetchall():
					admin_comment.append({'id':raw['id'],'comment':raw2[0]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_summary_paper.html",name="Summary of paper",s=submission,d=comment,a=admin_comment,img=img,fname=fname,p_id=p_id,arr=arrx,c=count,sst=sst)
			
@app.route('/admin_submission_details')
def admin_submission_details():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			id = session['id']
			fname=session['name']
			img=session['img']	
			p_id= request.args.get('p_id', default='', type=str)
			s_id= request.args.get('s_id', default='', type=str)
			mode= request.args.get('mode', default='', type=str)
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
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_paper_details.html",name="Paper Details",mode=mode,p_id=p_id,img=img,arr=arr,keyw=key,track=track,sub=sub,fname=fname,s_id=s_id,c=count,arr1=arrx)
			
@app.route('/admin_review_comment')
def admin_review_comment():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			id = session['id']
			fname=session['name']
			img=session['img']	
			paper= request.args.get('pp_id', default='', type=str)
			arr=[{'c_id':'1','comment':'aas','status':'asa','name':'asa'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",paper)
			for raw in cursor.fetchall():
				s_id=raw[0]
			cursor.execute("select comment_id,comment_message,first_name,status_name from expert_comment,expert_information,status where submission_id=%s and status.status_id=expert_comment.status_id and expert_comment.expert_id=expert_information.expert_id",s_id)
			for raw in cursor.fetchall():
				arr.append({'c_id':raw[0],'comment':raw[1],'name':raw[2],'status':raw[3]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_review_comment.html",name="Review Comment",k=arr,img=img,fname=fname,p_id=paper,s_id=s_id,c=count,arr=arrx)
			
@app.route('/admin_review_comment_1',methods=['POST'])
def admin_review_comment_1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			a_id = session['id']
			fname=session['name']
			img=session['img']	
			p_id=request.args.get('p_id', default='', type=str)
			ss_id=request.args.get('s_id', default='', type=str)
			send = request.form.getlist('send')
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
			id=cursor.fetchone()
			if request.form['hdd'] == 'accept':
				cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(2,p_id))
				for s in send:
					cursor.execute("""insert into paper_comment (comment_id,paper_id,submission_id) values(%s,%s,%s)""",(s,p_id,ss_id))
				
			elif request.form['hdd'] == 'reject':
				
				cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(3,p_id))
				for s in send:
					cursor.execute("""insert into paper_comment (comment_id,paper_id,submission_id) values(%s,%s,%s)""",(s,p_id,ss_id))
				
			elif request.form['hdd'] == 'rejectwithcomment':
				comment=request.form['comment']
				if comment == '':
					return "Please give comment"
				cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(5,p_id))
				for s in send:
					cursor.execute("""insert into paper_comment (comment_id,paper_id,submission_id) values(%s,%s,%s)""",(s,p_id,ss_id))
				cursor.execute("insert into admin_comment (comment_message,admin_id,paper_id,submission_id) values(%s,%s,%s,%s)",(comment,a_id,p_id,ss_id))
				
			elif request.form['hdd'] == 'acceptwithcomment':
				comment=request.form['comment']
				if comment == '':
					return "Please give comment"
				cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(4,p_id))
				for s in send:
					cursor.execute("""insert into paper_comment (comment_id,paper_id,submission_id) values(%s,%s,%s)""",(s,p_id,ss_id))
				cursor.execute("insert into admin_comment (comment_message,admin_id,paper_id,submission_id) values(%s,%s,%s,%s)",(comment,a_id,p_id,ss_id))
				
			elif request.form['hdd'] == 'continuewithmodification':
				comment=request.form['comment']
				if comment == '':
					return "Please give comment"
				cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(6,p_id))
				for s in send:
					cursor.execute("""insert into paper_comment (comment_id,paper_id,submission_id) values(%s,%s,%s)""",(s,p_id,ss_id))
				cursor.execute("insert into admin_comment (comment_message,admin_id,paper_id,submission_id) values(%s,%s,%s,%s)",(comment,a_id,p_id,ss_id))
			cursor.execute("select user_id from paper_creation where paper_id=%s",p_id)
			u_id=cursor.fetchone()
			cursor.execute("insert into user_notification (user_id,n_id) values(%s,%s)",(u_id,3))
			db.commit()
			return redirect(url_for('.admin_pending'))
			
@app.route('/admin_notification_delete',methods=['POST','GET'])
def admin_notification_delete():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			noty=0
			index=request.args.get('index', default='', type=str)
			i=int(index)
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("delete from admin_notification where n_id=%s",i)
			db.commit()
			if i==4:
				return redirect(url_for('.admin_new'))	
			if i==2 or i==3:
				return redirect(url_for('.admin_pending'))	
			if i==5:
				return redirect(url_for('.admin_crc'))
				
				
				
#start
@app.route('/volume_issue',methods=['POST'])		
def volume_issue():
			
			
			year = request.form['year']
			mode=''
			arr=[{'id':'12','month':'harsh','mode':'0'}]
			arr.clear()
			
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from issue where volume_id=%s """,year)
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'month':raw[1],'no':raw[3]})
			db.commit()
			return render_template("volume_issue.html",arr=arr,mode=mode)
			
		
			
@app.route('/admin_track_subject_delete',methods=['POST'])		
def admin_track_subject_delete():
			
			track_id = request.form['track']
			mode=''
			arr=[{'id':'12','name':'harsh','mode':'0'}]
			arr.clear()
			
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from subject where track_id=%s """,track_id)
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'name':raw[1]})
			db.commit()
			return render_template("admin_track_subject_delete.html",arr=arr,mode=mode)	

@app.route('/admin_track_keyword',methods=['POST'])		
def admin_track_keyword():

			track_id = request.form['track']
			arr=[{'id':'12','name':'harsh'}]
			arr.clear()
			
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from keyword where track_id=%s """,track_id)
			for raw in cursor.fetchall():
				arr.append({'id':raw[0],'name':raw[1]})
			db.commit()
			return render_template("admin_track_keyword.html",arr=arr)			

@app.route('/send_by_mail',methods=['POST'])		
def send_by_mail():
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			mm=request.form['for_user']
			u_id = request.form['temp_22']
			e_id = request.form['temp_11']
			uu_id=u_id.split(",")
			ee_id=e_id.split(",")
			ux_id=[]
			uu_id=uu_id + ee_id
			for i in uu_id:
				if i!='###' or i!='':
					ux_id.append(i)
			print(ux_id)
			msg = Message('From Flask', sender = 'harshitus99@gmail.com', recipients = ux_id)
			msg.body=mm
			mail.send(msg)
			return redirect(url_for('.admin_announcements'))	
		
@app.route('/admin_expert_personal_info',methods=['POST','GET'])		
def admin_expert_personal_info():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			s_id = session['id']
			fname=session['name']
			img=session['img']	
			e_id=request.form['e_id']
			# e_id=request.args.get('e_id', default='', type=str)
			# mode=request.args.get('mode', default='', type=str)
			arr=['a']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("""select * from expert_information where expert_id=%s """,e_id)
			for raw in cursor.fetchall():
				arr=raw
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return jsonify({'dd':arr})
			# return render_template("admin_expert_personal_info.html",name="Expert Personal Information",mode=mode,k=arr,img=img,fname=fname,s_id=s_id,arr=arrx,c=count)	
@app.route('/search_allocation',methods=['POST','GET'])		
def search_allocation():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			s_id = session['id']
			arr=[{'id':'1','fname':'abc','lname':'sas'}]
			arr.clear()
			fname=session['name']
			img=session['img']	
			text=request.form['ss']
			temp=request.form['arr1']
			if text=='':
				db = mysql.connect()
				cursor = db.cursor()
				cursor.execute("""select expert_id,first_name,last_name from expert_information """)
				for raw in cursor.fetchall():
					arr.append({'id':raw[0],'fname':raw[1],'lname':raw[2]})
			else:
			
				db = mysql.connect()
				cursor = db.cursor()
				cursor.execute("""select expert_id,first_name,last_name from expert_information where first_name like %s or last_name like %s """,("%" + text + "%","%" + text + "%"))
				for raw in cursor.fetchall():
					arr.append({'id':raw[0],'fname':raw[1],'lname':raw[2]})
			return render_template("search_allocation.html",l=arr,tat=temp)
			
			
@app.route('/search_announcement1',methods=['POST','GET'])		
def search_announcement1():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:	
			s_id = session['id']
			arr=[{'id':'1','email':'abc','fname':'abc','lname':'sas'}]
			arr.clear()
			fname=session['name']
			img=session['img']	
			text=request.form['ss']
			temp=request.form['arrx']
			if text=='':
				db = mysql.connect()
				cursor = db.cursor()
				cursor.execute("""select expert_id,email_id,first_name,last_name from expert_information """)
				for raw in cursor.fetchall():
					arr.append({'id':raw[0],'email':raw[1],'fname':raw[2],'lname':raw[3]})
			else:
			
				db = mysql.connect()
				cursor = db.cursor()
				cursor.execute("""select expert_id,email_id,first_name,last_name from expert_information where first_name like %s or last_name like %s """,("%" + text + "%","%" + text + "%"))
				for raw in cursor.fetchall():
					arr.append({'id':raw[0],'email':raw[1],'fname':raw[2],'lname':raw[3]})
			return render_template("search_announcement1.html",l=arr,tat=temp)			

@app.route('/search_announcement2',methods=['POST','GET'])		
def search_announcement2():
	
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			s_id = session['id']
			fname=session['name']
			img=session['img']
			arr=[{'id':'1','email':'abc','fname':'abc','lname':'sas'}]
			arr.clear()	
			text=request.form['ss']
			temp=request.form['arry']
			if text=='':
				db = mysql.connect()
				cursor = db.cursor()
				cursor.execute("""select user_id,email_id,first_name,last_name from user_information """)
				for raw in cursor.fetchall():
					arr.append({'id':raw[0],'email':raw[1],'fname':raw[2],'lname':raw[3]})
			else:
			
				db = mysql.connect()
				cursor = db.cursor()
				cursor.execute("""select user_id,email_id,first_name,last_name from user_information where first_name like %s or last_name like %s """,("%" + text + "%","%" + text + "%"))
				for raw in cursor.fetchall():
					arr.append({'id':raw[0],'email':raw[1],'fname':raw[2],'lname':raw[3]})
			return render_template("search_announcement2.html",k=arr,tat=temp)	

@app.route("/add_editorial")
def add_editorial():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
		s_id = session['id']
		fname=session['name']
		img=session['img']
		arrx=[{'time':1,'type':1,'message':'sds'}]
		arrx.clear()
		arrx=notify(arrx)
		count=noticount()
		return render_template('add_editorial.html',name="Add Editorial",arr=arrx,c=count,fname=fname,img=img)	
		
@app.route("/add_editorial_1",methods=['POST','GET'])
def add_editorial_1():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
		fname=request.form['fname']
		mname=request.form['mname']
		lname=request.form['lname']
		desc=request.form['desc']
		designation=request.form['designation']
		profile=''
		db = mysql.connect()
		cursor = db.cursor()
		for f in request.files.getlist("file"):
				if f.filename=='':
					profile='Default.jpg'
				else:
					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
					filename=f.filename
					ext=filename.split(".")
					profile = "/".join([target,filename])
					f.save(profile)
					profile=filename
		cursor.execute("insert into editorial_board (first_name,middle_name,last_name,description,profile,designation) values(%s,%s,%s,%s,%s,%s)",(fname,mname,lname,desc,profile,designation))
		db.commit()
		return redirect(url_for('.add_editorial'))
	
@app.route("/delete_editorial")
def delete_editorial():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
		s_id = session['id']
		fname=session['name']
		img=session['img']
		arrx=[{'time':1,'type':1,'message':'sds'}]
		arrx.clear()
		arrx=notify(arrx)
		count=noticount()
		db = mysql.connect()
		cursor = db.cursor()
		arry=[{'id':'1','fname':'abc','mname':'ds','lname':'sdada','desc':'sdsd','pic':'asa','designation':'asa'}]
		arry.clear()
		cursor.execute("select guest_id,first_name,middle_name,last_name,description,profile,designation from editorial_board")
		for raw in cursor.fetchall():
			arry.append({'id':raw[0],'fname':raw[1],'mname':raw[2],'lname':raw[3],'desc':raw[4],'pic':raw[5],'designation':raw[6]})
		return render_template('delete_editorial.html',name="List Of Editorials",arr=arrx,c=count,fname=fname,img=img,arry=arry)
		
@app.route("/delete_editorial_1",methods=['POST'])
def delete_editorial_1():
	print("abc")
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:		
		#g_id= request.args.get('id', default='', type=str)
		print("abc")
		g_id=request.form['id']
		print(g_id)
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("delete from editorial_board where guest_id=%s",g_id)
		db.commit()
		return redirect(url_for('.delete_editorial'))

@app.route("/edit_editorial")
def edit_editorial():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:		
		g_id= request.args.get('id', default='', type=str)
		s_id = session['id']
		fname=session['name']
		img=session['img']
		arrx=[{'time':1,'type':1,'message':'sds'}]
		arrx.clear()
		arrx=notify(arrx)
		count=noticount()
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select * from editorial_board where guest_id=%s",g_id)
		arr=['a','a','a','a','a','a','a','a','a','a','a']
		for raw in cursor.fetchall():
			arr=raw

		return render_template("edit_editorial.html",name="Edit Editorial",arr=arrx,c=count,fname=fname,img=img,k=arr)

@app.route("/edit_editorial_1",methods=['POST','GET'])
def edit_editorial_1():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
		g_id=request.form['guest_id']
		fname=request.form['fname']
		mname=request.form['mname']
		lname=request.form['lname']
		desc=request.form['desc']
		designation=request.form['designation']
		profile=''
		db = mysql.connect()
		cursor = db.cursor()
		for f in request.files.getlist("file"):
				if f.filename=='':
					cursor.execute("select profile from editorial_board where guest_id=%s",g_id)
					for raw in cursor.fetchall():
						profile=raw[0]
				else:
					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
					filename=f.filename
					ext=filename.split(".")
					profile = "/".join([target,filename])
					f.save(profile)
					profile=filename
		cursor.execute("update editorial_board set first_name=%s,middle_name=%s,last_name=%s,description=%s,profile=%s,designation=%s where guest_id=%s",(fname,mname,lname,desc,profile,designation,g_id))
		db.commit()
		return redirect(url_for('.delete_editorial'))

@app.route("/admin_query")
def admin_query():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
		s_id = session['id']
		fname=session['name']
		img=session['img']
		arrx=[{'time':1,'type':1,'message':'sds'}]
		arrx.clear()
		arrx=notify(arrx)
		count=noticount()
		db = mysql.connect()
		cursor = db.cursor()
		arry=[{'id':'1','mobile':'abc','email':'ds','message':'sdada','name':'sdsd'}]
		arry.clear()
		cursor.execute("select c_id,mobile,email,message,name from contactus")
		for raw in cursor.fetchall():
			arry.append({'id':raw[0],'mobile':raw[1],'email':raw[2],'message':raw[3],'name':raw[4]})
		return render_template('admin_queries.html',name="User Queries",arr=arrx,c=count,fname=fname,img=img,arry=arry)
		
@app.route("/admin_query_1",methods=['POST','GET'])
def admin_query_1():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
		s_id = session['id']
		db = mysql.connect()
		cursor = db.cursor()
		q_id=request.form.getlist('query')
		for i in q_id:
			cursor.execute("delete from contactus where c_id=%s",i)
		db.commit()
		return redirect(url_for('.admin_query'))
		
@app.route("/admin_crc")
def admin_crc():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
		s_id = session['id']
		fname=session['name']
		img=session['img']
		arrx=[{'time':1,'type':1,'message':'sds'}]
		arrx.clear()
		arrx=notify(arrx)
		count=noticount()
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("Select paper_id from paper_creation where status_id=%s",8)
		arry=[{'id':'12','f_name':'harsh','l_name':'shah','topic':'shyam','creation_date':'asd','last':'asd','status':'asasd','path':'c'}]
		arry.clear()
		for raw in cursor.fetchall():
			cursor.execute("Select status_name,creation_date from paper_creation,status where paper_creation.status_id=status.status_id and paper_id=%s",raw[0])
			for raw2 in cursor.fetchall():
				id1=raw2[0]
				id2=raw2[1]
				
			cursor.execute("Select user_id from paper_creation where paper_id=%s",raw[0])
			u_id=cursor.fetchone()
			cursor.execute("Select first_name from user_information where user_id=%s",u_id)
			for raw3 in cursor.fetchall():
				name1=raw3[0]
			
			cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
			id=cursor.fetchone()
			cursor.execute("Select title,last_modified_date,path from submission_of_paper where submission_id=%s",id)
			for raw1 in cursor.fetchall():
				arry.append({'id':raw[0],'f_name':name1,'topic':raw1[0],'creation_date':id2,'last':raw1[1],'status':id1,'path':raw1[2]})
		return render_template('admin_crc.html',name="CRC Papers",arr=arrx,c=count,fname=fname,img=img,arry=arry)
		
@app.route("/admin_authors")
def admin_authors():
	if 'id' not in session:
			return render_template("signin_admin.html")
	else:
			s_id = session['id']
			fname=session['name']
			img=session['img']
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			arr=[{'id':'1','name':'m','no_paper':'5'}]
			arr.clear()
			
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select author_id,name from author")			
			for raw in cursor.fetchall():
				cursor.execute("Select count(paper_id) from user_author where author_id=%s",raw[0])
				for raw1 in cursor.fetchall():
					no_paper=raw1[0]
					print(no_paper)
				arr.append({'id':raw[0],'name':raw[1],'no_paper':no_paper})
			
		
			return render_template('admin_authors.html',name="List Of Authors",k=arr,arr=arrx,c=count,fname=fname,img=img)
			
@app.route('/admin_author_details')
def admin_author_details():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
		
			a_id= request.args.get('a_id', default='', type=str)
			
			db = mysql.connect()
			cursor = db.cursor()
			arr=['a','a','a','a','a','a','a','a','a']
			cursor.execute("Select * from author where author_id=%s",a_id)	
			for raw in cursor.fetchall():
				arr=raw
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_author_details.html",name="Details Of Author",a_id=a_id,arr=arrx,c=count,img=img,k=arr,fname=fname)

@app.route('/author_paper_details')
def author_paper_details():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
		
			a_id= request.args.get('a_id', default='', type=str)
			arr=[{'topic':'shyam','creation_date':'asd','last':'asd','status':'asasd','pap_id':'1'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from user_author where author_id=%s",a_id)
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
			
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("author_paper_details.html",name="Paper associated with Author",a_id=a_id,n=nn,arr=arrx,c=count,k=arr,img=img,fname=fname)

@app.route('/admin_show_comment_reviewer')
def admin_show_comment_reviewer():
		
		if 'id' not in session:
			return render_template("signin_admin.html")
		else:
			id = session['id']
			fname=session['name']
			img=session['img']
			e_id= request.args.get('e_id', default='', type=str)
			p_id= request.args.get('p_id', default='', type=str)
			db = mysql.connect()
			cursor = db.cursor()
			arr=[{'message':'sssdfd','date':'sfdsds'}]
			arr.clear()
			nos=0
			cursor.execute("Select comment_message,date_of_comment from expert_comment where paper_id=%s and expert_id=%s order by submission_id desc",(p_id,e_id))
			for raw in cursor.fetchall():
				nos=1
				arr.append({'message':raw[0],'date':raw[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify(arrx)
			count=noticount()
			return render_template("admin_reviewer_comment.html",name="Comment of Reviewer",nos=nos,eid=e_id,arr=arrx,c=count,img=img,k=arr,fname=fname)
