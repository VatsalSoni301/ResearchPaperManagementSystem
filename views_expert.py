from home import app
from flask import render_template,redirect,session,url_for,request
#from mysql import MySQL
from flaskext.mysql import MySQL
from datetime import datetime
import os

mysql = MySQL()
mysql.init_app(app)


@app.route('/expert')
def expert():
		return render_template("signin.html")
	
@app.route('/signout_expert')
def signout_expert():
		session.pop('id', None)
		session.pop('role', None)
		session.pop('name', None)
		session.pop('img', None)
		return redirect(url_for('.index'))
		
@app.route('/signin_expert')
def signin_expert():
		arr=['a']
		Email = request.args['Email']
		Pass = request.args['Pass']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("SELECT * FROM expert_information where email_id=%s and password=%s;", (Email,Pass))
		for raw in cursor.fetchall():
			arr=raw
		if arr[0]=='a':
			return "Unauthorized User"
		else:
			session['id']=arr[0]
			session['name']=arr[1] + " " + arr[3]
			session['img']=arr[12]
			session['role'] = 'reviewer'
			return redirect(url_for('.paper_to_be_reviwed'))
			
@app.route('/expert_home')  
def expert_home():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id=session['id']
			fname=session['name']
			img=session['img']
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("expert_home.html",fname=fname,img=img,c=count,arr=arrx)			
		
def notify_expert(arr):
		id=session['id']
		c=0
		d=0
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select n_id from expert_notification where expert_id=%s",id)
		for raw in cursor.fetchall():
			if raw[0]==1:
				c=c+1
			elif raw[0]==2:
				d=d+1
		if c>0:
			arr.append({'time':c,'type':1,'message':'Admin has allocated new papers to you'})
		if d>0:
			arr.append({'time':d,'type':2,'message':'User has resubmitted paper'})
		# cursor.execute("Select n_message from expert_notification,notification where expert_notification.n_id=notification.n_id and expert_id=%s",id)
		# for raw in cursor.fetchall():
			# arr.append({'message':raw[0]})
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
def noticount_expert():
		count=0
		id=session['id']
		db = mysql.connect()
		cursor = db.cursor()
		cursor.execute("select n_id from expert_notification where expert_id=%s",id)
		for raw in cursor.fetchall():
			count=count+1
		return count
		
		
@app.route('/validate_email_expert_1',methods=['POST'])
def validate_email_expert_1():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			email = request.form['email']
			email1=''
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select email_id from expert_information where expert_id=%s",id)
			for raw in cursor.fetchall():
				email1=raw[0]
			if email1==email:
				return "success"
			else:
				cursor.execute("select * from expert_information where email_id=%s",email)
				x=0
				for raw in cursor.fetchall():
					x=x+1
				if x>0:
					return "wrong"
				else:
					return "success"

		
@app.route('/pi_expert')
def pi_expert():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id=session['id']
			fname=session['name']
			img=session['img']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select * from expert_information where expert_id=%s",id)
			arr=['a']
			for raw in cursor.fetchall():
				arr=raw
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("pi_expert.html",name="Reviewer",k=arr,fname=fname,img=img,c=count,arr=arrx)
		
@app.route('/pi_expert1', methods=['POST'])
def pi_expert1():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id=session['id']
			img = session['img']
			destination='temp'
			for f in request.files.getlist("file"):
				if f.filename in '':
					break
				else:
				
					target=os.path.join('/home/tp/python_flask/Research_Paper/static','Img/')
					filename=f.filename
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
			total_experience = request.form['total_experience']
			experience_in_words = request.form['experience_in_words']
			dob = request.form['date']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute('''update expert_information set first_name=%s,middle_name=%s,last_name=%s,mobile_no=%s,email_id=%s,date_of_birth=%s,gender=%s,skills=%s,total_experience=%s,experience_in_words=%s,profile_pic=%s where expert_id=%s''', (first,middle,last,mobile,email,dob,gender,skill,total_experience,experience_in_words,img,id))
			db.commit()
			return redirect(url_for('.pi_expert'))
		
@app.route('/expert_announcements')
def expert_announcements():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id=session['id']
			fname=session['name']
			img=session['img']
			arrz=[{'name':'as','date':'12'}]
			arrz.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select announcement_details,announcements_date from announcement where related_to like %s order by announcements_date DESC",'%Reviewer%')
			for raw in cursor.fetchall():
				arrz.append({'name':raw[0],'date':raw[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("Expert_announcement.html",name="Announcement",arr1=arrz,fname=fname,img=img,c=count,arr=arrx)
			


@app.route('/list_of_paper')
def list_of_paper():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id=session['id']
			fname=session['name']
			img=session['img']
			id2=0
			arr=[{'id':'x','topic':'shyam','creation_date':'asd','last':'asd','status':'asasd'}]
			arr.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from paper_of_expert where expert_id=%s",s_id)
			
			for raw in cursor.fetchall():
				cursor.execute("Select creation_date from paper_creation where paper_id=%s",raw[0])
				for raw2 in cursor.fetchall():
					id1=raw2[0]
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select status_name from paper_of_expert,status where paper_of_expert.status_id=status.status_id and paper_id=%s and expert_id=%s",(raw[0],s_id))
				for rawy in cursor.fetchall():
					id2=rawy[0]
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					arr.append({'id':raw[0],'topic':raw1[0],'creation_date':id1,'last':raw1[1],'status':id2})
			
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("expert_list_papers.html",name="List Of Papers",k=arr,fname=fname,img=img,arr=arrx,c=count)
			
@app.route('/paper_to_be_reviwed')
def paper_to_be_reviwed():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id=session['id']
			fname=session['name']
			img=session['img']
			arr=[{'p_id':'1','id':'1','title':'sds'}]
			key=[{'id':'1','name':'sad'}]
			arr.clear()
			key.clear()
			arr1=[{'p_id':'1','id':'1','title':'sds'}]
			key1=[{'id':'1','name':'sad'}]
			arr1.clear()
			key1.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id from paper_of_expert where expert_id=%s and (status_id=%s)",(s_id,7))
			for raw in cursor.fetchall():
				id=raw[0]
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id)
				id1=cursor.fetchone()
				cursor.execute("select title from submission_of_paper where submission_id=%s",id1)
				for raw1 in cursor.fetchall():
					arr.append({'p_id':id,'id':id1,'title':raw1[0]})
				cursor.execute("select keyword_name from paper_keyword where paper_id=%s and submission_id=%s",(id,id1))
				for raw2 in cursor.fetchall():
					key.append({'id':id1,'name':raw2[0]})
			
			cursor.execute("select paper_id from paper_of_expert where expert_id=%s and (status_id=%s)",(s_id,6))
			for raw in cursor.fetchall():
				id=raw[0]
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id)
				id1=cursor.fetchone()
				cursor.execute("select title from submission_of_paper where submission_id=%s",id1)
				for raw1 in cursor.fetchall():
					arr1.append({'p_id':id,'id':id1,'title':raw1[0]})
				cursor.execute("select keyword_name from paper_keyword where paper_id=%s and submission_id=%s",(id,id1))
				for raw2 in cursor.fetchall():
					key1.append({'id':id1,'name':raw2[0]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("paper_tobe_reviwed.html",name="Paper To Be Reviewed",arr=arrx,key=key,arr1=arr1,key1=key1,fname=fname,img=img,c=count,arr2=arr)
			
@app.route('/review_paper')
def review_paper():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id=session['id']
			fname=session['name']
			img=session['img']
			p_id= request.args.get('p_id', default='', type=str)
			mode= request.args.get('mode', default='', type=str)
			idd=0
			key=[{'name':'hgh'}]
			key.clear()
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
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("Review_Comment.html",name="Review Of Paper",mode=mode,arr=arr,keyw=key,track=track,sub=sub,fname=fname,pp_id=p_id,img=img,c=count,arr1=arrx)
		
@app.route('/accept', methods=['POST'])
def accept():
		if 'id' not in session:
			return render_template("signin.html")
		else:
			p_id=request.args.get('p_id', default='', type=str)
			s_id=session['id']
			dd=datetime.utcnow()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",p_id)
			id=cursor.fetchone()
			if request.form['hdd'] == 'accept':
				cursor.execute("""insert into expert_comment (date_of_comment,expert_id,paper_id,status_id,submission_id) values(%s,%s,%s,%s,%s)""",(dd,s_id,p_id,2,id))
				#cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(2,p_id))
				cursor.execute("""update paper_of_expert set status_id=%s where expert_id=%s and paper_id=%s""",(2,s_id,p_id))
			elif request.form['hdd'] == 'reject':
				cursor.execute("""insert into expert_comment (date_of_comment,expert_id,paper_id,status_id,submission_id) values(%s,%s,%s,%s,%s)""",(dd,s_id,p_id,3,id))
				#cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(3,p_id))
				cursor.execute("""update paper_of_expert set status_id=%s where expert_id=%s and paper_id=%s""",(3,s_id,p_id))
			elif request.form['hdd'] == 'rejectwithcomment':
				comment=request.form['comment']
				cursor.execute("""insert into expert_comment (comment_message,date_of_comment,expert_id,paper_id,status_id,submission_id) values(%s,%s,%s,%s,%s,%s)""",(comment,dd,s_id,p_id,5,id))
				#cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(5,p_id))
				cursor.execute("""update paper_of_expert set status_id=%s where expert_id=%s and paper_id=%s""",(5,s_id,p_id))
			elif request.form['hdd'] == 'acceptwithcomment':
				comment=request.form['comment']
				cursor.execute("""insert into expert_comment (comment_message,date_of_comment,expert_id,paper_id,status_id,submission_id) values(%s,%s,%s,%s,%s,%s)""",(comment,dd,s_id,p_id,4,id))
				#cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(4,p_id))
				cursor.execute("""update paper_of_expert set status_id=%s where expert_id=%s and paper_id=%s""",(4,s_id,p_id))
			elif request.form['hdd'] == 'continuewithmodification':
				comment=request.form['comment']
				cursor.execute("""insert into expert_comment (comment_message,date_of_comment,expert_id,paper_id,status_id,submission_id) values(%s,%s,%s,%s,%s,%s)""", (comment,dd,s_id,p_id,6,id))
				#cursor.execute("""update paper_creation set status_id=%s where paper_id=%s""",(6,p_id))
				cursor.execute("""update paper_of_expert set status_id=%s where expert_id=%s and paper_id=%s""",(6,s_id,p_id))
			cursor.execute("insert into admin_notification (n_id) values(%s)",(3))
			db.commit()
			return redirect(url_for('.paper_to_be_reviwed'))
		
@app.route('/paper_already_review')
def paper_already_review():

		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id=session['id']
			fname=session['name']
			img=session['img']
			arr=[{'id':'1','title':'sds','stat':'x','p_id':'x'}]
			key=[{'id':'1','name':'sad'}]
			arr.clear()
			key.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select paper_id from paper_of_expert where expert_id=%s and (status_id=2 or status_id=3 or status_id=4 or status_id=5)",s_id)
			for raw in cursor.fetchall():
				id=raw[0]
				cursor.execute("select MAX(submission_id) from submission_of_paper where paper_id=%s",id)
				id1=cursor.fetchone()
				cursor.execute("Select status_name from paper_of_expert,status where paper_of_expert.status_id=status.status_id and paper_id=%s and expert_id=%s",(id,s_id))
				for rawx in cursor.fetchall():
					
					id2=rawx[0]
				cursor.execute("select title from submission_of_paper where submission_id=%s",id1)
				for raw1 in cursor.fetchall():
					arr.append({'id':id1,'title':raw1[0],'stat':id2,'p_id':id})
				
				cursor.execute("select keyword_name from paper_keyword where paper_id=%s and submission_id=%s",(id,id1))
				for raw2 in cursor.fetchall():
					key.append({'id':id1,'name':raw2[0]})	
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("reviewed_paper.html",name="Reviewed Paper",arr=arrx,key=key,fname=fname,img=img,arr1=arr,c=count)
			
@app.route('/review_paper_1')
def review_paper_1():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id=session['id']
			fname=session['name']
			img=session['img']
			search= request.args.get('search', default='', type=str)
			p_id= request.args.get('p_id', default='', type=str)
			mode= request.args.get('mode', default='', type=str)
			idd='0'
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
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("Review_Comment_1.html",name="Review Of Paper",search=search,mode=mode,arr=arr,keyw=key,track=track,sub=sub,fname=fname,pp_id=p_id,img=img,c=count,arr1=arrx)
			
@app.route('/expert_comment')	
def expert_comment():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			s_id = session['id']
			img=session['img']
			fname=session['name']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("Select paper_id from paper_of_expert where expert_id=%s and (status_id=%s or status_id=%s or status_id=%s)",(s_id,4,5,6))
			arr=[{'id':'12','topic':'shyam','creation_date':'asd','last':'asd','status':'asasd','p_id':'x'}]
			arr.clear()
			for raw in cursor.fetchall():
				cursor.execute("Select creation_date from paper_creation where paper_id=%s",raw[0])
				for raw2 in cursor.fetchall():
					id1=raw2[0]
				cursor.execute("Select MAX(submission_id) from submission_of_paper where paper_id=%s",raw[0])
				id=cursor.fetchone()
				cursor.execute("Select status_name from paper_of_expert,status where paper_of_expert.status_id=status.status_id and paper_id=%s and expert_id=%s",(raw[0],s_id))
				for rawy in cursor.fetchall():
					id2=rawy[0]
				cursor.execute("Select title,last_modified_date from submission_of_paper where submission_id=%s",id)
				for raw1 in cursor.fetchall():
					arr.append({'id':id,'topic':raw1[0],'creation_date':id1,'last':raw1[1],'status':id2,'p_id':raw[0]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("expert_list_papers_1.html",name="List Of Papers",k=arr,fname=fname,img=img,arr=arrx,c=count)
			
@app.route('/expert_comment_1')	
def expert_comment_1():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			p_id= request.args.get('p_id', default='', type=str)
			s_id = session['id']
			img=session['img']
			fname=session['name']
			p_id= request.args.get('p_id', default='', type=str)
			mode= request.args.get('mode', default='', type=str)
			max=0
			sss=0
			submission=[{'count':'1','id':'1','title':'abc'}]
			submission.clear()
			comment=[{'id':'1','date':'asa','comment':'dsd'}]
			comment.clear()
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select status_id from paper_creation where paper_id=%s",p_id)
			for raw in cursor.fetchall():
				sss=raw[0]
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
				cursor.execute("select comment_message,date_of_comment from expert_comment where submission_id=%s and expert_id=%s",(raw['id'],s_id))
				for raw1 in cursor.fetchall():
					comment.append({'id':raw['id'],'comment':raw1[0],'date':raw1[1]})
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("expert_comment_view.html",name="Summary of Paper",mode=mode,c=comment,ss1=sss,s=submission,fname=fname,img=img,p_id=p_id,d=count,arr=arrx)

@app.route('/expert_change_pass')
def expert_change_pass():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			fname = session['name']
			img = session['img']
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("expert_change_password.html",name="Change Password",fname=fname,img=img,arr=arrx,c=count)

@app.route('/expert_change_pass_1',methods=['POST'])
def expert_change_pass_1():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:
			id = session['id']
			old=request.form['old1']
			new=request.form['new1']
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("select password from expert_information where expert_id=%s",id)
			for raw in cursor.fetchall():
				pas=raw[0]
			if pas == old:
				cursor.execute("update expert_information set password=%s where expert_id=%s",(new,id))
				db.commit()
				return "success"
			else:
				return "wrong"	


@app.route("/expert_search",methods=['POST','GET'])
def expert_search():	
		
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
			arrx=[{'time':1,'type':1,'message':'sds'}]
			arrx.clear()
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("expert_search.html",name="Search",search=search,k=arr,img=img,fname=fname,x=x,c=count,arr=arrx)	

@app.route('/get_details_by_submission_id')
def get_details_by_submission_id():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:	
			id = session['id']
			fname=session['name']
			img=session['img']	
			s_id= request.args.get('s_id', default='', type=str)
			p_id= request.args.get('p_id', default='', type=str)
			mode=request.args.get('mode', default='', type=str)
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
			arrx=notify_expert(arrx)
			count=noticount_expert()
			return render_template("Review_Comment_1.html",name="Paper Details",mode=mode,p_id=p_id,img=img,arr=arr,keyw=key,track=track,sub=sub,fname=fname,s_id=s_id,c=count,arr1=arrx)			
			
@app.route('/expert_notification_delete',methods=['POST','GET'])
def expert_notification_delete():
		
		if 'id' not in session:
			return render_template("signin.html")
		else:	
			s_id = session['id']
			noty=0
			index=request.args.get('index', default='', type=str)
			i=int(index)
			db = mysql.connect()
			cursor = db.cursor()
			cursor.execute("delete from expert_notification where n_id=%s and expert_id=%s",(i,s_id))
			db.commit()
			return redirect(url_for('.paper_to_be_reviwed'))	
			