import os
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,validators,PasswordField,IntegerField
from functools import wraps
from forms import RegistrationForm,LoginForm

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SECRET_KEY'] = 'secret123'

store = {}
store['tommy'] = '12345'



mysql=MySQL(app)

@app.route('/')
def index():
	return render_template('home.html')

#register user	
@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST' and form.validate() :
		name =request.form['name']
		roll_no = request.form['roll_no']
		email = request.form['email']
		password = request.form['password']
		confirm_password =  request.form['confirm_password']
		error =None
		if not name:
			error = "Name is required"
		elif not roll_no:
			error = "Roll number is  required"
		elif not email:
			error = "Email is required"
		elif not password:
			error = "Password is required"
		elif password != confirm_password:
			error = "Password does not match"
		else :
			if name in store:
				error = 'User {} is already registered.'.format(name)
			else:
				error = 'Account created for {}.'.format(name)
				store['name'] = password
			
			'''cur = mysql.connection.cursor()
			result = cur.execute('SELECT * FROM student WHERE roll_no = %s',[roll_no])
			if result.fetchone  is not None:
				error = 'User {} is already registered.'.format(name)
			else :
				cur.execute('INSERT INTO student(roll_no,name,email,password) VALUES (%s,%s,%s,%s)'
									,(roll_no,name,email,password))
				error = 'Account created for {}.'.format(username)
			cur.close()'''


		flash(error)
		return redirect(url_for('login'))

	return render_template('register.html')

		
username = ""
useremail = ""
userroll_no = ""

#user login
@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm(request.form)
	if request.method=='POST' and form.validate():
		name = request.form['name']
		roll_no = request.form['roll_no']
		condidate_password = request.form['password']
		if name in store:
			if store[name] == condidate_password:
				session['logged_in'] =  True
				session['name'] = name
				session['password'] = password
				flash('You are now logged in','success')
				return redirect(url_for('dashboard'))
			else:
				flash('password is incorrect')
				return render_template('login.html')

			'''cur=mysql.connection.cursor()

		result=cur.execute('SELECT * FROM student WHERE roll_no = %s', [roll_no])

		if result > 0:
			data=cur.fetchone()
			password=data['password']
			if condidate_password ==  password:
				session['logged_in']=True
				session['roll_no']=data['roll_no']
				session['name']=data['name']
				session['email']=data['email']
				global username,useremail,userroll_no
				username=data['name']
				useremail = data['email']
				userroll_no =data['roll_no']
				flash('You are now logged in','success')
				return redirect('dashboard.html')
		
			else:
				error='Invalid Login'
				return render_template('login.html',error=error)
			cur.close()	
		'''
		else:
			error = 'Name is not found'
			return render_template('login.html', error=error)

	return render_template(url_for('login'))

adminemail = ""
adminpassword = ""
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
	form = RegistrationForm()
	if request.method == 'POST' and form.validate():
		admin_email = request.form['email']
		admin_password = request.form['password']
		error = None
		if admin_email == 'admin@gmail.com' and admin_password == '12345':
			session['admin_loggedin']=True
			session['admin_email'] = admin_email
			session['admin_password'] = admin_password
			global adminemail, adminpassword
			adminemail =  admin_email
			adminpassword = admin_password
			error = 'login successfully as admin'
		else:
			error = 'Please check your email or password'
		flash(error)
		return render_template(url_for('dashboard'))
	return render_template(url_for('admin_login'))


def admin_login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'admin_loggedin' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorised,Please login','danger')
			return redirect(url_for('admin_login'))	
	return wrap	

def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorised,Please login','danger')
			return redirect(url_for('login'))	
	return wrap	


@app.route('/logout_admin',methods = ['GET','POST'])
@admin_login_required
def logout_admin():
	session.pop('admin_loggedin',None)
	session.pop('admin_email',None)
	session.pop('admin_password',None)
	flash('You are now logged out','success')
	return redirect(url_for('admin_login'))

@app.route('/logout_student',methods = ['GET','POST'])
@login_required
def logout_student():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))



if __name__ == '__main__':
	app.run(debug=True)
